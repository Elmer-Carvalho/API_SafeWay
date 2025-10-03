import httpx

BASE_URL = "http://localhost:8000"  # ajuste se precisar

def test_requests():
    r1 = httpx.get(f"{BASE_URL}/health")
    print("GET /health:", r1.status_code, r1.json())

    r2 = httpx.get(f"{BASE_URL}/api/v1/users")
    print("GET /api/v1/users:", r2.status_code)

    r3 = httpx.get(f"{BASE_URL}/nao_existe")
    print("GET /nao_existe:", r3.status_code)

    logs = httpx.get(f"{BASE_URL}/api/v1/logs/http?limit=10")
    print("Últimos logs gravados:")

    data = logs.json()
    if isinstance(data, list):
        for log in data:
            if isinstance(log, dict):  # garante que é dicionário
                print(f"[{log.get('timestamp')}] {log.get('method')} {log.get('endpoint')} -> {log.get('status_code')}")
            else:
                print("Log bruto:", log)
    else:
        print("Resposta inesperada:", data)

if __name__ == "__main__":
    test_requests()
