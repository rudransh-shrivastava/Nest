"""Tests for BoardCandidateClaim GraphQL node."""

from unittest.mock import Mock

from apps.owasp.api.internal.nodes.board_candidate_claim import BoardCandidateClaimNode
from apps.owasp.api.internal.nodes.enum import BoardCandidateClaimStatusEnum
from tests.unit.apps.common.graphql_node_base_test import GraphQLNodeBaseTest


class TestBoardCandidateClaimNode(GraphQLNodeBaseTest):
    """Test cases for BoardCandidateClaimNode class."""

    def test_node_fields(self):
        """Test expected fields are present on the node."""
        field_names = {
            field.name for field in BoardCandidateClaimNode.__strawberry_definition__.fields
        }
        expected_field_names = {
            "_id",
            "description",
            "evidences",
            "is_locked",
            "nest_created_at",
            "nest_updated_at",
            "status",
            "title",
            "withdrawn_at",
            "withdrawn_reason",
        }
        assert field_names == expected_field_names

    def test_status_resolver(self):
        """Test status resolver returns enum."""
        mock_claim = Mock()
        mock_claim.status = "DRAFT"

        field = self._get_field_by_name("status", BoardCandidateClaimNode)
        result = field.base_resolver.wrapped_func(None, mock_claim)

        assert result == BoardCandidateClaimStatusEnum.DRAFT

    def test_evidences_resolver(self):
        """Test evidences resolver filters out removed evidences."""
        mock_evidence1 = Mock()
        mock_evidence2 = Mock()

        mock_claim = Mock()
        mock_claim.evidences.filter.return_value = [mock_evidence1, mock_evidence2]

        field = self._get_field_by_name("evidences", BoardCandidateClaimNode)
        result = field.base_resolver.wrapped_func(None, mock_claim)

        assert result == [mock_evidence1, mock_evidence2]
        mock_claim.evidences.filter.assert_called_once_with(is_removed=False)
