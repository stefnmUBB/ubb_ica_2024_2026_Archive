from abc import ABC

from pydantic import BaseModel


class Action(BaseModel, ABC):
    """
    An abstract class for actions in an agent environment. Each type of
    Action should be a separate subclass.
    """
