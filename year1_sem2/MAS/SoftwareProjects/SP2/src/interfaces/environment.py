from abc import ABC, abstractmethod

from pydantic import BaseModel

from .action import Action
from .agent import Agent
from .percept import Percept
from .state import State


class Environment(BaseModel, ABC):
    """
    This can be used for either single or multi-agent environments.
    """

    state: State

    @abstractmethod
    def get_percept(self, agent: Agent) -> Percept:
        """
        Creates a percept for an agent. This should implement the
        see: S -> P function.
        """
        pass

    @abstractmethod
    def update_state(self, agent: Agent, action: Action) -> None:
        """
        Executes an agent's action and update the environment's state. This
        implements the env: S x A -> S function.
        """
        pass

    def step(self) -> None:
        """
        Advances the environment by one step.
        """
        return
