import logging
from pathlib import Path
from clp_logging.handlers import ClpKeyValuePairStreamHandler

import uuid

ADLI_EXECUTION_ID = str(uuid.uuid4())

parent = Path(__file__).resolve().parent.parent
(parent / "traces").mkdir(exist_ok=True)

path = parent / "traces" / f"{ADLI_EXECUTION_ID}.clp.zst"
clp_handler = ClpKeyValuePairStreamHandler(open(path, "wb"))
logger = logging.getLogger("semanticLogger")
logger.setLevel(logging.INFO)
logger.addHandler(clp_handler)

class LoggingHelper:
    '''
        This class holds all the logging functions used by the 
        instrumented code during runtime. 
    '''

    def logBehavior(self, behaviorId):
        entry = {}
        entry["type"] = "behavior"
        entry["behaviorName"] = behaviorId
        logger.info(entry)

semanticLogger = LoggingHelper()