from src.interfaces.action import Action
from src.interfaces.executable_action import ExecutableAction


class ActionExecutorFactory:
    _executors = {}

    @classmethod
    def register(cls, action_type: type[Action], executor: type[ExecutableAction]):
        cls._executors[action_type] = executor

    @classmethod
    def get_executor(cls, action: Action) -> ExecutableAction:
        executor_cls = cls._executors[type(action)]
        return executor_cls(action)
