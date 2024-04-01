import typing
import json
from . import varint

# Message protocol:
# 1. u8 specifying number of additional data segments
# 2. Varint specifying length of JSON data
# 3. One varint for each data segment, specifying the length of data segment
# 4. JSON data
# 5. Data segments
def serialize_for_http(params: typing.Any, data: "list[bytes]") -> bytes:
    num_additional_segments_buf = len(data).to_bytes(1, "big")

    msg_buf = json.dumps(params).encode()
    msg_length_varint = varint.serialize_varuint64(len(msg_buf))

    final = [num_additional_segments_buf, msg_length_varint]

    for el in data:
        el_length_varint = varint.serialize_varuint64(len(el))
        final.append(el_length_varint)

    final.append(msg_buf)

    for el in data:
        final.append(el)

    return b''.join(final)

# Message protocol:
# 1. u32 id
# 2. u8 specifying number of additional data segments
# 3. Varint specifying length of JSON data
# 4. One varint for each data segment, specifying the length of data segment
# 5. JSON data
# 6. Data segments
def serialize_for_websocket(id: int, message: typing.Any, data: "list[bytes]") -> bytes:
    id_buf = id.to_bytes(4, "big")

    num_additional_segments_buf = len(data).to_bytes(1, "big")

    msg_buf = json.dumps(message).encode()
    msg_length_varint = varint.serialize_varuint64(len(msg_buf))

    final = [id_buf, num_additional_segments_buf, msg_length_varint]
    for el in data:
        el_length_varint = varint.serialize_varuint64(len(el))
        final.append(el_length_varint)

    final.append(msg_buf)
    final.extend(data)

    return b''.join(final)

# Message protocol:
# 1. Varint specifying length of JSON data
# 2. JSON data
# Repeated:
# 3. Varint encoding length of next data segment
# 4. next data segment
def deserialize_for_http(data: bytes) -> "typing.Tuple[typing.Any, list[bytes]]":
    length, v_length = varint.deserialize_varuint64(data)

    response = json.loads(data[v_length : v_length + length])

    data_segments = []
    pos = v_length + length
    while pos < len(data):
        segment_length, segment_v_length = varint.deserialize_varuint64(data[pos : ])
        data_segments.append(data[pos + segment_v_length : pos + segment_v_length + segment_length])
        pos += segment_v_length + segment_length

    return response, data_segments

# Message protocol:
# 1. u8 literal 0 if result, 1 if event
# 2. If result: u32 id
# 3. Varint specifying length of JSON data
# 4. JSON data
# Repeated:
# 5. Varint encoding length of next data segment
# 6. next data segment
def deserialize_for_ws(data: bytes) -> "typing.Tuple[typing.Tuple[int, typing.Any] | None, typing.Any | None, list[bytes]]":
    first = data[0]
    if first == 0:
        # Response message
        id = int.from_bytes(data[1:5], 'big')
        api = None
        data = data[5:]
    else:
        # Event message
        id = 0
        api_len = data[1]
        api = data[2 : 2 + api_len].decode()
        data = data[2 + api_len :]

    length, v_length = varint.deserialize_varuint64(data)

    parsed = json.loads(data[v_length : v_length + length])

    data_segments = []
    pos = v_length + length
    while pos < len(data):
        segment_length, segment_v_length = varint.deserialize_varuint64(data[pos:])
        data_segments.append(data[pos + segment_v_length : pos + segment_v_length + segment_length])
        pos += segment_v_length + segment_length

    if first == 0:
        # Response message
        return (id, parsed), None, data_segments
    else:
        # Event message
        parsed["api"] = api
        return None, parsed, data_segments
