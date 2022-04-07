from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TRAINING_TYPE: ClassVar[str] = 'Тип тренировки:'
    MESSAGE_DURATION: ClassVar[str] = ' Длительность:'
    MESSAGE_DISTANCE: ClassVar[str] = ' Дистанция:'
    MESSAGE_SPEED: ClassVar[str] = ' Ср. скорость:'
    MESSAGE_CALORIES: ClassVar[str] = ' Потрачено ккал:'

    def get_message(self) -> str:
        """Возврат строки сообщения."""
        return (f'{self.MESSAGE_TRAINING_TYPE} {self.training_type};'
                f'{self.MESSAGE_DURATION} {self.duration:.3f} ч.;'
                f'{self.MESSAGE_DISTANCE} {self.distance:.3f} км;'
                f'{self.MESSAGE_SPEED} {self.speed:.3f} км/ч;'
                f'{self.MESSAGE_CALORIES} { self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    M_IN_KM: ClassVar[float] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MINUTES_IN_HOUR: ClassVar[float] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance()) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'В классе {type(self).__name__} не'
                                  'реализован метод  get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: ClassVar[float] = 18
    COEFF_CALORIE_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight
                / self.M_IN_KM * self.duration
                * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        return (self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_2
                * self.weight) * self.duration * self.MINUTES_IN_HOUR


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        return ((self.get_mean_speed()
                + self.COEFF_CALORIE_1) * self.COEFF_CALORIE_2
                * self.weight)


SWM_CODE: str = 'SWM'
RUN_CODE: str = 'RUN'
WLK_CODE: str = 'WLK'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    parameters_dict: dict = {
        SWM_CODE: Swimming,
        RUN_CODE: Running,
        WLK_CODE: SportsWalking}
    if parameters_dict:
        return parameters_dict[workout_type](*data)
    else:
        raise ValueError(f'{workout_type} не'
                         f'соответствует значениям в {parameters_dict}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
