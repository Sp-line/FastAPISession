from enum import StrEnum


class HallLimits:
    NAME_MAX: int = 30
    NAME_MIN: int = 1

    DESCRIPTION_REQ: bool = False


class HallTechType(StrEnum):
    STANDARD = "standard"
    IMAX = "imax"
    DX_4 = "4dx"
    VIP = "vip"
    SCREENX = "screenx"
    ONYX = "onyx"
