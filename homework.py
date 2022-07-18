"""Модуль фитнес-трекера."""

class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str, # имя класса тренировки
                 duration: float,    # длительность тренировки в часах
                 distance: float,    # дистанция в километрах
                 speed: float,       # средняя скорость, с которой двигался пользователь
                 calories: float     # количество килокалорий, которое израсходовал пользователь
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        
    def get_message(self) -> None:
        return(f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000           # константа для перевода м. в км.
    H_IN_M: int = 60              # константа для перевода ч. в мин.
    LEN_STEP: float = 0.65        # расстояние за 1 шаг в м.

    def __init__(self,
                 action: int,     # кол-во совершённых действий (шагов/гребков).
                 duration: float, # длительность тренировки, в ч.
                 weight: float    # вес спортсмена, в кг.
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance 

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__  # имя класса тренировки
        duration = self.duration                 # длительность тренировки в часах
        distance = self.get_distance()           # дистанция в километрах
        speed= self.get_mean_speed()             # средняя скорость, с которой двигался пользователь
        calories =self.get_spent_calories()      # количество килокалорий, которое израсходовал пользователь
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
        
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_RUN_1: int = 18  # коэффициент №1 из формулы
        COEFF_CALORIE_RUN_2: int = 20  # коэффициент №2 из формулы

        spent_calories = (COEFF_CALORIE_RUN_1 
                          * self.get_mean_speed() 
                          - COEFF_CALORIE_RUN_2) * self.weight / self.M_IN_KM * self.duration * self.H_IN_M
        return spent_calories


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
        COEFF_CALORIE_WALK_1: float = 0.035          # коэффициент №1 из формулы
        COEFF_CALORIE_WALK_2: int = 2                # коэффициент №2 из формулы
        COEFF_CALORIE_WALK_3: float = 0.029          # коэффициент №3 из формулы
        
        mean_speed = self.get_mean_speed()           # расчет средней скорости
        duration_in_m = self.duration * self.H_IN_M  # длительность тренировки, в м.
        spent_calories = (COEFF_CALORIE_WALK_1 
                          * self.weight 
                          + ( mean_speed ** COEFF_CALORIE_WALK_2 // self.height) 
                          *  COEFF_CALORIE_WALK_3 * self.weight) * duration_in_m
        return spent_calories

class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38           # расстояние за 1 гребок в м.

    def __init__(self,
                 action: int,        # кол-во совершённых действий (шагов).
                 duration: float,    # длительность тренировки, в ч.
                 weight: float,      # вес спортсмена, в кг.
                 length_pool: int,   # длина бассейна в м.
                 count_pool: int     # сколько раз пользователь переплыл бассейн.
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        distance = self.length_pool * self.count_pool  # расчет дистанции, в м.
        mean_speed = distance / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_SWIM_1: float = 1.1       # коэффициент №1
        COEFF_CALORIE_SWIM_2: int = 2           # коэффициент №2
        
        mean_speed = self.get_mean_speed() # расчет средней скорости
        spent_calories = (mean_speed + COEFF_CALORIE_SWIM_1) * COEFF_CALORIE_SWIM_2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM' : Swimming,
                     'RUN' : Running,
                     'WLK' : SportsWalking
                    }
    if workout_type in training_type:
        return training_type.get(workout_type)(*data) 
        
def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    


if __name__ == '__main__':
    """Имитация получения данных от блока датчиков фитнес-трекера."""

    packages = [                     # список смоделированных пакетов тренировок
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data) # передача списка покатев в функцию read_package
        main(training)                              # вызов главной функции main
        #print(training.__class__.__name__)
        #print(training.action)
        #print(training.duration)     
# мой проверочный код
#SWM = Swimming(1000, 1, 75, 25, 40)
#RUN = Running(1000, 1, 75)
#WLK = SportsWalking(1000, 1, 75, 180)
#print(f'SWM кол-во {SWM.action}, длит {SWM.duration} , вес {SWM.weight}, длина {SWM.length_pool}, переплыл {SWM.count_pool}')
#print(f'SWM дистанция {SWM.get_distance()}, скорость {SWM.get_mean_speed()} , калории {SWM.get_spent_calories()}')
#print()
#print(f'RUN кол-во {RUN.action}, длит {RUN.duration} , вес {RUN.weight}')
#print(f'RUN дистанция {RUN.get_distance()}, скорость {RUN.get_mean_speed()} , калории {RUN.get_spent_calories()}')
#print()
#print(f'WLK кол-во {WLK.action}, длит {WLK.duration} , вес {WLK.weight}, рост {WLK.height}')
#print(f'WLK дистанция {WLK.get_distance()}, скорость {WLK.get_mean_speed()} , калории {WLK.get_spent_calories()}')
