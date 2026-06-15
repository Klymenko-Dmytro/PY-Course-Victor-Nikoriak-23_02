import asyncio
import json
import aiohttp
import time

# Налаштування
SUBREDDIT = "python"
TOTAL_PAGES_TO_FETCH = 3  # Зменшимо до 3, щоб гарантовано не зловити бан за флуд (Rate Limit)
SIZE_PER_PAGE = 25  # Скільки коментарів тягнути за один запит (макс. 100)
OUTPUT_FILE = "reddit_real_comments.json"

# Актуальне робоче дзеркало Pushshift API
PULLPUSH_URL = "https://api.pullpush.io/reddit/search/comment/"


async def fetch_comments_page(session: aiohttp.ClientSession, page_index: int) -> list:
    """
    Асинхронний запит до реального дзеркала PullPush API.
    """
    current_time = int(time.time())
    # Робимо зсув у часі назад (пагінація), щоб кожен запит отримував унікальні старіші дані
    before_timestamp = current_time - (page_index * 86400)  # Крок в 1 добу назад

    params = {
        'subreddit': SUBREDDIT,
        'size': SIZE_PER_PAGE,
        'before': before_timestamp
    }

    # ТЗ вимагає надсилати кастомний User-Agent, щоб сервер дзеркала розумів, хто робить запит
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) University_Lab_Assignment/1.0'
    }

    try:
        print(f"[Запит] Спроба завантажити сторінку {page_index}...")
        async with session.get(PULLPUSH_URL, params=params, headers=headers, timeout=10) as response:

            if response.status == 200:
                # Читаємо та парсимо JSON відповідь від сервера
                result_json = await response.json()
                comments_data = result_json.get('data', [])
                print(f"[Успіх] Сторінка {page_index} повернула {len(comments_data)} реальних коментарів.")
                return comments_data
            else:
                print(f"[Помилка] Сервер повернув статус {response.status} для сторінки {page_index}")
                return []

    except asyncio.TimeoutError:
        print(f"[Таймаут] Дзеркало занадто довго відповідало на запит сторінки {page_index}")
        return []
    except Exception as e:
        print(f"[Помилка мережі] Не вдалося виконати запит для сторінки {page_index}: {e}")
        return []


async def main():
    start_time = time.time()
    print(f"=== Запуск скачування з дзеркала api.pullpush.io для r/{SUBREDDIT} ===")

    # Створюємо сесію клієнта
    async with aiohttp.ClientSession() as session:
        # Формуємо список асинхронних завдань
        tasks = [fetch_comments_page(session, i) for i in range(TOTAL_PAGES_TO_FETCH)]

        # Конкурентно виконуємо всі запити паралельно
        pages_results = await asyncio.gather(*tasks)

    # Об'єднуємо всі результати в один плаский список
    all_comments = []
    for page_data in pages_results:
        all_comments.extend(page_data)

    end_time = time.time()
    print(f"\n[Завершено] Усі запити оброблено за {end_time - start_time:.4f} сек.")
    print(f"Загалом знайдено коментарів: {len(all_comments)}")

    if not all_comments:
        print("❌ Жодного коментаря не завантажено. Можливо, дзеркало тимчасово офлайн.")
        return

    # Перевіряємо наявність потрібного ключа для сортування (безпечний доступ через get)
    print("Сортування коментарів за зростанням часу (created_utc)...")
    sorted_comments = sorted(all_comments, key=lambda x: x.get('created_utc', 0))

    # Записуємо реальні дані у файл JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sorted_comments, f, indent=4, ensure_ascii=False)

    print(f"✅ Успішно записано реальні дані у файл: {OUTPUT_FILE}")


if __name__ == '__main__':
    # Запуск Event Loop
    asyncio.run(main())
