"""
Action: Deals with different actions
"""

import abc


@abc.abstractclassmethod
class Action:
    """Represent a single action that can be done in a turn"""
    @abc.abstractmethod
    def perform(self, entity):
        """The action to perform"""
        return
