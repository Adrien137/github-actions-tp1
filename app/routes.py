from flask import Blueprint, jsonify, request

from .services import add_task, delete_task, get_task, list_tasks, update_task

api = Blueprint("api", __name__)


@api.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "task-api",
        "message": "Application disponible"
    }), 200


@api.get("/metrics")
def metrics():
    tasks = list_tasks()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["done"] is True)
    pending_tasks = total_tasks - completed_tasks

    return jsonify({
        "service": "task-api",
        "version": "1.0.0",
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks
    }), 200


@api.route("/")
def home():
    return {
        "message": "Task Manager API fonctionne",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "tasks": "/api/tasks"
        }
    }


@api.get("/api/tasks")
def tasks_list():
    return jsonify({"tasks": list_tasks()}), 200


@api.get("/api/tasks/<int:task_id>")
def tasks_get(task_id: int):
    task = get_task(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@api.post("/api/tasks")
def tasks_create():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Field title is required"}), 400

    task = add_task(title.strip())
    return jsonify(task), 201


@api.put("/api/tasks/<int:task_id>")
def tasks_update(task_id: int):
    payload = request.get_json(silent=True) or {}
    task = update_task(task_id, payload)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


@api.delete("/api/tasks/<int:task_id>")
def tasks_delete(task_id: int):
    deleted = delete_task(task_id)

    if not deleted:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"deleted": True}), 200