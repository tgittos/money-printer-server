from tests.helpers import client, db
from tests.factories import create_scheduled_job

# return client.post('/login', data=dict(
#        username=username,
#        password=password
#    ), follow_redirects=True)

#rv = c.post('/api/auth', json={
#        'email': 'flask@example.com', 'password': 'secret'
#    })
#    json_data = rv.get_json()


# /v1/api/admin/schedules
def test_create_schedule_accepts_valid_input(client):
    assert False


# /v1/api/admin/schedules
def test_create_schedule_rejects_invalid_input(client):
    assert False


# /v1/api/admin/schedules/1
def test_get_schedule_returns_a_schedule(db, client):
    session = db.get_session()
    try:
        job = create_scheduled_job(session)
        r = client.get('/v1/api/admin/schedules/' + str(job.id),
                       headers={'Authorization': ''},
                       follow_redirects=True)
        json = r.get_json()
        print(json)
        assert False
    except Exception as e:
        session.close()
        raise e


# /v1/api/admin/schedules
def test_get_schedules_returns_all_schedules(db, client):
    session = db.get_session()
    try:
        job_1 = create_scheduled_job(session)
        job_2 = create_scheduled_job(session)
        r = client.get('/v1/api/admin/schedules', follow_redirects=True)
        json = r.get_json()
        assert False
    except Exception as e:
        session.close()
        raise e


# /v1/api/admin/schedules/1
def test_update_schedule_accepts_valid_input(client):
    assert False


# /v1/api/admin/schedules/1
def test_update_schedule_rejects_invalid_input(client):
    assert False


# /v1/api/admin/schedules/1
def test_delete_schedule_accepts_valid_input(client):
    assert False


# /v1/api/admin/schedules/1
def test_delete_schedule_rejects_invalid_input(client):
    assert False
