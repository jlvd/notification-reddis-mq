import redis

# Conexión a Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Probar set/get
r.set("test", "funciona")
print(r.get("test"))  # Debería imprimir: funciona
