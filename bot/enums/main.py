from enum import Enum


class StatusEnum(Enum):
    process = "PROCESS"
    pending = "PENDING"
    accepted = "ACCEPTED"
    denied = "DENIED"