"""OWASP Board Candidate Claim Evidence GraphQL node."""

from __future__ import annotations

import strawberry
import strawberry_django
from strawberry.file_uploads import Upload  # noqa: TC002

from apps.owasp.models.board_candidate_claim_evidence import BoardCandidateClaimEvidence


@strawberry_django.type(
    BoardCandidateClaimEvidence,
    fields=[
        "description",
        "file_name",
        "file_size",
        "is_removed",
        "nest_created_at",
        "nest_updated_at",
        "removed_at",
        "removed_reason",
        "source_url",
        "title",
    ],
)
class BoardCandidateClaimEvidenceNode(strawberry.relay.Node):
    """Board candidate claim evidence node."""


@strawberry.input
class CreateBoardCandidateClaimEvidenceInput:
    """Input for creating board candidate claim evidence."""

    claim_id: strawberry.ID
    title: str
    description: str = ""
    source_url: str | None = None
    file: Upload | None = None


@strawberry.input
class UpdateBoardCandidateClaimEvidenceInput:
    """Input for updating board candidate claim evidence."""

    id: strawberry.ID
    title: str | None = None
    description: str | None = None
    source_url: str | None = None
    file: Upload | None = None


@strawberry.input
class RemoveBoardCandidateClaimEvidenceInput:
    """Input for removing board candidate claim evidence."""

    id: strawberry.ID
    removed_reason: str = ""
