from dataclasses import dataclass, field, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESS: str = ('Тип тренировки: {}; '
                 'Длительность: {:=.3f} ч.; '
                 'Дистанция: {:=.3f} км; '
                 'Ср. скорость: {:=.3f} км/ч; '
                 'Потрачено ккал: {:=.3f}.')

    def get_message(self) -> str:
        """Метод возврата результата тренировки."""

        return self.MESS.format(*asdict(self).values())


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: float = field(default=0.65, init=False)
    M_IN_KM: int = field(default=1000, init=False)
    MPH: int = field(default=60, init=False)

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

    RUN1: float = 18
    RUN2: float = 20

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""

        return ((self.RUN1 * self.get_mean_speed() - self.RUN2)
                * self.weight / self.M_IN_KM * self.duration * self.MPH)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    SW_COEFF_1: float = 0.035
    SW_COEFF_2: float = 2
    SW_COEFF_3: float = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.SW_COEFF_1 * self.weight
                 + (self.get_mean_speed() ** self.SW_COEFF_2 // self.height)
                 * self.SW_COEFF_3 * self.weight) * self.duration
                * self.MPH
                )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: float
    LEN_STEP: float = field(default=1.38, init=False)
    SWM1: float = 1.1
    SWM2: float = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWM1)
                * self.SWM2 * self.weight)


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
        ('WLK', [9000, 1, 75, 180],)
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
