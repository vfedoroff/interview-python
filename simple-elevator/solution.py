UP = 1
DOWN = 2
FLOOR_COUNT = 6

import time

class Elevator(object):
    def __init__(self, logic_delegate, starting_floor=1):
        self._current_floor = starting_floor
        self._history = [starting_floor]
        print ("%s..." % starting_floor)
        self._motor_direction = None
        self._logic_delegate = logic_delegate
        self._logic_delegate.callbacks = self.Callbacks(self)

    def call(self, floor, direction):
        self._logic_delegate.on_called(floor, direction)
 
    def select_floor(self, floor):
         self._logic_delegate.on_floor_selected(floor)

    def step(self):
        delta = 0
        if self._motor_direction == UP: delta = 1
        elif self._motor_direction == DOWN: delta = -1
        if delta:
            self._current_floor = self._current_floor + delta
            print("%s..." % self._current_floor)
            self._history.append(self._current_floor)
            self._logic_delegate.on_floor_changed()
        else:
            self._logic_delegate.on_ready()
            assert self._current_floor >= 1
            assert self._current_floor <= FLOOR_COUNT

    def run_until_stopped(self):
        self.step()
        while self._motor_direction is not None: self.step()

    def run_until_floor(self, floor):
        for _ in range(100):
            self.step()
            if self._current_floor == floor: break
            else: assert False

    @property
    def history(self):
        return self._history

    class Callbacks(object):
        def __init__(self, outer):
            self._outer = outer

        @property
        def current_floor(self):
            return self._outer._current_floor

        @property
        def motor_direction(self):
            return self._outer._motor_direction

        @motor_direction.setter
        def motor_direction(self, direction):
            self._outer._motor_direction = direction


class ElevatorLogic(object):
    """
    An incorrect implementation. Can you make it pass all the tests?

    Fix the methods below to implement the correct logic for elevators.
    The tests are integrated into `README.md`. To run the tests:
    $ python -m doctest -v README.md

    To learn when each method is called, read its docstring.
    To interact with the world, you can get the current floor from the
    `current_floor` property of the `callbacks` object, and you can move the
    elevator by setting the `motor_direction` property. See below for how this is done.
    """

    class Call(object):
        def __init__(self, floor, time):
            self.floor = floor
            self.time = time

        def __repr__(self):
            return "%d" % self.floor

    def __init__(self):
        # Feel free to add any instance variables you want.
        self.destination_floor = None
        self.callbacks = None
        self.orders = {}
        self.orders[UP] = []
        self.orders[DOWN] = []
        self.current_direction = None
        self.bounded_direction = None

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """

        if not self.valid_floor(floor) or direction not in [UP, DOWN]:
            return
        direction_to_floor = self.direction_to(floor)
        if self.current_direction is None:
            # Change direction
            self.current_direction = direction_to_floor

        if self.callbacks.current_floor != floor:
            self.index(direction, floor)
            # Reorder
            self.sort(UP)
            self.sort(DOWN)
            if self.current_direction == UP and self.orders[UP]:
                self.destination_floor = self.orders[UP][0].floor
            else:
                self.destination_floor = self.orders[direction][0].floor
        else:
            # Missed the boat, come back later
            self.index(self.other_direction(self.current_direction), floor)

        # print "direction to floor: ", self.direction_str(direction_to_floor)
        self.log("on called")

    def index(self, direction, floor):
        if not direction:
            return
        self.orders[direction].insert(0, self.Call(floor, time.time()))

    def sort(self, direction):
        if direction == UP:
            if self.callbacks.motor_direction:
                self.orders[UP].sort(key=lambda x: x.floor)
            elif all(x.floor > self.callbacks.current_floor for x in self.orders[UP]):
                self.orders[UP].sort(key=lambda x: x.floor)
            else:
                self.orders[UP].sort(key=lambda x: x.time)
        elif direction == DOWN:
            self.orders[DOWN].sort(key=lambda x: x.time, reverse=True)
        else:
            pass

    @staticmethod
    def valid_floor(floor):
        return floor >= 1 or floor <= FLOOR_COUNT

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """

        if not self.valid_floor(floor):
            return


        direction_to_floor = self.direction_to(floor)

        if direction_to_floor is None:
            self.log("missed the boat")
            return

        # Check the other queue for duplicates
        other_direction = self.other_direction(direction_to_floor)
        if self.orders[other_direction]:
            _floor = self.orders[other_direction][0].floor
            if _floor == floor:
                # Serve that, but not this floor request (line 485)
                return

        if self.bounded_direction:
            self.log("floor selected. bounded direction detected. direction to floor %d: %s"
                     % (floor, self.direction_str(direction_to_floor))
                     )
            if direction_to_floor == self.bounded_direction:
                self.current_direction = self.bounded_direction
                self.bounded_direction = None
            else:
                self.log("floor selection ignored. Mismatch between bounded direction and direction to floor selected")
                # self.bounded_direction = None
                return

        if self.current_direction and self.current_direction != direction_to_floor:
            # Set it to wait for requests to move to the other direction
            other_direction = self.other_direction(self.current_direction)
            self.current_direction = other_direction
            self.log("""\
                     floor selection ignored.
                     floor selected: %d
                     Direction to floor: %s.
                     Must wait for requests to move to the other direction"""
                     % (floor, self.direction_str(direction_to_floor)))
            # Clear for the next call
            if self.callbacks.current_floor == self.destination_floor:
                self.log("Clear for the next call")
                # Reverse again
                other_direction = self.other_direction(other_direction)
                if self.orders[other_direction] and self.orders[other_direction][0].floor == self.callbacks.current_floor:
                    self.orders[other_direction].pop(0)
                self.current_direction = None
            return

        self.index(direction_to_floor, floor)

        # sort the list so closer floors are attended first
        # self.orders[direction_to_floor].sort()
        self.sort(direction_to_floor)

        if self.current_direction is None:
            self.current_direction = direction_to_floor

        self.destination_floor = self.orders[self.current_direction][0].floor

        self.log("on floor selected")

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """

        if self.destination_floor == self.callbacks.current_floor:
            self.log("on change. Destiny %d reached" % self.destination_floor)
            self.callbacks.motor_direction = None

            if self.current_direction and self.orders[self.current_direction]:
                self.orders[self.current_direction].pop(0)
            else:
                if self.current_direction and self.orders[self.other_direction(self.current_direction)]:
                    self.orders[self.other_direction(self.current_direction)].pop(0)  # something had to be served (

            if self.current_direction and self.orders[self.current_direction]:
                next_destination = self.orders[self.current_direction][0].floor
                if next_destination != self.callbacks.current_floor:
                    self.destination_floor = next_destination
                else:
                    self.orders[self.current_direction].pop(0)  # drop it, already there
                    self.destination_floor = None
                    self.bounded_direction = self.current_direction

            else:
                self.bounded_direction = self.current_direction

        if self.current_direction and not self.orders[self.current_direction]:
            other_direction = self.other_direction(self.current_direction)
            if other_direction and self.orders[other_direction]:
                self.current_direction = other_direction
                # Set the new target floor
                if self.orders[self.current_direction]:
                    self.destination_floor = self.orders[self.current_direction][0].floor

        if self.is_idle():
            self.current_direction = None  # Elevator is idle

        if self.callbacks.current_floor <= 1 and self.callbacks.motor_direction == DOWN:
            # self.callbacks.current_floor = 1
            self.callbacks.motor_direction = None
            self.current_direction = None
            self.bounded_direction = None

        if self.callbacks.motor_direction == UP and self.callbacks.current_floor == FLOOR_COUNT:
            self.callbacks.motor_direction = DOWN
            self.bounded_direction = None
            self.destination_floor = FLOOR_COUNT

        self.log("on_changed")

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """

        if self.destination_floor and not self.valid_floor(self.destination_floor):
            self.destination_floor = None
            self.callbacks.motor_direction = None



        # print "on ready: dest floor: %d" % self.destination_floor
        if self.destination_floor > self.callbacks.current_floor:
            self.callbacks.motor_direction = UP
        elif self.destination_floor < self.callbacks.current_floor:
            self.callbacks.motor_direction = DOWN
        else:
            self.bounded_direction = None

        if self.callbacks.motor_direction == DOWN and self.callbacks.current_floor == 1:
            self.callbacks.motor_direction = None

        if self.callbacks.motor_direction == UP and self.callbacks.current_floor == FLOOR_COUNT:
            self.callbacks.motor_direction = None
            self.bounded_direction = None
            self.destination_floor = None


        self.log("on ready")

    def direction_to(self, floor):
        direction = None
        if floor > self.callbacks.current_floor:
            direction = UP
        elif floor < self.callbacks.current_floor:
            direction = DOWN
        return direction

    def is_idle(self):
        return not self.orders[UP] and not self.orders[DOWN]

    @staticmethod
    def other_direction(direction):
        if UP == direction:
            return DOWN
        if DOWN == direction:
            return UP
        return None

    @staticmethod
    def direction_str(direction):
        if UP == direction:
            return "UP"
        elif DOWN == direction:
            return "DOWN"
        else:
            return "None"

    def status(self):
        return """\
   Current direction: %s
   Current floor: %s
   Destination floor: %s
   Bounded direction: %s
   orders UP: %s
   orders DOWN: %s
               """ % (self.direction_str(self.current_direction),
                      self.callbacks.current_floor,
                      self.destination_floor,
                      self.direction_str(self.bounded_direction),
                      self.orders[UP],
                      self.orders[DOWN])

    def log(self, msg):
        # print "%s. \nstatus:\n%s" % (msg, self.status())
        pass

if __name__ == "__main__":
    e = Elevator(ElevatorLogic())
    e.call(5, DOWN)
    e.run_until_stopped()
    e.select_floor(1)
    e.call(3, DOWN)
    e.run_until_stopped()
    e.run_until_stopped()
    assert e.history == [1, 2, 3, 4, 5, 4, 3, 2, 1]
    print("------")
    """
    Elevators want to keep going in the same direction. An elevator will serve as many requests in one direction as it can before going the other way. For example, if an elevator is going up, it won't stop to pick up passengers who want to go down until it's done with everything that requires it to go up.
    """
    e = Elevator(ElevatorLogic())
    e.call(2, DOWN)
    e.select_floor(5)
    e.run_until_stopped()
    e.run_until_stopped()
    assert e.history == [1, 2, 3, 4, 5, 4, 3, 2]
    print("------")
    """
    In fact, if a passenger tries to select a floor that contradicts the current direction of the elevator, that selection is ignored entirely. You've probably seen this before. You call the elevator to go down. The elevator shows up, and you board, not realizing that it's still going up. You select a lower floor. The elevator ignores you.
    """
    # e = Elevator(ElevatorLogic())
    # e.select_floor(3)
    # e.select_floor(5)
    # e.run_until_stopped()
    # e.select_floor(2)
    # e.run_until_stopped()
    # e.run_until_stopped()  # nothing happens, because e.select_floor(2) was ignored
    # e.select_floor(2)
    # e.run_until_stopped()
    # print("------")    
    # """
    # The process of switching directions is a bit tricky. Normally, if an elevator going up stops at a floor and there are no more requests at higher floors, the elevator is free to switch directions right away. However, if the elevator was called to that floor by a user indicating that she wants to go up, the elevator is bound to consider itself going up.
    # """
    # e = Elevator(ElevatorLogic())
    # e.call(2, DOWN)
    # e.call(4, UP)
    # e.run_until_stopped()
    # e.select_floor(5)
    # e.run_until_stopped()
    # e.run_until_stopped()
    # print("------")    
    # """
    # If nobody wants to go further up though, the elevator can turn around.
    # """
    # e = Elevator(ElevatorLogic())
    # e.call(2, DOWN)
    # e.call(4, UP)
    # e.run_until_stopped()
    # e.run_until_stopped()
    # print("------")    
    # """
    # If the elevator is called in both directions at that floor, it must wait once for each direction. You may have seen this too. Some elevators will close their doors and reopen them to indicate that they have changed direction.
    # """
    # e = Elevator(ElevatorLogic())
    # e.select_floor(5)
    # e.call(5, UP)
    # e.call(5, DOWN)
    # e.run_until_stopped()
    # """
    # Here, the elevator considers itself to be going up, as it favors continuing in the direction it came from.
    # """
    # e.select_floor(4)  # ignored
    # e.run_until_stopped()
    # """
    # Since nothing caused the elevator to move further up, it now waits for requests that cause it to move down.
    # """
    # e.select_floor(6)  # ignored
    # e.run_until_stopped()   
    # """
    # Since nothing caused the elevator to move down, the elevator now considers itself idle. It can move in either direction.
    # """ 
    # e.select_floor(6)
    # e.run_until_stopped()    
    # print("------")
    # """
    # Keep in mind that a user could call the elevator or select a floor at any time. The elevator need not be stopped. If the elevator is called or a floor is selected before it has reached the floor in question, then the request should be serviced.
    # """
    # e = Elevator(ElevatorLogic())
    # e.select_floor(6)
    # e.run_until_floor(2)  # elevator is not stopped
    # e.select_floor(3)
    # e.run_until_stopped()  # stops for above
    # e.run_until_floor(4)
    # e.call(5, UP)
    # e.run_until_stopped()  # stops for above
    # """
    # On the other hand, if the elevator is already at, or has passed the floor in question, then the request should be treated like a request in the wrong direction. That is to say, a call is serviced later, and a floor selection is ignored.
    # """
    # e = Elevator(ElevatorLogic())
    # e.select_floor(5)
    # e.run_until_floor(2)
    # e.call(2, UP)  # missed the boat, come back later
    # e.step()  # doesn't stop
    # e.select_floor(3)  # missed the boat, ignored
    # e.step()  # doesn't stop
    # e.run_until_stopped()  # service e.select_floor(5)
    # e.run_until_stopped()  # service e.call(2, UP)
    # """
    # No amount of legal moves should compel the elevator to enter an illegal state. Here, we run a bunch of random requests against the simulator to make sure that no asserts are triggered.
    # """
    # import random
    # e = Elevator(ElevatorLogic())
    # try:
    #     print("-")
    # finally:
    #     for i in range(100000):  
    #         r = random.randrange(6)
    #         if r == 0: e.call(
    #             random.randrange(FLOOR_COUNT) + 1,
    #             random.choice((UP, DOWN)))
    #         elif r == 1: e.select_floor(random.randrange(FLOOR_COUNT) + 1)
    #     else: e.step()   
    # """
    # An elevator is called but nobody boards. It goes idle.
    # """
    # e = Elevator(ElevatorLogic())
    # e.call(5, UP)
    # e.run_until_stopped()
    # e.run_until_stopped()
    # e.run_until_stopped()
    # """
    # The elevator is called at two different floors.
    # """
    # e = Elevator(ElevatorLogic())
    # e.call(3, UP)
    # e.call(5, UP)
    # e.run_until_stopped()
    # e.run_until_stopped()
    # """
    # Like above, but called in reverse order.
    # """
    # e = Elevator(ElevatorLogic())
    # e.call(5, UP)
    # e.call(3, UP)
    # e.run_until_stopped()
    # e.run_until_stopped()
    # """
    # The elevator is called at two different floors, but going the other direction.
    # """
    # e = Elevator(ElevatorLogic())
    # e.call(3, DOWN)
    # e.call(5, DOWN)
    # e.run_until_stopped()
    # e.run_until_stopped()    
    # """
    # The elevator is called at two different floors, going in opposite directions.
    # """
    # e = Elevator(ElevatorLogic())
    # e.call(3, UP)
    # e.call(5, DOWN)
    # e.run_until_stopped()
    # e.run_until_stopped()
