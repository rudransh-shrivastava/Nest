"""Tests for BoardCandidateClaimEvidence GraphQL node."""

from apps.owasp.api.internal.nodes.board_candidate_claim_evidence import (
    BoardCandidateClaimEvidenceNode,
)
from tests.unit.apps.common.graphql_node_base_test import GraphQLNodeBaseTest


class TestBoardCandidateClaimEvidenceNode(GraphQLNodeBaseTest):
    """Test cases for BoardCandidateClaimEvidenceNode class."""

    def test_node_fields(self):
        """Test expected fields are present on the node."""
        field_names = {
            field.name
            for field in BoardCandidateClaimEvidenceNode.__strawberry_definition__.fields
        }
        expected_field_names = {
            "_id",
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
        }
        assert field_names == expected_field_names
