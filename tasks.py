from celery import Celery
import redis
import json

# Configura Celery usando Redis como broker y backend
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

# Conexión directa a Redis para publicar cambios
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

@celery_app.task
def change_task_status(task_id: int):
    """Cambia el estado de la tarea a 'completed' y publica la actualización"""
    task_key = f"task:{task_id}"
    task_json = r.get(task_key)
    if task_json:
        task = json.loads(task_json)
        task["status"] = "completed"

        # Guarda el nuevo estado
        r.set(task_key, json.dumps(task))

        # Publica el cambio a los clientes WebSocket
        r.publish("tasks", json.dumps(task))
        print(f"✅ Tarea {task_id} actualizada a COMPLETED")
