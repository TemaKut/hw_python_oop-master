from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    message: ClassVar[str] = ('Тип тренировки: {}; '
                              'Длительность: {:.3f} ч.; '
                              'Дистанция: {:.3f} км; '
                              'Ср. скорость: {:.3f} км/ч; '
                              'Потрачено ккал: {:.3f}.')
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Метод возврата результата тренировки."""
        return self.message.format(*asdict(self).values())


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    SPEED_MULTIPLIER: ClassVar[float] = 18
    SPEED_MINUS: ClassVar[float] = 20

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return ((self.SPEED_MULTIPLIER * self.get_mean_speed()
                - self.SPEED_MINUS)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SW_MULTIPLIER_1: ClassVar[float] = 0.035
    SW_DEGREE: ClassVar[float] = 2
    SW_MULTIPLIER_2: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.SW_MULTIPLIER_1 * self.weight
                + (self.get_mean_speed() ** self.SW_DEGREE // self.height)
                * self.SW_MULTIPLIER_2 * self.weight)
                * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    SWM_SUMM: ClassVar[float] = 1.1
    SWM_MULTIPLIER: ClassVar[float] = 2
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWM_SUMM)
                * self.SWM_MULTIPLIER * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        training_dict = {
            'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking,
        }

        return training_dict.get(workout_type)(*data)

    except TypeError:
        print('Такой тренировки нет.')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
