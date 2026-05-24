"""OWASP Board Candidate Claim Evidence GraphQL Mutations."""

import logging

import strawberry
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.utils import timezone
from graphql import GraphQLError

from apps.nest.api.internal.permissions import IsAuthenticated
from apps.owasp.api.internal.nodes.board_candidate_claim_evidence import (
    BoardCandidateClaimEvidenceNode,
    CreateBoardCandidateClaimEvidenceInput,
    RemoveBoardCandidateClaimEvidenceInput,
    UpdateBoardCandidateClaimEvidenceInput,
)
from apps.owasp.models.board_candidate_claim import BoardCandidateClaim
from apps.owasp.models.board_candidate_claim_evidence import BoardCandidateClaimEvidence

logger = logging.getLogger(__name__)


@strawberry.type
class BoardCandidateClaimEvidenceMutation:
    """GraphQL mutations related to board candidate claim evidence."""

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
    def create_board_candidate_claim_evidence(
        self, info: strawberry.Info, input_data: CreateBoardCandidateClaimEvidenceInput
    ) -> BoardCandidateClaimEvidenceNode:
        """Create new board candidate claim evidence."""
        user = info.context.request.user

        try:
            claim = BoardCandidateClaim.objects.get(
                pk=input_data.claim_id,
                candidate__member=user.github_user,
            )
        except BoardCandidateClaim.DoesNotExist as err:
            msg = f"Claim with ID '{input_data.claim_id}' not found or you do not have permission."
            logger.warning(msg, exc_info=True)
            raise ObjectDoesNotExist(msg) from err

        try:
            evidence = BoardCandidateClaimEvidence(
                claim=claim,
                title=input_data.title,
                description=input_data.description,
                source_url=input_data.source_url or "",
            )
            if input_data.file:
                evidence.file = input_data.file
            evidence.full_clean()
            evidence.save()
        except ValidationError as e:
            raise GraphQLError(
                str(e.message_dict if hasattr(e, "message_dict") else e),
                extensions={"code": "VALIDATION_ERROR"},
            ) from e

        logger.info(
            "User '%s' successfully added evidence '%s' (ID: %s) to claim '%s'.",
            user.username,
            evidence.title,
            evidence.id,
            claim.id,
        )

        return evidence

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
    def update_board_candidate_claim_evidence(
        self, info: strawberry.Info, input_data: UpdateBoardCandidateClaimEvidenceInput
    ) -> BoardCandidateClaimEvidenceNode:
        """Update existing board candidate claim evidence."""
        user = info.context.request.user

        try:
            evidence = (
                BoardCandidateClaimEvidence.objects.select_related("claim")
                .select_for_update()
                .get(
                    pk=input_data.id,
                    claim__candidate__member=user.github_user,
                )
            )
        except BoardCandidateClaimEvidence.DoesNotExist as err:
            msg = f"Evidence with ID '{input_data.id}' not found or you do not have permission."
            logger.warning(msg, exc_info=True)
            raise ObjectDoesNotExist(msg) from err

        if input_data.title is not None:
            evidence.title = input_data.title
        if input_data.description is not None:
            evidence.description = input_data.description
        if input_data.source_url is not None:
            evidence.source_url = input_data.source_url
        if input_data.file is not None:
            evidence.file = input_data.file

        try:
            evidence.save()
        except ValidationError as e:
            raise GraphQLError(
                str(e.message_dict if hasattr(e, "message_dict") else e),
                extensions={"code": "VALIDATION_ERROR"},
            ) from e

        logger.info(
            "User '%s' successfully updated evidence '%s' (ID: %s).",
            user.username,
            evidence.title,
            evidence.id,
        )

        return evidence

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
    def remove_board_candidate_claim_evidence(
        self, info: strawberry.Info, input_data: RemoveBoardCandidateClaimEvidenceInput
    ) -> BoardCandidateClaimEvidenceNode:
        """Soft-remove board candidate claim evidence."""
        user = info.context.request.user

        try:
            evidence = (
                BoardCandidateClaimEvidence.objects.select_related("claim")
                .select_for_update()
                .get(
                    pk=input_data.id,
                    claim__candidate__member=user.github_user,
                )
            )
        except BoardCandidateClaimEvidence.DoesNotExist as err:
            msg = f"Evidence with ID '{input_data.id}' not found or you do not have permission."
            logger.warning(msg, exc_info=True)
            raise ObjectDoesNotExist(msg) from err

        # The clean() method checks if the claim is locked, but since we're just
        # soft-removing, we should ideally allow it, or respect the lock.
        # Following strict constraints: we update the fields. If it fails full_clean,
        # the model prevents it.
        evidence.is_removed = True
        evidence.removed_at = timezone.now()
        evidence.removed_reason = input_data.removed_reason

        try:
            evidence.save()
        except ValidationError as e:
            raise GraphQLError(
                str(e.message_dict if hasattr(e, "message_dict") else e),
                extensions={"code": "VALIDATION_ERROR"},
            ) from e

        logger.info(
            "User '%s' successfully removed evidence '%s' (ID: %s).",
            user.username,
            evidence.title,
            evidence.id,
        )

        return evidence
