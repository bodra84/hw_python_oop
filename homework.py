"""Модуль фитнес-трекера."""

from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,  # имя класса тренировки
                 duration: float,  # длительность тренировки в часах
                 distance: float,  # дистанция в километрах
                 speed: float,  # средняя скорость пользователя
                 calories: float  # кол-во израсходованных килокал.
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> None:
        type = f'Тип тренировки: {self.training_type}; '
        time = f'Длительность: {self.duration:.3f} ч.; '
        dist = f'Дистанция: {self.distance:.3f} км; '
        spd = f'Ср. скорость: {self.speed:.3f} км/ч; '
        clr = f'Потрачено ккал: {self.calories:.3f}.'
        return(type + time + dist + spd + clr)


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # константа для перевода м. в км.
    H_IN_M: int = 60  # константа для перевода ч. в мин.
    LEN_STEP: float = 0.65  # расстояние за 1 шаг в м.

    def __init__(self,
                 action: int,  # кол-во совершённых действий (шагов/гребков).
                 duration: float,  # длительность тренировки, в ч.
                 weight: float  # вес спортсмена, в кг.
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__  # имя класса тренировки
        duration = self.duration                 # длительность тренировки в ч.
        distance = self.get_distance()           # дистанция в километрах
        speed = self.get_mean_speed()            # средняя скорость
        calories = self.get_spent_calories()     # количество килокалорий
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_run_1: int = 18  # коэффициент №1 из формулы
        coeff_calorie_run_2: int = 20  # коэффициент №2 из формулы
        mean_speed = self.get_mean_speed()  # расчет средней скорости
        duration_in_m = self.duration * self.H_IN_M  # длит. тренировки, в м.
        calor = coeff_calorie_run_1 * mean_speed - coeff_calorie_run_2
        return calor * self.weight / self.M_IN_KM * duration_in_m


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,      # кол-во совершённых действий (шагов).
                 duration: float,  # длительность тренировки, в ч.
                 weight: float,    # вес спортсмена, в кг.
                 height: float     # рост спортсмена, в см.
                 ) -> None:

        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_walk_1: float = 0.035  # коэффициент №1 из формулы
        coeff_calorie_walk_2: int = 2        # коэффициент №2 из формулы
        coeff_calorie_walk_3: float = 0.029  # коэффициент №3 из формулы

        mean_speed = self.get_mean_speed()           # расчет средней скорости
        duration_in_m = self.duration * self.H_IN_M  # длит. тренировки, в м.
        return (coeff_calorie_walk_1
                * self.weight
                + (mean_speed ** coeff_calorie_walk_2 // self.height)
                * coeff_calorie_walk_3 * self.weight) * duration_in_m


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,        # кол-во совершённых действий (шагов).
                 duration: float,    # длительность тренировки, в ч.
                 weight: float,      # вес спортсмена, в кг.
                 length_pool: int,   # длина бассейна в м.
                 count_pool: int     # сколько раз переплыл бассейн.
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        distance = self.length_pool * self.count_pool  # расчет дистанции, в м.
        return distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_swim_1: float = 1.1       # коэффициент №1
        coeff_calorie_swim_2: int = 2           # коэффициент №2

        mean_speed = self.get_mean_speed()  # расчет средней скорости
        calor = (mean_speed + coeff_calorie_swim_1) * coeff_calorie_swim_2
        return calor * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking
                                                }
    try:
        if workout_type in training_type:
            return training_type.get(workout_type)(*data)
    except AttributeError:
        return print("Тип тренировки не определен")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """Имитация получения данных от блока датчиков фитнес-трекера."""

    packages = [  # список смоделированных пакетов тренировок
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        # передача в функцию read_package
        training = read_package(workout_type, data)
        main(training)  # вызов главной функции main
