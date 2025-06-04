from abc import ABC, abstractmethod

from pydantic import BaseModel

from .action import Action
from .percept import Percept


class Agent(BaseModel, ABC):
    """
    An abstract software agent class. The agent must be managed by the Simulation
    class
    """

    @abstractmethod
    def see(self, percept: Percept):
        """
        Provides a Percept to the agent. If the agent has internal state, this
        method should update it.
        """
        pass

    @abstractmethod
    def select_action(self) -> Action:
        """
        Have the agent select its next action to perform. In an agent with
        internal state, this implements the action: I -> A function.
        """
        pass
