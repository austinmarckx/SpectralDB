
import logging
logger = logging.getLogger(__name__)
from typing import Literal, Optional

from utils.types import Timestamp

LOGGING_LEVELS_R = {"NOTSET":0, "DEBUG":10, "INFO":20, "WARNING":30, "ERROR":40, "CRITICAL":50}
LOGGING_LEVELS = {v:k for k, v in LOGGING_LEVELS_R.items()}
#LogLevel = Literal[logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
LogLevel = Literal[0,10,20,30,40,50]

class Log: 
    @classmethod
    def log(cls, message:str, lvl:LogLevel=20, exc_info:Optional['logging._ExcInfoType']=None, console:bool=True, prefix:bool=True, time:bool=False, **kwargs):
        lvl = cls.parse_level(lvl)
        if prefix:
            message = cls.getprefix(lvl, time) + message
        
        logger.log(lvl, message, exc_info=exc_info)
        if console:
            print(message)
    
    @classmethod
    def getprefix(cls, lvl:LogLevel, time:bool=False):
        """  `[lvl] timestamp:` message"""
        level = f"[{cls.parse_level(lvl, 'str')}]" 
        time = cls.get_time() if time else "now"
        suffix = " "
        return ":".join([time, lvl, suffix])

    @classmethod
    def parse_level(cls, lvl:LogLevel, out:Literal["int", "str"]="int"):
        if out == "int":
            return LOGGING_LEVELS_R.get(lvl, lvl)
        elif out == "str":
            return LOGGING_LEVELS.get(lvl, lvl)
        else:
            raise ValueError(out)

    @classmethod
    def get_time(cls):
        return Timestamp.encode()