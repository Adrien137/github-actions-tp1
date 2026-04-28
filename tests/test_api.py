from app import create_app


def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_health():
    response = client().get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_list_tasks():
    response = client().get('/api/tasks')
    assert response.status_code == 200
    assert 'tasks' in response.get_json()


def test_create_task():
    response = client().post('/api/tasks', json={'title': 'Nouvelle tâche'})
    assert response.status_code == 201
    assert response.get_json()['title'] == 'Nouvelle tâche'


def test_create_task_without_title():
    response = client().post('/api/tasks', json={})
    assert response.status_code == 400


def test_update_task():
    response = client().put('/api/tasks/1', json={'done': True})
    assert response.status_code == 200
    assert response.get_json()['done'] is True


def test_get_unknown_task():
    response = client().get('/api/tasks/999')
    assert response.status_code == 404
