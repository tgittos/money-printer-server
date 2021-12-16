from datetime import datetime, timezone

from core.lib.jwt import encode_jwt, hash_password, check_password, generate_temp_password
from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.models.scheduler.scheduled_job import ScheduledJob
from core.lib.utilities import id_generator
from core.lib.constants import WORKER_QUEUE


def create_user_profile(session,
                        email="user@example.org",
                        is_admin=False,
                        password="Password1!",
                        timestamp=datetime.now(tz=timezone.utc)):
    profile = Profile()
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
