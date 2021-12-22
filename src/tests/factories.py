from datetime import datetime, timedelta, timezone, tzinfo

from core.lib.jwt import encode_jwt, hash_password, check_password, generate_temp_password
from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.models.scheduler.scheduled_job import ScheduledJob
from core.models.reset_token import ResetToken
from core.lib.utilities import id_generator
from core.lib.constants import WORKER_QUEUE


def create_user_profile(session,
                        first_name="Joe",
                        last_name="Example",
                        email="user@example.org",
                        is_admin=False,
                        password="Password1!",
                        timestamp=datetime.now(tz=timezone.utc)):
    profile = Profile()
    profile.first_name = first_name
    profile.last_name = last_name
    profile.email = email
    profile.is_admin = is_admin
    profile.password = hash_password(password)
    profile.timestamp = timestamp
    session.add(profile)
    session.commit()
    return profile


def create_plaid_item(session,
                      profile_id=None,
                      item_id=id_generator(16),
                      timestamp=datetime.now(tz=timezone.utc)):
    # seed in a plaid item
    if profile_id is None:
        profile = create_user_profile(session)
        profile_id = profile.id

    plaid_item = PlaidItem()
    plaid_item.item_id = item_id
    plaid_item.profile_id = profile_id
    plaid_item.timestamp = timestamp
    session.add(plaid_item)
    session.commit()
    return plaid_item


def create_scheduled_job(session,
                         job_name='Test Job',
                         json_args=None,
                         cron='0 0 12 1/1 * ? *',
                         active=True,
                         queue=WORKER_QUEUE):
    if json_args is None:
        json_args = {}
    job = ScheduledJob()
    job.job_name = job_name
    job.cron = cron
    job.json_args = json_args
    job.active = active
    job.queue = queue
    session.add(job)
    session.commit()
    return job


def create_reset_token(session, profile_id,
                       token='random token',
                       expiry=None):
    t = ResetToken()

    t.token = token
    t.profile_id = profile_id
    t.expiry = expiry or datetime.now(tz=timezone.utc) + timedelta(days=30)
    t.timestamp = datetime.now(tz=timezone.utc)

    session.add(t)
    session.commit()

    return t
