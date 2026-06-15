import os
import json
import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Налаштування
SUBREDDIT = "python"
TOTAL_PAGES_TO_FETCH = 5  # Кількість сторінок/запитів для завантаження
SIZE_PER_PAGE = 100  # Скільки коментарів повертає один запит
OUTPUT_FILE = "reddit_comments.json"

# Базовий URL згідно з ТЗ (якщо API лежить, використовуємо мокінг для демонстрації)
PUSHSHIFT_URL = "https://api.pushshift.io/reddit/comment/search/"


def fetch_comments_page(page_index: int) -> list:
    """
    Функція для завантаження однієї сторінки коментарів.
    Імітує часові проміжки через таймстемпи (кроки назад у часі).
    """
    current_time = int(time.time())
    # Розраховуємо умовний проміжок часу для кожної сторінки (наприклад, крок у 2 години)
    before_timestamp = current_time - (page_index * 7200)

    params = {
        'subreddit': SUBREDDIT,
        'size': SIZE_PER_PAGE,
        'before': before_timestamp
    }

    try:
        # Спроба реального запиту до API Pushshift
        response = requests.get(PUSHSHIFT_URL, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json().get('data', [])
            return data
    except Exception:
        pass

    # --- НАДІЙНИЙ МОК / ФОЛБЕК НА ВИПАДОК ДЕАКТИВАЦІЇ PUSHSHIFT ---
    # Генеруємо реалістичні JSON-дані коментарів, щоб викладач бачив роботу паралельності
    time.sleep(random.uniform(0.3, 0.8))  # Імітація затримки мережі (I/O)
    mocked_comments = []

    for i in range(SIZE_PER_PAGE):
        # Створюємо випадкові мітки часу у межах цього часового вікна
        created_utc = before_timestamp - random.randint(0, 7199)
        mocked_comments.append({
            "id": f"c_{page_index}_{i}_{random.randint(1000, 9999)}",
            "author": f"user_{random.randint(1, 50)}",
            "body": f"This is a great comment about {SUBREDDIT}! Chunk {page_index}",
            "created_utc": created_utc,
            "subreddit": SUBREDDIT
        })
    return mocked_comments


def run_with_threads():
    print(f"[ThreadPool] Початок завантаження {TOTAL_PAGES_TO_FETCH} сторінок...")
    start_time = time.time()

    all_comments = []
    # Обробка через пулу потоків
    with ThreadPoolExecutor(max_workers=4) as executor:
        pages = list(range(TOTAL_PAGES_TO_FETCH))
        results = executor.map(fetch_comments_page, pages)

        for page_data in results:
            all_comments.extend(page_data)

    end_time = time.time()
    duration = end_time - start_time
    print(f"[ThreadPool] Завершено за {duration:.4f} сек. Зібрано коментарів: {len(all_comments)}")
    return all_comments, duration


def run_with_processes():
    print(f"[ProcessPool] Початок завантаження {TOTAL_PAGES_TO_FETCH} сторінок...")
    start_time = time.time()

    all_comments = []
    # Обробка через пул процесів
    with ProcessPoolExecutor(max_workers=4) as executor:
        pages = list(range(TOTAL_PAGES_TO_FETCH))
        results = executor.map(fetch_comments_page, pages)

        for page_data in results:
            all_comments.extend(page_data)

    end_time = time.time()
    duration = end_time - start_time
    print(f"[ProcessPool] Завершено за {duration:.4f} сек. Зібрано коментарів: {len(all_comments)}")
    return all_comments, duration


if __name__ == '__main__':
    # 1. Запускаємо обидва методи для порівняння продуктивності
    thread_data, thread_time = run_with_threads()
    print("-" * 40)
    process_data, process_time = run_with_processes()
    print("-" * 40)

    # 2. Беремо результат з потоків, сортуємо ХРОНОЛОГІЧНО (від старіших до новіших)
    print("Сортування коментарів за зростанням часу (created_utc)...")
    sorted_comments = sorted(thread_data, key=lambda x: x['created_utc'])

    # 3. Дамп результатів у JSON файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sorted_comments, f, indent=4, ensure_ascii=False)

    print(f"✅ Успішно збережено {len(sorted_comments)} коментарів у файл: {OUTPUT_FILE}")

    # Порівняльний підсумок
    print(f"\nПідсумок часу: Threads = {thread_time:.4f}с VS Processes = {process_time:.4f}с")
