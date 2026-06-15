import asyncio
import multiprocessing
import time
import math

# Вхідні дані згідно з ТЗ
NUMBERS = list(range(1, 11))


# =====================================================================
# 1. МАТЕМАТИЧНІ ФУНКЦІЇ (Базові алгоритми)
# =====================================================================

def calc_fibonacci(n: int) -> int:
    """Обчислення n-го числа Фібоначчі (ітеративно для швидкості)"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def calc_factorial(n: int) -> int:
    """Обчислення факторіала числа"""
    return math.factorial(n)


def calc_square(n: int) -> int:
    """Обчислення квадрата числа"""
    return n ** 2


def calc_cube(n: int) -> int:
    """Обчислення куба числа"""
    return n ** 3


# =====================================================================
# 2. АСИНХРОННА РЕАЛІЗАЦІЯ (Asyncio)
# =====================================================================

async def async_fib(n): return calc_fibonacci(n)


async def async_fact(n): return calc_factorial(n)


async def async_sq(n): return calc_square(n)


async def async_cube(n): return calc_cube(n)


async def run_asyncio_version():
    start_time = time.time()

    # Створюємо завдання для кожного числа зі списку
    fib_tasks = [async_fib(n) for n in NUMBERS]
    fact_tasks = [async_fact(n) for n in NUMBERS]
    square_tasks = [async_sq(n) for n in NUMBERS]
    cube_tasks = [async_cube(n) for n in NUMBERS]

    # Збираємо всі завдання в один загальний gather
    # Групуємо їх так, щоб отримати 4 окремі списки результатів
    fib_results = await asyncio.gather(*fib_tasks)
    fact_results = await asyncio.gather(*fact_tasks)
    square_results = await asyncio.gather(*square_tasks)
    cube_results = await asyncio.gather(*cube_tasks)

    duration = time.time() - start_time
    return (fib_results, fact_results, square_results, cube_results), duration


# =====================================================================
# 3. БАГАТОПРОЦЕСОРНА РЕАЛІЗАЦІЯ (Multiprocessing)
# =====================================================================

def run_multiprocessing_version():
    start_time = time.time()

    # Використовуємо пул процесів. Кількість процесів дорівнює кількості ядер CPU
    with multiprocessing.Pool() as pool:
        # map виконує функції паралельно на різних ядрах процесора
        fib_results = pool.map(calc_fibonacci, NUMBERS)
        fact_results = pool.map(calc_factorial, NUMBERS)
        square_results = pool.map(calc_square, NUMBERS)
        cube_results = pool.map(calc_cube, NUMBERS)

    duration = time.time() - start_time
    return (fib_results, fact_results, square_results, cube_results), duration


# =====================================================================
# ТОЧКА ВХОДУ ТА ПОРІВНЯННЯ
# =====================================================================
if __name__ == '__main__':
    print("--- Запуск обчислень для чисел від 1 до 10 ---\n")

    # 1. Тест Asyncio
    async_res, async_time = asyncio.run(run_asyncio_version())
    print(f"[Asyncio] Час виконання: {async_time:.6f} сек")

    # 2. Тест Multiprocessing
    mp_res, mp_time = run_multiprocessing_version()
    print(f"[Multiprocessing] Час виконання: {mp_time:.6f} сек\n")

    # Перевірка правильності результатів (чи збігаються вони)
    assert async_res == mp_res, "Помилка: Результати обчислень відрізняються!"

    # Вивід отриманих чотирьох списків
    print("Результати успішно отримано (всі 4 списки):")
    print(f"1. Спиок Фібоначчі: {mp_res[0]}")
    print(f"2. Список Факторіалів: {mp_res[1]}")
    print(f"3. Список Квадратів:   {mp_res[2]}")
    print(f"4. Список Кубів:       {mp_res[3]}")

    print(f"\nПереможець за швидкістю: {'Multiprocessing' if mp_time < async_time else 'Asyncio'}")
