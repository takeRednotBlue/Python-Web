"""
Напишіть реалізацію функції factorize, яка приймає список чисел та повертає список чисел, на які числа із вхідного списку поділяються без залишку.

Реалізуйте синхронну версію та виміряйте час виконання.
 
Потім покращіть продуктивність вашої функції, реалізувавши використання кількох ядер процесора для паралельних обчислень і заміряйте час
виконання знову. Для визначення кількості ядер на машині використовуйте функцію cpu_count() з пакета multiprocessing

Для перевірки правильності роботи алгоритму самої функції можете скористатися тестом:
"""

import time
from multiprocessing import Pool, current_process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import logging

# print(f"My laptop has {cpu_count()} cpu.")

# def factorize(*numbers: int) -> list[list[int]]:
# """
# Це синхронна функція яка виконує завдання послідовно.
# """
#     final_result = []
#     for number in numbers:
#         result = []
#         for i in range(1, number+1):
#             if number % i == 0:
#                 result.append(i)
#         final_result.append(result)
#     return final_result

def factorize_one_num(number: int) -> list[int]:
        """
        Функція яка обробляє кожне число окремо.
        """
        # logging.debug(f'Factorize {number}')
        print(f"pid={current_process().pid}, number={number}")
        result = []
        for i in range(1, number+1):
            if number % i == 0:
                result.append(i)
        return result
    
def factorize(*numbers: int) -> list[list[int]]:
    """
    Тут вже імплементована сама логіка багатопоточності
    """
    # Розділення задачі на процеси
    with Pool() as executor:
        final_result = list(executor.map(factorize_one_num, numbers))

    # Розділення задачі на потоки, використовував для порівняння часу роботи
    # logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     final_result = list(executor.map(factorize_one_num, numbers))
        
    return final_result


start = time.time()

# Великі числа потрібні для того щоб побачити як задіюються різні ядра.
# З тим прикладом що в домашці різниці між процесами та потоками майже немає.
# a, b  = factorize(646546556, 546546555)
a, b, c, d  = factorize(128, 255, 99999, 10651060)

finish = time.time()

print('Task was finished in {:2f} seconds.'.format(finish - start))

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

print('Everything is OK!')