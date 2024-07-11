import typing
import json
from . import varint

# Message protocol:
# 1. u8 specifying number of blobs
# 2. Varint specifying length of JSON data
# 3. One varint for each blob, specifying the length
# 4. JSON data
# 5. Blobs
def serialize_for_http(params: typing.Any, data: "list[bytes]") -> bytes:
    num_blobs_buf = len(data).to_bytes(1, "big")

    msg_buf = json.dumps(params).encode()
    msg_length_varint = varint.serialize_varuint64(len(msg_buf))

    final = [num_blobs_buf, msg_length_varint]

    for el in data:
        el_length_varint = varint.serialize_varuint64(len(el))
        final.append(el_length_varint)

    final.append(msg_buf)

    for el in data:
        final.append(el)

    return b''.join(final)

# Message protocol:
# 1. u32 id
# 2. u8 specifying number of blobs
# 3. Varint specifying length of JSON data
# 4. One varint for each blob, specifying the length
# 5. JSON data
# 6. Blobs
def serialize_for_websocket(id: int, message: typing.Any, data: "list[bytes]") -> bytes:
    id_buf = id.to_bytes(4, "big")

    num_blobs_buf = len(data).to_bytes(1, "big")

    msg_buf = json.dumps(message).encode()
    msg_length_varint = varint.serialize_varuint64(len(msg_buf))

    final = [id_buf, num_blobs_buf, msg_length_varint]
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
# 3. Varint encoding length of next blob
# 4. Next blob
def deserialize_for_http(data: bytes) -> "typing.Tuple[typing.Any, list[bytes]]":
    length, v_length = varint.deserialize_varuint64(data)

    response = json.loads(data[v_length : v_length + length])

    blobs = []
    pos = v_length + length
    while pos < len(data):
        blob_length, blob_v_length = varint.deserialize_varuint64(data[pos : ])
        blobs.append(data[pos + blob_v_length : pos + blob_v_length + blob_length])
        pos += blob_v_length + blob_length

    return response, blobs

# Message protocol:
# 1. u8 literal 0 if result, 1 if event
# 2. If result: u32 id
# 3. Varint specifying length of JSON data
# 4. JSON data
# Repeated:
# 5. Varint encoding length of next blob
# 6. Next blob
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

    blobs = []
    pos = v_length + length
    while pos < len(data):
        blob_length, blob_v_length = varint.deserialize_varuint64(data[pos:])
        blobs.append(data[pos + blob_v_length : pos + blob_v_length + blob_length])
        pos += blob_v_length + blob_length

    if first == 0:
        # Response message
        return (id, parsed), None, blobs
    else:
        # Event message
        parsed["api"] = api
        return None, parsed, blobs
