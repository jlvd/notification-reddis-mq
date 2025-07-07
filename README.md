# 📬 Notification Queue with FastAPI, Redis, Celery and WebSockets

Este proyecto es una prueba de concepto (PoC) para implementar un sistema de tareas asincrónicas con cambio de estado diferido, usando:  

- 🐍 **Python** con **FastAPI** como API backend  
- 🐇 **Redis** como broker de mensajes  
- 🥬 **Celery** para procesar tareas en segundo plano  
- 🌐 **WebSockets** para notificar cambios en tiempo real a los clientes  

---

## 🚀 Tecnologías

✅ **FastAPI** – API REST rápida y moderna  
✅ **Redis** – Cola de mensajes y pub/sub  
✅ **Celery** – Ejecución de tareas asincrónicas, se consideró time.sleep, theading, sched, asyncio, eta y celery
✅ **WebSockets** – Comunicación bidireccional en tiempo real  
✅ **HTTPX** y **websockets** – Cliente HTTP y WS para pruebas  

---

## 📂 Estructura

```
notification-reddis-mq/
├── main.py         # API FastAPI + WebSocket
├── worker.py       # Configuración Celery
├── test.py         # Script de prueba POST + WS
├── test_delay.py   # Pruebas de diferentes librerías delay
├── test_redis.py   # Para verificar que redis está instalado y funcionando
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.10+  
- Redis corriendo en `localhost:6379`  
- Pipenv o virtualenv recomendado  

---

## 🛠 Instalación

1️⃣ Clona el repositorio:  
```bash
git clone https://github.com/tu_usuario/notification-reddis-mq.git
cd notification-reddis-mq
```

2️⃣ Crea un entorno virtual e instala dependencias:  
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac

pip install -r requirements.txt
```

3️⃣ Asegúrate de tener Redis corriendo:  
```bash
redis-server
```

---

## ▶️ Ejecución

1️⃣ Levanta el API FastAPI:  
```bash
uvicorn main:app --reload
```

2️⃣ En otra terminal, inicia el worker de Celery:  
```bash
celery -A worker worker --pool=solo --loglevel=info
```
ó
```python
python worker.py
```


3️⃣ (Opcional) Ejecuta el script de prueba:  
```bash
python test.py
```

---

## 📡 Flujo del sistema

1. Se crea una tarea (`POST /tasks/`).  
2. El estado inicial de la tarea es `pending`.  
3. La tarea se encola en Celery y tras **10 segundos** su estado pasa a `completed`.  
4. Los clientes conectados vía WebSocket reciben ambos eventos en tiempo real.

---

## 🧪 Test rápido

```bash
python test.py
```

✅ Envía una tarea  
✅ Escucha por WebSocket los estados `pending` → `completed`  

---
