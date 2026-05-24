"""GraphQL enum for OWASP Board Candidate Claims."""

import enum

import strawberry

from apps.owasp.models.board_candidate_claim import BoardCandidateClaim


@strawberry.enum
class BoardCandidateClaimStatusEnum(enum.Enum):
    """Board candidate claim status enum."""

    DRAFT = BoardCandidateClaim.Status.DRAFT
    DISCARDED = BoardCandidateClaim.Status.DISCARDED
    SUBMITTED = BoardCandidateClaim.Status.SUBMITTED
    APPROVED = BoardCandidateClaim.Status.APPROVED
    REJECTED = BoardCandidateClaim.Status.REJECTED
    WITHDRAWN = BoardCandidateClaim.Status.WITHDRAWN
