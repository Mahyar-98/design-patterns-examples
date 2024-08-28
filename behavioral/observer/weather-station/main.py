from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float) -> None:
        pass

class Subject:
    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, temperature: float) -> None:
        for observer in self._observers:
            observer.update(temperature)

class WeatherStation(Subject):
    def __init__(self) -> None:
        super().__init__()
        self._temperature = 0.0

    @property
    def temperature(self) -> float:
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float) -> None:
        self._temperature = value
        self.notify(self._temperature)

class LaptopDisplay(Observer):
    def update(self, temperature: float) -> None:
        print(f"Laptop display: The temperature is {temperature}°C")

class PhoneDisplay(Observer):
    def update(self, temperature: float) -> None:
        print(f"Phone display: The temperature is {temperature}°C")


if __name__ == "__main__":
    weather_station = WeatherStation()
    phone = PhoneDisplay()
    laptop = LaptopDisplay()

    weather_station.attach(phone)
    weather_station.attach(laptop)

    weather_station.temperature = 27
    weather_station.temperature = 34

    weather_station.detach(laptop)
    weather_station.temperature = 13