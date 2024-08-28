from abc import ABC, abstractmethod

class Pizza(ABC):
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def price(self) -> float:
        pass

class RegPizza(Pizza):
    def description(self) -> None:
        return "Regular pizza"
    
    def price(self) -> float:
        return 9.99
    
class PizzaDecorator(Pizza, ABC):
    def __init__(self, pizza: Pizza) -> None:
        self._pizza = pizza

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def price(self) -> float:
        pass

class Pepperoni(PizzaDecorator):
    def description(self) -> str:
        return self._pizza.description() + " with extra pepperoni"
    
    def price(self) -> float:
        return self._pizza.price() + 2.99
    
class Cheese(PizzaDecorator):
    def description(self) -> str:
        return self._pizza.description() + " with extra cheese"
    
    def price(self) -> float:
        return self._pizza.price() + 1.99
    
if __name__ == "__main__":
    my_pizza = RegPizza()
    print(my_pizza.description() + " costs " + str(my_pizza.price()))

    my_pizza = Pepperoni(my_pizza)
    my_pizza = Cheese(my_pizza)
    print(my_pizza.description() + " costs " + str(my_pizza.price()))


    
    