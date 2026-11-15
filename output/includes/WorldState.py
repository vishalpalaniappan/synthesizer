import uuid
import json
from LoggingHelper import semanticLogger

class WorldState:
    '''
        This class will contain the world state of the design. It will
        assign a UID to each participant that is added and then it will
        return the value when requested or the UID + value.

        It wll also act as the boundary through which all world state
        transformations happen. This will then allow you to log all the
        information needed to understand how the design modifies the world
        state and the invariants that were violated.
    '''

    def __init__(self, mode):
        self.worldState = {}
        self.behavior = None
        self.mode = mode

    def setBehavior(self, behaviorName):
        self.behavior = behaviorName
        if self.mode == "verbose":
            semanticLogger.logBehavior(behaviorName)

worldStateManager = WorldState("verbose")