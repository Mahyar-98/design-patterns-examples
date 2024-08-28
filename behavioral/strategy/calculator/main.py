from abc import ABC, abstractmethod

class OperationStrategy(ABC):
    @abstractmethod
    def evaluate(self, num1: float, num2:float) -> float:
        pass

class Addition(OperationStrategy):
    def evaluate(self, num1: float, num2: float) -> float:
        return num1 + num2
    
class Subtraction(OperationStrategy):
    def evaluate(self, num1: float, num2: float) -> float:
        return num1 - num2
    
class Multiplication(OperationStrategy):
    def evaluate(self, num1: float, num2: float) -> float:
        return num1 * num2
    
class Division(OperationStrategy):
    def evaluate(self, num1: float, num2: float) -> float:
        if num2 == 0:
            return None
        return num1 / num2
    
class OperationContext:
    def __init__(self, strategy: OperationStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: OperationStrategy):
        self._strategy = strategy

    def perform_operation(self, num1: float, num2: float):
        return self._strategy.evaluate(num1, num2)
    
if __name__ == "__main__":
    context = OperationContext(Addition())

    # add
    print(context.perform_operation(2, 4))

    # subtract
    context.set_strategy(Subtraction())
    print(context.perform_operation(7, 2))

    # multiply
    context.set_strategy(Multiplication())
    print(context.perform_operation(3, 4))

    # divide
    context.set_strategy(Division())
    print(context.perform_operation(6, 2))