from abc import ABC

from pydantic import BaseModel


class State(BaseModel, ABC):
    """
    A complete representation of a situation in the agent environment.
    Since this is very domain specific, few methods are given.
    However, there should be methods for updating and retrieving various
    aspects of the state.
    """

    def step(self):
        """
        Advances the state by one step.
        """
        return
