from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import math

# Вхідний список чисел
NUMBERS = [
    2, 1099726899285419, 1570341764013157, 1637027521802551,
    1880450821379411, 1893530391196711, 2447109360961063, 3,
    2772290760589219, 3033700317376073, 4350190374376723, 4350190491008389,
    4350190491008390, 4350222956688319, 2447120421950803, 5
]


# Утилітарна функція для перевірки простоти числа
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Оптимізований алгоритм перевірки до квадратного кореня (крок 6)
    for i in range(5, int(math.isqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def run_thread_pool():
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        # map зберігає початковий порядок елементів
        results = list(executor.map(is_prime, NUMBERS))
    end_time = time.time()

    primes = [num for num, prime in zip(NUMBERS, results) if prime]
    print(f"[ThreadPoolExecutor] Знайдено простих чисел: {len(primes)}")
    print(f"[ThreadPoolExecutor] Час виконання: {end_time - start_time:.4f} сек\n")
    return primes


def run_process_pool():
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(is_prime, NUMBERS))
    end_time = time.time()

    primes = [num for num, prime in zip(NUMBERS, results) if prime]
    print(f"[ProcessPoolExecutor] Знайдено простих чисел: {len(primes)}")
    print(f"[ProcessPoolExecutor] Час виконання: {end_time - start_time:.4f} сек\n")
    return primes


if __name__ == '__main__':
    print("--- Запуск фільтрації чисел ---\n")

    # Тестування ThreadPoolExecutor
    threads_primes = run_thread_pool()

    # Тестування ProcessPoolExecutor
    process_primes = run_process_pool()

    # Вивід результату
    print(f"Знайдені прості числа: {process_primes}")
