from tasks import celery_app

@celery_app.task
def saludo(nombre: str) -> str:
    return f"Hola, {nombre}!"

saludo.apply_async(args=["Mundo"], countdown=5)