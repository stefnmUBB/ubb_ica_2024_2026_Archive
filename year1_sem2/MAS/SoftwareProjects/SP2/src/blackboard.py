from multiprocessing import synchronize
from typing import Any
import multiprocessing

from pydantic import BaseModel, PrivateAttr


class Blackboard(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    _manager: multiprocessing.Manager = PrivateAttr()
    _queues: dict = PrivateAttr()
    _lock: multiprocessing.synchronize.Lock = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._manager = multiprocessing.Manager()
        self._queues = self._manager.dict()
        self._lock = self._manager.Lock()

    def _ensure_queue(self, key: str):
        with self._lock:
            if key not in self._queues:
                self._queues[key] = self._manager.list()

    def write(self, key: str, message: Any):
        self._ensure_queue(key)
        with self._lock:
            self._queues[key].append(message)

    def read(self, key: str):
        self._ensure_queue(key)
        with self._lock:
            if not self._queues[key]:
                return None
            return self._queues[key].pop(0)

    def read_all(self, key: str):
        self._ensure_queue(key)
        with self._lock:
            items = list(self._queues[key])
            self._queues[key].clear()
            return items
