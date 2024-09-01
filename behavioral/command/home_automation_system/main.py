from abc import ABC, abstractmethod
from typing import List

# Command: interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass


##########################################################################################
# Receiver
class Thermostat:
    def __init__(self) -> None:
        self.temperature = 0

    def change_temperature(self, step: float):
        self.temperature += step
        print(f"Thermostat temperature is at {self.temperature}°C")


class Light:
    def __init__(self) -> None:
        self.status  = "OFF"
    
    def turn_on(self):
        if self.status == "OFF":
            self.status = "ON"
        print("The light is on!")
    
    def turn_off(self):
        if self.status == "ON":
            self.status = "OFF"
        print("The light is off!")


class Fan:
    def __init__(self) -> None:
        self.status  = "OFF"
    
    def turn_on(self):
        if self.status == "OFF":
            self.status = "ON"
        print("The fan is on!")
    
    def turn_off(self):
        if self.status == "ON":
            self.status = "OFF"
        print("The fan is off!")


##########################################################################################
# Command: concrete implementation

# Thermostat
class ThermostatCommand(Command):
    def __init__(self, receiver: Thermostat, step: float) -> None:
        if step <= 0:
            raise ValueError("Please provide a positive number for the step")
        self.receiver = receiver
        self.step = step


class IncreaseThermostatTemp(ThermostatCommand):
    def execute(self):
        self.receiver.change_temperature(self.step)
    
    def undo(self):
        self.receiver.change_temperature(-self.step)


class DecreaseThermostatTemp(ThermostatCommand):    
    def execute(self):
        self.receiver.change_temperature(-self.step)
    
    def undo(self):
        self.receiver.change_temperature(self.step)


 # Light
class LightCommand(Command):
    def __init__(self, receiver: Light) -> None:
        self.receiver = receiver


class TurnOnLight(LightCommand):
    def execute(self):
        self.receiver.turn_on()

    def undo(self):
        self.receiver.turn_off()


class TurnOffLight(LightCommand):
    def execute(self):
        self.receiver.turn_off()

    def undo(self):
        self.receiver.turn_on()


# Fan
class FanCommand(Command):
    def __init__(self, receiver: Fan) -> None:
        self.receiver = receiver


class TurnOnFan(FanCommand):
    def execute(self):
        self.receiver.turn_on()

    def undo(self):
        self.receiver.turn_off()


class TurnOffFan(FanCommand):
    def execute(self):
        self.receiver.turn_off()

    def undo(self):
        self.receiver.turn_on()


##########################################################################################
# Invoker
class Remote:
    def __init__(self) -> None:
        self.command = None
        self.execute_history: List[Command] = []
        self.undo_history: List[Command] = []
    
    # Once the command is changed, it won't be possible to undo or redo previous commands
    def set_command(self, command: Command):
        self.command = command

    # When a command is executed, it will be added to the execution history to make undo possible
    def execute_command(self):
        self.command.execute()
        self.execute_history.append(self.command)
        self.undo_history.clear()

    # Once a command is undone, it will be added to the undo history to make redo possible.
    # It will also be removed from the execution history to prevent undoing the same command that has been once undone.
    def undo_command(self):
        if len(self.execute_history) == 0:
            print("There is no command to undo!")
        else:
            last_executed_command = self.execute_history[-1]
            last_executed_command.undo()
            self.undo_history.append(last_executed_command)
            self.execute_history.pop(-1)

    # Once a command is redone, it will be added to the exection history to make undo possible again.
    # It will also be removed from the undo history to prevent redoing the same command that has been once redone.
    def redo_command(self):
        if len(self.undo_history) == 0:
            print("There is no command to redo!")
        else:
            last_undone_command = self.undo_history[-1]
            last_undone_command.execute()
            self.execute_history.append(last_undone_command)
            self.undo_history.pop(-1)


##########################################################################################
# Client
if __name__ == "__main__":
    thermostat = Thermostat()
    light = Light()
    fan = Fan()
    remote = Remote()

    remote.set_command(IncreaseThermostatTemp(thermostat, 5)) # temp: 0 degrees, execute_history = [], undo_history = []
    remote.execute_command() # temp: 5°C, execute_history = [+5], undo_history = []
    remote.execute_command() # temp: 10°C, execute_history = [+5, +5], undo_history = []
    remote.undo_command() # temp: 5°C, execute_history = [+5], undo_history = [+5]
    remote.redo_command() # temp: 10°C, execute_history = [+5, +5], undo_history = []
    remote.redo_command() # temp: 10°C, execute_history = [+5, +5], undo_history = [] ==> No redo: undo_history is empty.

    remote.set_command(TurnOnLight(light)) # light: OFF, execute_history = [+5, +5], undo_history = []
    remote.execute_command() # light: ON, execute_history = [+5, +5, lightON], undo_history = []
    remote.undo_command() # light: OFF, execute_history = [+5, +5], undo_history = [lightON]
    remote.undo_command() # light: OFF, temp: 5°C, execute_history = [+5], undo_history = [lightON, +5]

    remote.set_command(TurnOnFan(fan))
    remote.execute_command() # fan: ON, execute_history = [+5, fanON], undo_history = []
    remote.undo_command() # fan: OFF, execute_history = [+5], undo_history = [fanON]
    remote.redo_command() # fan: ON, execute_history = [+5, fanON], undo_history = []

    remote.set_command(TurnOffFan(fan))
    remote.execute_command() # fan: OFF, execute_history = [+5, fanON, fanOFF], undo_history = []
