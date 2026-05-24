"""Tests for BoardCandidateClaim GraphQL queries."""

from unittest.mock import MagicMock, Mock, patch

from apps.owasp.api.internal.queries.board_candidate_claim import BoardCandidateClaimQuery


def _make_info(user, is_authenticated=True):
    info = MagicMock()
    info.context.request.user = user
    user.is_authenticated = is_authenticated
    return info


class TestBoardCandidateClaimQuery:
    """Test cases for BoardCandidateClaimQuery class."""

    @patch("apps.owasp.api.internal.queries.board_candidate_claim.BoardCandidateClaim")
    def test_board_candidate_claim_found(self, mock_claim_cls):
        query = BoardCandidateClaimQuery()
        user = MagicMock()
        user.github_user = "gh_user_123"
        info = _make_info(user)

        mock_claim = Mock()
        mock_claim_cls.objects.get.return_value = mock_claim

        result = query.board_candidate_claim(info=info, id=1)

        mock_claim_cls.objects.get.assert_called_once_with(pk=1, candidate__member="gh_user_123")
        assert result == mock_claim

    @patch("apps.owasp.api.internal.queries.board_candidate_claim.BoardCandidateClaim")
    def test_board_candidate_claim_not_found(self, mock_claim_cls):
        query = BoardCandidateClaimQuery()
        user = MagicMock()
        user.github_user = "gh_user_123"
        info = _make_info(user)

        mock_claim_cls.DoesNotExist = type("DoesNotExist", (Exception,), {})
        mock_claim_cls.objects.get.side_effect = mock_claim_cls.DoesNotExist

        result = query.board_candidate_claim(info=info, id=999)

        assert result is None

    def test_board_candidate_claim_unauthenticated(self):
        query = BoardCandidateClaimQuery()
        user = MagicMock()
        info = _make_info(user, is_authenticated=False)

        result = query.board_candidate_claim(info=info, id=1)
        assert result is None

    @patch("apps.owasp.api.internal.queries.board_candidate_claim.BoardCandidateClaim")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.EntityMember")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.BoardOfDirectors")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.ContentType")
    def test_board_candidate_claims_owner_success(
        self, mock_content_type, mock_board, mock_entity_member_cls, mock_claim_cls
    ):
        query = BoardCandidateClaimQuery()
        user = MagicMock()
        user.github_user = "gh_user_123"
        info = _make_info(user)

        mock_board_obj = Mock()
        mock_board_obj.id = 1
        mock_board.objects.get.return_value = mock_board_obj
        mock_content_type.objects.get_for_model.return_value = "board_type"

        mock_candidate = Mock()
        mock_candidate.member = "gh_user_123"
        mock_entity_member_cls.objects.get.return_value = mock_candidate

        mock_claims = [Mock(), Mock()]
        mock_claim_cls.objects.filter.return_value = mock_claims
        mock_entity_member_cls.Role.CANDIDATE = "candidate"

        result = query.board_candidate_claims(info=info, year=2025, login="testuser")

        mock_entity_member_cls.objects.get.assert_called_once_with(
            entity_type="board_type", entity_id=1, member__login="testuser", role="candidate"
        )
        mock_claim_cls.objects.filter.assert_called_once_with(candidate=mock_candidate)
        assert result == mock_claims

    @patch("apps.owasp.api.internal.queries.board_candidate_claim.BoardCandidateClaim")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.EntityMember")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.BoardOfDirectors")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.ContentType")
    def test_board_candidate_claims_public_success(
        self, mock_content_type, mock_board, mock_entity_member_cls, mock_claim_cls
    ):
        query = BoardCandidateClaimQuery()
        user = MagicMock()
        user.github_user = "gh_user_other"
        info = _make_info(user)

        mock_board_obj = Mock()
        mock_board_obj.id = 1
        mock_board.objects.get.return_value = mock_board_obj
        mock_content_type.objects.get_for_model.return_value = "board_type"

        mock_candidate = Mock()
        mock_candidate.member = "gh_user_123"
        mock_entity_member_cls.objects.get.return_value = mock_candidate

        mock_filtered_claims = [Mock()]
        mock_claim_cls.objects.filter.return_value.filter.return_value = mock_filtered_claims
        mock_claim_cls.Status.APPROVED = "approved"

        result = query.board_candidate_claims(info=info, year=2025, login="testuser")

        mock_claim_cls.objects.filter.assert_called_once_with(candidate=mock_candidate)
        mock_claim_cls.objects.filter.return_value.filter.assert_called_once_with(
            status="approved"
        )
        assert result == mock_filtered_claims

    @patch("apps.owasp.api.internal.queries.board_candidate_claim.EntityMember")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.BoardOfDirectors")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.ContentType")
    def test_board_candidate_claims_not_candidate(
        self, mock_content_type, mock_board, mock_entity_member_cls
    ):
        query = BoardCandidateClaimQuery()
        user = MagicMock()
        user.github_user = "gh_user_123"
        info = _make_info(user)

        mock_board_obj = Mock()
        mock_board_obj.id = 1
        mock_board.objects.get.return_value = mock_board_obj
        mock_content_type.objects.get_for_model.return_value = "board_type"

        mock_entity_member_cls.DoesNotExist = type("DoesNotExist", (Exception,), {})
        mock_entity_member_cls.objects.get.side_effect = mock_entity_member_cls.DoesNotExist

        result = query.board_candidate_claims(info=info, year=2025, login="testuser")

        assert result == []

    @patch("apps.owasp.api.internal.queries.board_candidate_claim.BoardCandidateClaim")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.EntityMember")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.BoardOfDirectors")
    @patch("apps.owasp.api.internal.queries.board_candidate_claim.ContentType")
    def test_board_candidate_claims_unauthenticated(
        self, mock_content_type, mock_board, mock_entity_member_cls, mock_claim_cls
    ):
        query = BoardCandidateClaimQuery()
        user = MagicMock()
        info = _make_info(user, is_authenticated=False)

        mock_board_obj = Mock()
        mock_board_obj.id = 1
        mock_board.objects.get.return_value = mock_board_obj
        mock_content_type.objects.get_for_model.return_value = "board_type"

        mock_candidate = Mock()
        mock_entity_member_cls.objects.get.return_value = mock_candidate

        mock_filtered_claims = [Mock()]
        mock_claim_cls.objects.filter.return_value.filter.return_value = mock_filtered_claims

        result = query.board_candidate_claims(info=info, year=2025, login="testuser")
        assert result == mock_filtered_claims
