import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
django.setup()

from apps.github.models.user import User as GithubUser
from apps.owasp.models.board_of_directors import BoardOfDirectors
from apps.owasp.models.entity_member import EntityMember

board, _ = BoardOfDirectors.objects.get_or_create(
    year=2025, defaults={"name": "2025 Board of Directors", "owasp_url": "https://owasp.org/board"}
)
user, _ = GithubUser.objects.get_or_create(
    login="test_candidate", defaults={"name": "Test Candidate", "email": "test@example.com"}
)

member, created = EntityMember.objects.get_or_create(
    entity_id=board.id,
    member=user,
    role=EntityMember.Role.CANDIDATE,
    defaults={"is_active": True, "title": "Board Candidate"},
)
print("Created/found candidate:", member)
