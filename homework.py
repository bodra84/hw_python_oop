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
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


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
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

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
    COEFF_CALOR_RUN_1: int = 18  # коэффициент №1 из формулы
    COEFF_CALOR_RUN_2: int = 20  # коэффициент №2 из формулы

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()  # расчет средней скорости
        duration_in_m = self.duration * self.H_IN_M  # длит. тренировки, в м.
        calor = self.COEFF_CALOR_RUN_1 * mean_speed - self.COEFF_CALOR_RUN_2

        return calor * self.weight / self.M_IN_KM * duration_in_m


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALOR_WALK_1: float = 0.035  # коэффициент №1 из формулы
    COEFF_CALOR_WALK_2: int = 2        # коэффициент №2 из формулы
    COEFF_CALOR_WALK_3: float = 0.029  # коэффициент №3 из формулы

    def __init__(self,
                 action: int,      # кол-во совершённых действий (шагов).
                 duration: float,  # длительность тренировки, в ч.
                 weight: float,    # вес спортсмена, в кг.
                 height: float     # рост спортсмена, в см.
                 ) -> None:

        super().__init__(action,
                         duration,
                         weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        mean_speed = self.get_mean_speed()           # расчет средней скорости
        duration_in_m = self.duration * self.H_IN_M  # длит. тренировки, в м.
        return (self.COEFF_CALOR_WALK_1
                * self.weight
                + (mean_speed ** self.COEFF_CALOR_WALK_2 // self.height)
                * self.COEFF_CALOR_WALK_3 * self.weight) * duration_in_m


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38               # расстояние за 1 гребок в м.
    COEFF_CALOR_SWIM_1: float = 1.1    # коэффициент №1
    COEFF_CALOR_SWIM_2: int = 2        # коэффициент №2

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
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        distance = self.length_pool * self.count_pool  # расчет дистанции, в м.
        return distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        mean_speed = self.get_mean_speed()  # расчет средней скорости
        calor = mean_speed + self.COEFF_CALOR_SWIM_1
        return calor * self.COEFF_CALOR_SWIM_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking
                                                }
    if workout_type not in training_type:
        raise KeyError('Ошибка! Тип тренировки не определен!')
    else:
        return training_type.get(workout_type)(*data)


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
