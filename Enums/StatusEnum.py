from enum import Enum


class UavStatus(Enum):
    TIER_0=1
    TIER_1=2
    TIER_2=3
    WAIT=4

class HandStatus(Enum):
    TIER_0=1
    DEFENCE=0
    BACK=2
