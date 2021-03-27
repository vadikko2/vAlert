from random import random
from typing import List
from constants import FREQUENCY_LIST


def get_distribution(frequencies: List[float]) -> List[float]:
    dist = [0]
    for freq in frequencies:
        dist.append(dist[-1] + freq)
    return dist


def get_index(r: float, dist: List[float]) -> int:
    for i, freq in enumerate(dist[1:]):
        if r < freq:
            return i


if __name__ == '__main__':
    # Строим распределение
    distribution = get_distribution([freq for _, freq in FREQUENCY_LIST])
    print('Frequencies: ', dict(FREQUENCY_LIST))
    print('distribution: ', distribution)

    # Собираем статистику для проверки алгоритма (должна сойтись с нашими вероятностями)
    res_dict = {key: 0 for key, _ in FREQUENCY_LIST}

    # Делаем много экспериментов
    examples = 1000000

    for _ in range(examples):
        r_ = random()
        key = FREQUENCY_LIST[get_index(r_, distribution)][0]
        res_dict[key] += 1

    # считаем вероятности
    res_dict = {key: value / examples for key, value in res_dict.items()}
    print('Result statistic:', res_dict)
