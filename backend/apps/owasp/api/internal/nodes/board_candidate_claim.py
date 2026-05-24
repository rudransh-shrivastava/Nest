"""OWASP Board Candidate Claim GraphQL node."""

from __future__ import annotations

import strawberry
import strawberry_django

from apps.owasp.api.internal.nodes.board_candidate_claim_evidence import (
    BoardCandidateClaimEvidenceNode,  # noqa: TC001
)
from apps.owasp.api.internal.nodes.enum import BoardCandidateClaimStatusEnum
from apps.owasp.models.board_candidate_claim import BoardCandidateClaim


@strawberry_django.type(
    BoardCandidateClaim,
    fields=[
        "description",
        "is_locked",
        "nest_created_at",
        "nest_updated_at",
        "title",
        "withdrawn_at",
        "withdrawn_reason",
    ],
)
class BoardCandidateClaimNode(strawberry.relay.Node):
    """Board candidate claim node."""

    @strawberry_django.field
    def status(self, root: BoardCandidateClaim) -> BoardCandidateClaimStatusEnum:
        """Resolve claim status as enum."""
        return BoardCandidateClaimStatusEnum(root.status)

    @strawberry_django.field(prefetch_related=["evidences"])
    def evidences(self, root: BoardCandidateClaim) -> list[BoardCandidateClaimEvidenceNode]:
        """Resolve non-removed evidences for this claim."""
        return root.evidences.filter(is_removed=False)


@strawberry.input
class CreateBoardCandidateClaimInput:
    """Input for creating a board candidate claim."""

    year: int
    login: str
    title: str
    description: str = ""


@strawberry.input
class UpdateBoardCandidateClaimInput:
    """Input for updating a board candidate claim."""

    id: strawberry.ID
    title: str | None = None
    description: str | None = None
    status: BoardCandidateClaimStatusEnum | None = None


@strawberry.input
class WithdrawBoardCandidateClaimInput:
    """Input for withdrawing a board candidate claim."""

    id: strawberry.ID
    withdrawn_reason: str = ""
