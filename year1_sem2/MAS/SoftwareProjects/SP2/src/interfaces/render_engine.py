from abc import ABC

from .state import State


class RenderEngine(ABC):
    def display(self, state: State):
        """
        Displays information about the state. This may be as simple as
        text-based output, or could update a graphical display.
        """
        pass

    def stop(self):
        """
        Stops the render engine. This may be as simple as closing a window,
        or could involve more complex cleanup.
        """
        pass
