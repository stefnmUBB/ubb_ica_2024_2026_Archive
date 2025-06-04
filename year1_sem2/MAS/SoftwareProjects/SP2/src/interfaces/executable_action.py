from abc import ABC, abstractmethod

from src.interfaces.agent import Agent
from src.interfaces.state import State

from src.interfaces.action import Action


class ExecutableAction(ABC):
    def __init__(self, action: Action):
        self.action = action

    @abstractmethod
    def execute(self, agent: Agent, state: State) -> State:
        """
        Update the state of the environment to reflect the effects of the
        agent performing the action. This implements the env: S x A -> S
        function. Note that in a multiagent environment, it is also
        important to know which agent is executing the action.
        """
        pass
