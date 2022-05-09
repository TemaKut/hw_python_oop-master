from dataclasses import dataclass, field, asdict
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

    LEN_STEP: ClassVar[float] = field(default=0.65, init=False)
    M_IN_KM: ClassVar[int] = field(default=1000, init=False)
    MPH: ClassVar[int] = field(default=60, init=False)
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

    SPEED_MULTIPLIER_1: ClassVar[float] = 18
    SPEED_MINUS: ClassVar[float] = 20

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return ((self.SPEED_MULTIPLIER_1 * self.get_mean_speed()
                 - self.SPEED_MINUS)
                * self.weight / self.M_IN_KM * self.duration * self.MPH)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SW_COEFF_1: ClassVar[float] = 0.035
    SW_COEFF_2: ClassVar[float] = 2
    SW_COEFF_3: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.SW_COEFF_1 * self.weight
                 + (self.get_mean_speed() ** self.SW_COEFF_2 // self.height)
                 * self.SW_COEFF_3 * self.weight) * self.duration * self.MPH)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = field(default=1.38, init=False)
    SWM_COEFF_1: ClassVar[float] = 1.1
    SWM_COEFF_2: ClassVar[float] = 2
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWM_COEFF_1)
                * self.SWM_COEFF_2 * self.weight)


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
