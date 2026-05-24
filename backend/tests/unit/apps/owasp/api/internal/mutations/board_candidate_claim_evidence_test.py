"""Tests for board candidate claim evidence mutations."""

from unittest.mock import MagicMock, patch

import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from graphql import GraphQLError

from apps.owasp.api.internal.mutations.board_candidate_claim_evidence import (
    BoardCandidateClaimEvidenceMutation,
)


@pytest.fixture(autouse=True)
def _mock_transaction_atomic():
    """Disable transaction.atomic decorator for all tests."""
    with (
        patch("django.db.transaction.Atomic.__enter__", return_value=None),
        patch("django.db.transaction.Atomic.__exit__", return_value=False),
    ):
        yield


@pytest.fixture
def mutation():
    return BoardCandidateClaimEvidenceMutation()


def _make_info(user):
    info = MagicMock()
    info.context.request.user = user
    return info


class TestCreateBoardCandidateClaimEvidence:
    """Tests for create_board_candidate_claim_evidence."""

    @patch("apps.owasp.api.internal.mutations.board_candidate_claim_evidence.BoardCandidateClaim")
    @patch(
        "apps.owasp.api.internal.mutations.board_candidate_claim_evidence.BoardCandidateClaimEvidence"
    )
    def test_create_evidence_success(self, mock_evidence_cls, mock_claim_cls, mutation):
        user = MagicMock()
        user.username = "testuser"
        user.github_user = "gh_user_123"
        info = _make_info(user)

        input_data = MagicMock()
        input_data.claim_id = 10
        input_data.title = "My Evidence"
        input_data.description = "My Desc"
        input_data.source_url = "https://example.com"

        mock_claim = MagicMock()
        mock_claim_cls.objects.get.return_value = mock_claim

        mock_evidence = MagicMock()
        mock_evidence_cls.return_value = mock_evidence

        result = mutation.create_board_candidate_claim_evidence(info, input_data)

        assert result == mock_evidence
        mock_evidence.full_clean.assert_called_once()
        mock_evidence.save.assert_called_once()
        mock_evidence_cls.assert_called_once_with(
            claim=mock_claim,
            title="My Evidence",
            description="My Desc",
            source_url="https://example.com",
        )

    @patch("apps.owasp.api.internal.mutations.board_candidate_claim_evidence.BoardCandidateClaim")
    def test_create_evidence_claim_not_found(self, mock_claim_cls, mutation):
        user = MagicMock()
        info = _make_info(user)
        input_data = MagicMock()

        mock_claim_cls.DoesNotExist = type("DoesNotExist", (Exception,), {})
        mock_claim_cls.objects.get.side_effect = mock_claim_cls.DoesNotExist

        with pytest.raises(ObjectDoesNotExist):
            mutation.create_board_candidate_claim_evidence(info, input_data)


class TestUpdateBoardCandidateClaimEvidence:
    """Tests for update_board_candidate_claim_evidence."""

    @patch(
        "apps.owasp.api.internal.mutations.board_candidate_claim_evidence.BoardCandidateClaimEvidence"
    )
    def test_update_evidence_success(self, mock_evidence_cls, mutation):
        user = MagicMock()
        user.github_user = "gh_user_123"
        info = _make_info(user)

        input_data = MagicMock()
        input_data.id = 1
        input_data.title = "Updated Title"
        input_data.description = "Updated Desc"
        input_data.source_url = "https://example.com/updated"

        mock_evidence = MagicMock()
        mock_objects = mock_evidence_cls.objects
        mock_objects.select_related.return_value.select_for_update.return_value.get.return_value = mock_evidence

        result = mutation.update_board_candidate_claim_evidence(info, input_data)

        assert result == mock_evidence
        assert mock_evidence.title == "Updated Title"
        assert mock_evidence.description == "Updated Desc"
        assert mock_evidence.source_url == "https://example.com/updated"
        mock_evidence.save.assert_called_once()

    @patch(
        "apps.owasp.api.internal.mutations.board_candidate_claim_evidence.BoardCandidateClaimEvidence"
    )
    def test_update_evidence_validation_error(self, mock_evidence_cls, mutation):
        user = MagicMock()
        info = _make_info(user)
        input_data = MagicMock()

        mock_evidence = MagicMock()
        mock_evidence.save.side_effect = ValidationError("Invalid evidence")
        mock_objects = mock_evidence_cls.objects
        mock_objects.select_related.return_value.select_for_update.return_value.get.return_value = mock_evidence

        with pytest.raises(GraphQLError) as exc:
            mutation.update_board_candidate_claim_evidence(info, input_data)

        assert exc.value.extensions.get("code") == "VALIDATION_ERROR"


class TestRemoveBoardCandidateClaimEvidence:
    """Tests for remove_board_candidate_claim_evidence."""

    @patch("apps.owasp.api.internal.mutations.board_candidate_claim_evidence.timezone")
    @patch(
        "apps.owasp.api.internal.mutations.board_candidate_claim_evidence.BoardCandidateClaimEvidence"
    )
    def test_remove_evidence_success(self, mock_evidence_cls, mock_timezone, mutation):
        user = MagicMock()
        user.github_user = "gh_user_123"
        info = _make_info(user)

        input_data = MagicMock()
        input_data.id = 1
        input_data.removed_reason = "No longer relevant"

        mock_evidence = MagicMock()
        mock_objects = mock_evidence_cls.objects
        mock_objects.select_related.return_value.select_for_update.return_value.get.return_value = mock_evidence
        mock_timezone.now.return_value = "2026-05-24T12:00:00Z"

        result = mutation.remove_board_candidate_claim_evidence(info, input_data)

        assert result == mock_evidence
        assert mock_evidence.is_removed is True
        assert mock_evidence.removed_at == "2026-05-24T12:00:00Z"
        assert mock_evidence.removed_reason == "No longer relevant"
        mock_evidence.save.assert_called_once()
