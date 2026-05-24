"""Tests for board candidate claim mutations."""

from unittest.mock import MagicMock, patch

import pytest
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from graphql import GraphQLError

from apps.owasp.api.internal.mutations.board_candidate_claim import BoardCandidateClaimMutation
from apps.owasp.api.internal.nodes.enum import BoardCandidateClaimStatusEnum


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
    return BoardCandidateClaimMutation()


def _make_info(user):
    info = MagicMock()
    info.context.request.user = user
    return info


class TestCreateBoardCandidateClaim:
    """Tests for create_board_candidate_claim."""

    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.EntityMember")
    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.BoardCandidateClaim")
    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.BoardOfDirectors")
    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.ContentType")
    def test_create_claim_success(
        self, mock_content_type, mock_board, mock_claim_cls, mock_entity_member_cls, mutation
    ):
        user = MagicMock()
        user.username = "testuser"
        user.github_user = "gh_user_123"
        info = _make_info(user)

        input_data = MagicMock()
        input_data.year = 2025
        input_data.login = "testuser"
        input_data.title = "My Claim"
        input_data.description = "My Desc"

        mock_board_obj = MagicMock()
        mock_board_obj.id = 100
        mock_board.objects.get.return_value = mock_board_obj
        mock_content_type.objects.get_for_model.return_value = "board_type"

        mock_candidate = MagicMock()
        mock_candidate.entity_id = 100
        mock_candidate.member = "gh_user_123"
        mock_entity_member_cls.objects.filter.return_value.first.return_value = mock_candidate
        mock_entity_member_cls.Role.CANDIDATE = "candidate"

        mock_claim = MagicMock()
        mock_claim_cls.return_value = mock_claim

        result = mutation.create_board_candidate_claim(info, input_data)

        assert result == mock_claim
        mock_claim.full_clean.assert_called_once()
        mock_claim.save.assert_called_once()
        mock_claim_cls.assert_called_once_with(
            board_id=100,
            candidate=mock_candidate,
            title="My Claim",
            description="My Desc",
            status=BoardCandidateClaimStatusEnum.DRAFT.value,
        )

    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.EntityMember")
    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.BoardOfDirectors")
    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.ContentType")
    def test_create_claim_not_candidate(
        self, mock_content_type, mock_board, mock_entity_member_cls, mutation
    ):
        user = MagicMock()
        info = _make_info(user)
        input_data = MagicMock()

        mock_board_obj = MagicMock()
        mock_board.objects.get.return_value = mock_board_obj
        mock_content_type.objects.get_for_model.return_value = "board_type"

        mock_entity_member_cls.objects.filter.return_value.first.return_value = None

        with pytest.raises(PermissionDenied, match="You are not a registered candidate"):
            mutation.create_board_candidate_claim(info, input_data)

    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.EntityMember")
    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.BoardCandidateClaim")
    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.BoardOfDirectors")
    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.ContentType")
    def test_create_claim_validation_error(
        self, mock_content_type, mock_board, mock_claim_cls, mock_entity_member_cls, mutation
    ):
        user = MagicMock()
        info = _make_info(user)
        input_data = MagicMock()

        mock_board_obj = MagicMock()
        mock_board.objects.get.return_value = mock_board_obj
        mock_content_type.objects.get_for_model.return_value = "board_type"

        mock_candidate = MagicMock()
        mock_candidate.member = user.github_user
        mock_entity_member_cls.objects.filter.return_value.first.return_value = mock_candidate

        mock_claim = MagicMock()
        mock_claim.full_clean.side_effect = ValidationError("Invalid claim")
        mock_claim_cls.return_value = mock_claim

        with pytest.raises(GraphQLError) as exc:
            mutation.create_board_candidate_claim(info, input_data)

        assert exc.value.extensions.get("code") == "VALIDATION_ERROR"


class TestUpdateBoardCandidateClaim:
    """Tests for update_board_candidate_claim."""

    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.BoardCandidateClaim")
    def test_update_claim_success(self, mock_claim_cls, mutation):
        user = MagicMock()
        user.github_user = "gh_user_123"
        info = _make_info(user)

        input_data = MagicMock()
        input_data.id = 1
        input_data.title = "Updated Title"
        input_data.description = "Updated Desc"
        input_data.status = BoardCandidateClaimStatusEnum.SUBMITTED

        mock_claim = MagicMock()
        mock_claim_cls.objects.select_for_update.return_value.get.return_value = mock_claim

        result = mutation.update_board_candidate_claim(info, input_data)

        assert result == mock_claim
        assert mock_claim.title == "Updated Title"
        assert mock_claim.description == "Updated Desc"
        assert mock_claim.status == BoardCandidateClaimStatusEnum.SUBMITTED.value
        mock_claim.save.assert_called_once()

    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.BoardCandidateClaim")
    def test_update_claim_not_found(self, mock_claim_cls, mutation):
        user = MagicMock()
        info = _make_info(user)
        input_data = MagicMock()

        mock_claim_cls.DoesNotExist = type("DoesNotExist", (Exception,), {})
        mock_objects = mock_claim_cls.objects
        mock_objects.select_for_update.return_value.get.side_effect = mock_claim_cls.DoesNotExist

        with pytest.raises(ObjectDoesNotExist):
            mutation.update_board_candidate_claim(info, input_data)


class TestWithdrawBoardCandidateClaim:
    """Tests for withdraw_board_candidate_claim."""

    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.timezone")
    @patch("apps.owasp.api.internal.mutations.board_candidate_claim.BoardCandidateClaim")
    def test_withdraw_claim_success(self, mock_claim_cls, mock_timezone, mutation):
        user = MagicMock()
        user.github_user = "gh_user_123"
        info = _make_info(user)

        input_data = MagicMock()
        input_data.id = 1
        input_data.withdrawn_reason = "No longer valid"

        mock_claim = MagicMock()
        mock_claim_cls.objects.select_for_update.return_value.get.return_value = mock_claim
        mock_timezone.now.return_value = "2026-05-24T12:00:00Z"

        result = mutation.withdraw_board_candidate_claim(info, input_data)

        assert result == mock_claim
        assert mock_claim.status == BoardCandidateClaimStatusEnum.WITHDRAWN.value
        assert mock_claim.withdrawn_at == "2026-05-24T12:00:00Z"
        assert mock_claim.withdrawn_reason == "No longer valid"
        mock_claim.save.assert_called_once()
