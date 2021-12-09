from datetime import datetime, timezone

from core.lib.jwt import encode_jwt, hash_password, check_password, generate_temp_password
from core.models.profile import Profile


def seed_fixtures(db):
    s = db.get_session()

    # seed in an admin profile
    admin_profile = Profile()
    admin_profile.email = "admin@example.org"
    admin_profile.is_admin = True
    admin_profile.password = hash_password("Password1!")
    admin_profile.timestamp = datetime.now(tz=timezone.utc)
    s.add(admin_profile)

    db.commit_session(s)
