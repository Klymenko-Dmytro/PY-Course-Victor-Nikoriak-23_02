import asyncio
import time
import httpx

# Список ендпоінтів вашого Django-проєкту нотаток
URLS = [
    "http://127.0.0.1:8000/notes/",
    "http://127.0.0.1:8000/accounts/",
    "http://127.0.0.1:8000/admin/",
]


async def measure_single_view(client, url):
    """Вимірює час виконання одного запиту"""
    start_time = time.perf_counter()
    try:
        response = await client.get(url)
        status = response.status_code
    except Exception as e:
        status = f"Error: {e}"

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"URL: {url} | Status: {status} | Час: {duration:.4f} сек")
    return duration


async def main():
    # Використовуємо асинхронний клієнт HTTPX
    async with httpx.AsyncClient() as client:
        print("=== ПОЧАТОК ТЕСТУВАННЯ ===")
        total_start = time.perf_counter()

        # Послідовний виклик кожного ендпоінту
        individual_times = []
        for url in URLS:
            duration = await measure_single_view(client, url)
            individual_times.append(duration)

        total_end = time.perf_counter()

        print("\n=== РЕЗУЛЬТАТИ ===")
        print(f"Сума окремих вимірів: {sum(individual_times):.4f} сек")
        print(f"Загальний витрачений час (сумарно): {total_end - total_start:.4f} сек")


if __name__ == "__main__":
    asyncio.run(main())
