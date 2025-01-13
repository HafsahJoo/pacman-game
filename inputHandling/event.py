#!/bin/python3
from dataclasses import dataclass


@dataclass
class EventDispatcher:
    """
    A class that handles events appropriately

    ---
    Attributes:
    ---

    - registered: a dictionary that holds the name of the events and then a list containing all the functions along with it.

    Methods:
    ---
    enroll(*args) -> None:

    - Register an event to the registered list

    associate(*args) -> None:

    - Emits an event and pass along any appropriate arguments
    """

    registered = dict()

    def enroll(self, eventType: str, function) -> None:
        """Assign the event to the registered list"""

        # Checks if the event is subscribed or not
        if eventType not in self.registered:
            # Add the function to the list of subscribers
            self.registered[eventType] = []
        # Append the function to the event
        self.registered[eventType].append(function)

    def associate(self, eventType: str, *args) -> None:
        """Post the event to the registered list"""

        # Does nothing if the event is not registered
        if eventType not in self.registered:
            return
        # Calls all the functions enrolled to that event
        for function in self.registered[eventType]:
            function(*args)
