from abc import ABC

from src.blackboard import Blackboard
from src.interfaces import Agent


class CommunicationAgent(Agent, ABC):
    blackboard: Blackboard
