from typing import Any

_TASKS = [
    {'id': 1, 'title': 'Créer pipeline GitHub Actions', 'done': True},
    {'id': 2, 'title': 'Déployer container Docker', 'done': False},
]
_NEXT_ID = 3


def list_tasks() -> list[dict[str, Any]]:
    return _TASKS


def get_task(task_id: int) -> dict[str, Any] | None:
    return next((task for task in _TASKS if task['id'] == task_id), None)


def add_task(title: str) -> dict[str, Any]:
    global _NEXT_ID
    task = {'id': _NEXT_ID, 'title': title, 'done': False}
    _TASKS.append(task)
    _NEXT_ID += 1
    return task


def update_task(task_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
    task = get_task(task_id)
    if task is None:
        return None
    if isinstance(payload.get('title'), str) and payload['title'].strip():
        task['title'] = payload['title'].strip()
    if isinstance(payload.get('done'), bool):
        task['done'] = payload['done']
    return task


def delete_task(task_id: int) -> bool:
    task = get_task(task_id)
    if task is None:
        return False
    _TASKS.remove(task)
    return True
