from enum import Enum


class UavStatus(Enum):

    TIER_0=1
    TIER_1=2
    TIER_2=3
    WAIT=4
    ON_WAY=5
    ON_ATTACK=6
    ON_BACK=7
    ON_TEMP_BACK=8
    DEAD=9


    def to_string(self):
        if self==self.ON_BACK:
            return "On back"
        elif self==self.TIER_1:
            return "TIER_1"
        elif self == self.TIER_2:
            return "TIER_2"
        elif self == self.WAIT:
            return "WAIT"
        elif self == self.ON_ATTACK:
            return "ON_ATTACK"
        elif self == self.ON_TEMP_BACK:
            return "On temp back"
        elif self ==self.DEAD:
            return "DEAD"
        else:
            return "Status nieznany"

class HandStatus(Enum):
    TIER_0=1
    DEFENCE=0
    BACK=2


class Sides(Enum):
    RIGHT=0
    LEFT=1
