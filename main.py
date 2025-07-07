from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import redis
import json
import asyncio
from tasks import change_task_status

app = FastAPI()

# Conexión a Redis
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Modelo de tarea
class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str  # "pending", "in_progress", "completed"

# Endpoint para crear una tarea
@app.post("/tasks/")
async def create_task(task: Task):
    # Guarda la tarea en Redis
    r.set(f"task:{task.id}", task.json())

    # Publica la tarea a los clientes conectados
    r.publish("tasks", task.json())

    # Programa la tarea para cambiar de estado en 10 segundos
    change_task_status.apply_async((task.id,), countdown=10)

    return {"message": "Tarea creada y programada para actualizar en 10s", "task": task.dict()}

# WebSocket para enviar notificaciones en tiempo real
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    pubsub = r.pubsub()
    pubsub.subscribe("tasks")

    try:
        while True:
            message = pubsub.get_message()
            if message and message['type'] == 'message':
                await websocket.send_text(message['data'])
            await asyncio.sleep(0.1)
    finally:
        pubsub.close()
        await websocket.close()
