from enum import StrEnum


class HallLimits:
    CAPACITY_MIN = 0

    NAME_MAX: int = 30
    NAME_MIN: int = 1

    SLUG_MAX: int = 30
    SLUG_MIN: int = 1

    TECH_TYPE_MAX: int = 15

    DESCRIPTION_REQ: bool = False


class HallTechType(StrEnum):
    STANDARD = "standard"
    IMAX = "imax"
    DX_4 = "4dx"
    VIP = "vip"
    SCREENX = "screenx"
    ONYX = "onyx"
