"""
Elevator Control

You work for a company that likes to write all its own software... you've been given the task of writing the 
code to manage the elevators in HQ.

There is a single elevator serving 5 floors. Each floor has call buttons: up and down, except the top and 
bottom floor that have only single buttons. Inside the elevator there are also five buttons, which the passenger 
can use to choose their destination floor. The interface to the buttons is straightforward: you can read their 
on/ off state, and assign this same state. If you prefer to imagine that they invoke a callback method when 
pushed, that's also fine.

Please sketch out in pseudo- or real code an *algorithm* for running the elevator. Keep it simple.
"""

import enum


class Direction(enum.Enum):
    UP = 1
    DOWN = -1


class Lift:
    def __init__(self, floors=5):
        self.floor = 0
        self.destinations = [0] * floors
        self.directions = [None] * floors
        self.direction = 1

    def _correct_direction(self, floor):
        return (floor > self.floor and self.direction == 1) or (
            floor < self.floor and self.direction == -1
        )

    def _next_floor(self):
        def _appropriate_floors(all_destinations):
            destinations = [n for n, v in enumerate(all_destinations) if v]
            return [
                d
                for d in destinations
                if self._correct_direction(d)
                and (self.directions[d] is None or self.direction == self.directions[d])
            ]

        relevant_destinations = _appropriate_floors(self.destinations)
        if relevant_destinations:
            return relevant_destinations[0]
        else:
            self.direction = *-1
            relevant_destinations = _appropriate_floors(self.destinations)
            if relevant_destinations:
                return relevant_destinations[-1]

    def order(self, floor, direction):
        self.destinations[floor] = 1
        self.directions[floor] = direction

    def operate(self):
        if any(self.destinations):
            next_floor = self._next_floor()
            print(f"Heading to floor {next_floor}")
            self.floor = next_floor
            self.destinations[next_floor] = 0
            self.directions[next_floor] = None


class LiftManager:
    def __init__(self, floors):
        self.lift = Lift(floors)

    def order_inside(self, floor):
        self.lift.order(floor)

    def order_outside(self, floor, direction):
        self.lift.order(floor, direction)


if __name__ == "__main__":
    manager = LiftManager(5)
    manager.order_outside(3, Direction.UP)
    manager.order_outside(1, Direction.UP)
    manager.order_inside(4)
    manager.order_inside(4)
    manager.order_outside(4, Direction.DOWN)
    manager.order_outside(3, Direction.UP)
