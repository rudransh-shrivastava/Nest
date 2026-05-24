"""OWASP Board Candidate Claim GraphQL Mutations."""

import base64
import logging

import strawberry
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone
from graphql import GraphQLError

from apps.nest.api.internal.permissions import IsAuthenticated
from apps.owasp.api.internal.nodes.board_candidate_claim import (
    BoardCandidateClaimNode,
    CreateBoardCandidateClaimInput,
    UpdateBoardCandidateClaimInput,
    WithdrawBoardCandidateClaimInput,
)
from apps.owasp.api.internal.nodes.enum import BoardCandidateClaimStatusEnum
from apps.owasp.models.board_candidate_claim import BoardCandidateClaim
from apps.owasp.models.entity_member import EntityMember

logger = logging.getLogger(__name__)


def decode_relay_id(relay_id: str) -> str:
    """Decode a Relay Global ID (e.g. EntityMemberNode:3106) to its numeric ID."""
    try:
        decoded = base64.b64decode(relay_id).decode()
        return decoded.split(":")[1]
    except Exception:
        return relay_id


@strawberry.type
class BoardCandidateClaimMutation:
    """GraphQL mutations related to board candidate claims."""

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
    def create_board_candidate_claim(
        self, info: strawberry.Info, input_data: CreateBoardCandidateClaimInput
    ) -> BoardCandidateClaimNode:
        """Create a new board candidate claim."""
        user = info.context.request.user

        from django.contrib.contenttypes.models import ContentType

        from apps.owasp.models.board_of_directors import BoardOfDirectors

        try:
            board = BoardOfDirectors.objects.get(year=input_data.year)
            board_type = ContentType.objects.get_for_model(BoardOfDirectors)
        except BoardOfDirectors.DoesNotExist:
            board = None
            board_type = None

        if board and board_type:
            candidate = EntityMember.objects.filter(
                entity_type=board_type,
                entity_id=board.id,
                member__login=input_data.login,
                role=EntityMember.Role.CANDIDATE,
            ).first()
        else:
            candidate = None

        if not candidate or candidate.member != user.github_user:
            msg = "You are not a registered candidate for this board."
            logger.warning(
                "Permission denied for user '%s' to create claim for board year '%s'.",
                user.username,
                input_data.year,
            )
            raise PermissionDenied(msg)

        try:
            claim = BoardCandidateClaim(
                board_id=candidate.entity_id,
                candidate=candidate,
                title=input_data.title,
                description=input_data.description,
                status=BoardCandidateClaimStatusEnum.DRAFT.value,
            )
            claim.full_clean()
            claim.save()
        except ValidationError as e:
            raise GraphQLError(
                str(e.message_dict if hasattr(e, "message_dict") else e),
                extensions={"code": "VALIDATION_ERROR"},
            ) from e

        logger.info(
            "User '%s' successfully created board candidate claim '%s' (ID: %s).",
            user.username,
            claim.title,
            claim.id,
        )

        return claim

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
    def update_board_candidate_claim(
        self, info: strawberry.Info, input_data: UpdateBoardCandidateClaimInput
    ) -> BoardCandidateClaimNode:
        """Update an existing board candidate claim."""
        user = info.context.request.user

        try:
            claim = BoardCandidateClaim.objects.select_for_update().get(
                pk=input_data.id,
                candidate__member=user.github_user,
            )
        except BoardCandidateClaim.DoesNotExist as err:
            msg = f"Claim with ID '{input_data.id}' not found or you do not have permission."
            logger.warning(msg, exc_info=True)
            raise ObjectDoesNotExist(msg) from err

        if input_data.title is not None:
            claim.title = input_data.title
        if input_data.description is not None:
            claim.description = input_data.description
        if input_data.status is not None:
            claim.status = input_data.status.value

        try:
            claim.save()
        except ValidationError as e:
            raise GraphQLError(
                str(e.message_dict if hasattr(e, "message_dict") else e),
                extensions={"code": "VALIDATION_ERROR"},
            ) from e

        logger.info(
            "User '%s' successfully updated board candidate claim '%s' (ID: %s).",
            user.username,
            claim.title,
            claim.id,
        )

        return claim

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
    def withdraw_board_candidate_claim(
        self, info: strawberry.Info, input_data: WithdrawBoardCandidateClaimInput
    ) -> BoardCandidateClaimNode:
        """Withdraw a board candidate claim. Allowed even if locked."""
        user = info.context.request.user

        try:
            claim = BoardCandidateClaim.objects.select_for_update().get(
                pk=input_data.id,
                candidate__member=user.github_user,
            )
        except BoardCandidateClaim.DoesNotExist as err:
            msg = f"Claim with ID '{input_data.id}' not found or you do not have permission."
            logger.warning(msg, exc_info=True)
            raise ObjectDoesNotExist(msg) from err

        claim.status = BoardCandidateClaimStatusEnum.WITHDRAWN.value
        claim.withdrawn_at = timezone.now()
        claim.withdrawn_reason = input_data.withdrawn_reason

        try:
            claim.save()
        except ValidationError as e:
            raise GraphQLError(
                str(e.message_dict if hasattr(e, "message_dict") else e),
                extensions={"code": "VALIDATION_ERROR"},
            ) from e

        logger.info(
            "User '%s' successfully withdrew board candidate claim '%s' (ID: %s).",
            user.username,
            claim.title,
            claim.id,
        )

        return claim
