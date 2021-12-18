from tests.helpers import client, db
from tests.factories import create_user_profile

def test_sync_profile(db, client):
    session = db.get_session()
    profile = create_user_profile(session)

