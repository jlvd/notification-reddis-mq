import asyncio
import httpx
import websockets
import json

API_URL = "http://localhost:8000/tasks/"
WS_URL = "ws://localhost:8000/ws"

test_task = {
    "id": 3,
    "title": "Test con WS mejorado",
    "description": "Prueba POST + WS",
    "status": "pending"
}

async def listen_ws(task_id):
    async with websockets.connect(WS_URL) as ws:
        print("🔌 Conectado al WebSocket. Esperando mensajes...")

        pending_received = False
        completed_received = False

        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=15.0)
                data = json.loads(msg)

                if data["id"] == task_id:
                    print(f"📩 Recibido: {data}")

                    if data["status"] == "pending":
                        pending_received = True
                    if data["status"] == "completed":
                        completed_received = True
                        break
            except asyncio.TimeoutError:
                raise Exception("⏳ Timeout esperando mensajes en WebSocket")

async def send_task():
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(API_URL, json=test_task)
        print("📤 POST enviado. Respuesta:", resp.json())

async def main():
    ws_task = asyncio.create_task(listen_ws(test_task["id"]))
    await asyncio.sleep(1)  # darle tiempo al WS para conectarse
    await send_task()
    await ws_task

if __name__ == "__main__":
    asyncio.run(main())
