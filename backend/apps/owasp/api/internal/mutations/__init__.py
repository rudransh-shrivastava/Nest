"""OWASP GraphQL mutations."""

import strawberry

from .board_candidate_claim import BoardCandidateClaimMutation
from .board_candidate_claim_evidence import BoardCandidateClaimEvidenceMutation


@strawberry.type
class OwaspMutations(
    BoardCandidateClaimMutation,
    BoardCandidateClaimEvidenceMutation,
):
    """OWASP mutations."""
