from tasks import celery_app

# Arranca el worker Celery (modo solo para Windows)
celery_app.worker_main([
    "worker",
    "--pool=solo",   # 🛡️ Modo compatible con Windows
    "--loglevel=info",
])
