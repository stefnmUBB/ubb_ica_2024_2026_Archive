from abc import ABC

from pydantic import BaseModel


class Percept(BaseModel, ABC):
    """
    An abstract class for things an agent can perceive. Since an
    agent only receives one Percept per turn, the Percept may
    incorporate the results of multiple sensors
    """

    pass
