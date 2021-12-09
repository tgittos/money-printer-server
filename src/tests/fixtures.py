from datetime import datetime, timezone

from core.lib.jwt import encode_jwt, hash_password, check_password, generate_temp_password
from core.models.profile import Profile
from core.models.plaid_item import PlaidItem

PLAID_ITEM_ID = "my_plaid_item_id"


def seed_fixtures(db):
    s = db.get_session()

    # seed in an admin profile
    admin_profile = Profile()
    admin_profile.email = "admin@example.org"
    admin_profile.is_admin = True
    admin_profile.password = hash_password("Password1!")
    admin_profile.timestamp = datetime.now(tz=timezone.utc)
    s.add(admin_profile)
    s.commit()

    # seed in a plaid item
    plaid_item = PlaidItem()
    plaid_item.item_id = PLAID_ITEM_ID
    plaid_item.profile_id = admin_profile.id
    plaid_item.timestamp = datetime.now(tz=timezone.utc)
    s.add(plaid_item)

    db.commit_session(s)
