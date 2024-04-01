import typing

def get_varuint64_length(value: int) -> int:
    if value < 253:
        return 1
    elif value <= 2 ** 16:
        return 3
    elif value <= 2 ** 32:
        return 5
    else:
        return 9

def get_varuint64_length_from_bytes(data: bytes) -> int:
    first = int.from_bytes(data[0:1], 'big')
    if first < 253:
        return 1
    elif first == 253:
        return 3
    elif first == 254:
        return 5
    else:
        return 9

def serialize_varuint64(value: int) -> bytes:
    if value < 253:
        return value.to_bytes(1, 'big', signed=False)
    elif value <= 2 ** 16:
        return (253).to_bytes(1, 'big') + value.to_bytes(2, 'big', signed=False)
    elif value <= 2 ** 32:
        return (254).to_bytes(1, 'big') + value.to_bytes(4, 'big', signed=False)
    else:
        return (255).to_bytes(1, 'big') + value.to_bytes(8, 'big', signed=False)

def deserialize_varuint64(data: bytes) -> "typing.Tuple[int, int]":
    first = int.from_bytes(data[0:1], 'big')
    if first < 253:
        return (first, 1)
    elif first == 253:
        return (int.from_bytes(data[1:3], 'big'), 3)
    elif first == 254:
        return (int.from_bytes(data[1:5], 'big'), 5)
    else:
        return (int.from_bytes(data[1:9], 'big'), 9)
