from enum import Enum


class UavStatus(Enum):

    TIER_0=1
    TIER_1=2
    TIER_2=3
    WAIT=4
    ON_WAY=5
    ON_ATTACK=6
    ON_BACK=7

class HandStatus(Enum):
    TIER_0=1
    DEFENCE=0
    BACK=2


class Sides(Enum):
    RIGHT=0
    LEFT=1
