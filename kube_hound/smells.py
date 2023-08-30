from enum import Enum, auto


class Smell(Enum):
    IAC = auto()
    PAM = auto()
    UPM = auto()
    OCC = auto()
    NEDE = auto()
    HS = auto()
    NSC = auto()
    UT = auto()
    MUA = auto()
    CA = auto()
    UCP = auto()
    SCN = auto()
    def __repr__(self) -> str:
        return self.name
