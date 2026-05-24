"""OWASP Board Candidate Claim GraphQL queries."""

import base64

import strawberry
import strawberry_django

from apps.owasp.api.internal.nodes.board_candidate_claim import BoardCandidateClaimNode
from apps.owasp.models.board_candidate_claim import BoardCandidateClaim
from apps.owasp.models.entity_member import EntityMember


def decode_relay_id(relay_id: str) -> str:
    """Decode a Relay Global ID (e.g. EntityMemberNode:3106) to its numeric ID."""
    try:
        decoded = base64.b64decode(relay_id).decode()
        return decoded.split(":")[1]
    except Exception:
        return relay_id


@strawberry.type
class BoardCandidateClaimQuery:
    """GraphQL queries for Board Candidate Claim model."""

    @strawberry_django.field
    def board_candidate_claim(
        self,
        info: strawberry.Info,
        id: strawberry.ID,  # noqa: A002
    ) -> BoardCandidateClaimNode | None:
        """Resolve a single board candidate claim by ID.

        Only the owning candidate can view their claim.
        """
        user = info.context.request.user
        if not user.is_authenticated:
            return None

        try:
            return BoardCandidateClaim.objects.get(
                pk=id,
                candidate__member=user.github_user,
            )
        except BoardCandidateClaim.DoesNotExist:
            return None

    @strawberry_django.field
    def board_candidate_claims(
        self, info: strawberry.Info, year: int, login: str
    ) -> list[BoardCandidateClaimNode]:
        """Resolve all claims for a given candidate."""
        user = info.context.request.user

        try:
            from django.contrib.contenttypes.models import ContentType

            from apps.owasp.models.board_of_directors import BoardOfDirectors

            board = BoardOfDirectors.objects.get(year=year)
            board_type = ContentType.objects.get_for_model(BoardOfDirectors)

            candidate = EntityMember.objects.get(
                entity_type=board_type,
                entity_id=board.id,
                member__login=login,
                role=EntityMember.Role.CANDIDATE,
            )
        except (BoardOfDirectors.DoesNotExist, EntityMember.DoesNotExist):
            return []

        claims = BoardCandidateClaim.objects.filter(candidate=candidate)

        # Candidates can see all their claims. Others can only see APPROVED claims.
        if user.is_authenticated and candidate.member == user.github_user:
            return claims

        return claims.filter(status=BoardCandidateClaim.Status.APPROVED)
