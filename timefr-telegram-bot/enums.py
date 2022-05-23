from enum import Enum

class Direction(Enum):
    A = "A"
    R = "R"
    A_AND_R = "A+R"


class TransportType(Enum):
    BUS = "BUS"
    METRO = "METRO"
    RER = "RER"
    TRAMWAY = "TRAMWAY"

    @classmethod
    def from_str(cls, label):
        if "bus" in label.lower():
            return cls.BUS
        elif "metro" in label.lower() or "métro" in label.lower():
            return cls.METRO
        elif "rer" in label.lower():
            return cls.RER
        elif "tramway" in label.lower():
            return cls.TRAMWAY
        else:
            raise NotImplementedError

class Action(Enum):
    ADD_TO_FAV = "ADD_TO_FAV"
