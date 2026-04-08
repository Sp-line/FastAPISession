from enum import StrEnum, auto


class MovieDurables(StrEnum):
    SESSION_SVC_MOVIES_CREATED_SYNC_DB = auto()
    SESSION_SVC_MOVIES_BULK_CREATED_SYNC_DB = auto()
    SESSION_SVC_MOVIES_UPDATED_SYNC_DB = auto()