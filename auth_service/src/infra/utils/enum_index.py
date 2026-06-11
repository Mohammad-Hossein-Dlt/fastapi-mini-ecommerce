from enum import Enum

def get_index(
    enum: type[Enum],
    value,
) -> int | None:

    for i, v in enumerate(enum):
        if v == value:
            return i
    
    return None

def get_value_by_index(
    enum: type[Enum],
    index: int,
):

    for i, v in enumerate(enum):
        if i == index:
            return v
    
    return None

def get_value_by_name(
    enum: type[Enum],
    index: int,
):

    for i, v in enumerate(enum):
        if i == index:
            return v
    
    return None