import typing
import numpy as np

from . import varint

class DecthingsElementImage:
    def __init__(self, format: str, data: bytes):
        if not isinstance(format, str):
            raise ValueError("Invalid format: Expected a string.")
        if len(format.encode()) > 255:
            raise ValueError("The format must be no more than 255 bytes.")
        if not isinstance(data, bytes):
            raise ValueError("Invalid data: Expected bytes")

        self._format = format
        self._data = data

    def format(self) -> str:
        return self._format

    def data(self) -> bytes:
        return self._data

class DecthingsElementAudio:
    def __init__(self, format: str, data: bytes):
        if not isinstance(format, str):
            raise ValueError("Invalid format: Expected a string.")
        if len(format.encode()) > 255:
            raise ValueError("The format must be no more than 255 bytes.")
        if not isinstance(data, bytes):
            raise ValueError("Invalid data: Expected bytes")

        self._format = format
        self._data = data

    def format(self) -> str:
        return self._format

    def data(self) -> bytes:
        return self._data

class DecthingsElementVideo:
    def __init__(self, format: str, data: bytes):
        if not isinstance(format, str):
            raise ValueError("Invalid format: Expected a string.")
        if len(format.encode()) > 255:
            raise ValueError("The format must be no more than 255 bytes.")
        if not isinstance(data, bytes):
            raise ValueError("Invalid data: Expected bytes")

        self._format = format
        self._data = data

    def format(self) -> str:
        return self._format

    def data(self) -> bytes:
        return self._data

_type_specifiers = {
    "f32": 1,
    "f64": 2,
    "i8": 3,
    "i16": 4,
    "i32": 5,
    "i64": 6,
    "u8": 7,
    "u16": 8,
    "u32": 9,
    "u64": 10,
    "string": 11,
    "binary": 12,
    "boolean": 13,
    "image": 14,
    "audio": 15,
    "video": 16
}

_np_dtypes = {
    "f32": np.dtype("<f4"),
    "f64": np.dtype("<f8"),
    "i8": np.dtype("i1"),
    "i16": np.dtype("<i2"),
    "i32": np.dtype("<i4"),
    "i64": np.dtype("<i8"),
    "u8": np.dtype("u1"),
    "u16": np.dtype("<u2"),
    "u32": np.dtype("<u4"),
    "u64": np.dtype("<u8"),
    "string": object,
    "binary": object,
    "boolean": bool,
    "image": object,
    "audio": object,
    "video": object
}

_type_element_sizes = {
    "f32": 4,
    "f64": 8,
    "i8": 1,
    "i16": 2,
    "i32": 4,
    "i64": 8,
    "u8": 1,
    "u16": 2,
    "u32": 4,
    "u64": 8,
    "string": None,
    "binary": None,
    "boolean": 1,
    "image": None,
    "audio": None,
    "video": None
}

class DecthingsTensor:
    def __init__(self, data: typing.Union[list, np.ndarray], data_type: str, shape: list[int]):
        if not isinstance(shape, list) or any([not isinstance(x, int) for x in shape]):
            raise TypeError("Invalid shape: Expected shape to be a list of ints.")
        if any([x < 0 for x in shape]):
            raise TypeError("Invalid shape: Expected a list of non-negative integers.")
        if not data_type in _type_specifiers:
            raise ValueError(f"Invalid type: Expected one of {[x for x in _type_specifiers]}.")
        
        if isinstance(data, np.ndarray):
            if _np_dtypes[data_type] != data.dtype:
                raise ValueError(f"Expected dtype {_np_dtypes[data_type]} for data type {data_type}. Got: {data.dtype}")
            self._data = data.reshape(shape)
            self._type = data_type
            return

        expected_num_elements = int(np.prod(np.array(shape)))
        if not isinstance(data, list):
            raise TypeError("Invalid data: Expected a list or Numpy array.")
        if len(data) != expected_num_elements:
            raise ValueError(f"For shape {shape}, expected {expected_num_elements} elements. Got {len(data)}")
        
        if data_type == "string":
            for element in data:
                if not isinstance(element, str):
                    raise TypeError(f"For dtype=string, expected all elements to be strings, not {str(type(element))}.")
            self._data = np.array(data, dtype=object)
        elif data_type == "binary":
            for element in data:
                if not isinstance(element, str):
                    raise TypeError(f"For dtype=binary, expected all elements to be instances of bytes, not {str(type(element))}.")
            self._data = np.array(data, dtype=object)
        elif data_type == "image":
            for element in data:
                if not isinstance(element, DecthingsElementImage):
                    raise TypeError(f"For dtype=image, expected all elements to be instances of DecthingsElementImage, not {str(type(element))}.")
            self._data = np.array(data, dtype=object)
        elif data_type == "audio":
            for element in data:
                if not isinstance(element, DecthingsElementAudio):
                    raise TypeError(f"For dtype=audio, expected all elements to be instances of DecthingsElementAudio, not {str(type(element))}.")
            self._data = np.array(data, dtype=object)
        elif data_type == "video":
            for element in data:
                if not isinstance(element, DecthingsElementVideo):
                    raise TypeError(f"For dtype=video, expected all elements to be instances of DecthingsElementVideo, not {str(type(element))}.")
            self._data = np.array(data, dtype=object)
        else:
            self._data = np.array(data, dtype=_np_dtypes[data_type])

        self._data = self._data.reshape(shape)
        self._type = data_type

    def type(self) -> str:
        return self._type

    def shape(self) -> list[int]:
        return list(self._data.shape)

    def item(self) -> typing.Any:
        return self._data.item()

    def numpy(self) -> np.ndarray:
        return self._data

    @staticmethod
    def deserialize(data: bytes) -> typing.Tuple["DecthingsTensor", int]:
        if len(data) < 2:
            raise ValueError("Invalid data. Unexpected end of bytes.")
        first_byte = data[0]
        if not any([x == first_byte for x in _type_specifiers.values()]):
            raise ValueError(f"Invalid data. Invalid first byte (which specifies the type): {first_byte}. Expected one of the following: {_type_specifiers}")
        data_type = list(_type_specifiers.keys())[list(_type_specifiers.values()).index(first_byte)]

        num_dims = data[1]
        shape: list[int] = []

        pos = 2
        for _ in range(0, num_dims):
            if len(data) < pos + 1:
                raise ValueError("Invalid data. Unexpected end of bytes.")
            varint_len = varint.get_varuint64_length_from_bytes(data[pos:])
            if len(data) < pos + varint_len:
                raise ValueError("Invalid data. Unexpected end of bytes.")
            shape.append(varint.deserialize_varuint64(data[pos:])[0])
            pos += varint_len

        num_elements = int(np.prod(np.array(shape)))

        element_size = _type_element_sizes[data_type]
        if isinstance(element_size, int):
            if element_size * num_elements < len(data) - pos:
                raise ValueError("Invalid data. Unexpected end of bytes.")
            data_np = np.frombuffer(data[pos : pos + element_size * num_elements], dtype=_np_dtypes[data_type])
            return (DecthingsTensor(data_np, data_type, shape), pos + element_size * num_elements)
        else:
            if len(data) < pos + 1:
                raise ValueError("Invalid data. Unexpected end of bytes.")
            pos += varint.get_varuint64_length_from_bytes(data[pos:])

            res: list[typing.Any] = [None] * num_elements
            if data_type == "string":
                for i in range(0, num_elements):
                    if len(data) < pos + 1:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    varint_len = varint.get_varuint64_length_from_bytes(data[pos:])
                    if len(data) < pos + varint_len:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    length, _ = varint.deserialize_varuint64(data[pos:])
                    pos += varint_len
                    if len(data) < pos + length:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    res[i] = data[pos : pos + length].decode()
                    pos += length
            elif data_type == "binary":
                for i in range(0, num_elements):
                    if len(data) < pos + 1:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    varint_len = varint.get_varuint64_length_from_bytes(data[pos:])
                    if len(data) < pos + varint_len:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    length, _ = varint.deserialize_varuint64(data[pos:])
                    pos += varint_len
                    if len(data) < pos + length:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    res[i] = data[pos : pos + length]
                    pos += length
            elif data_type == "image":
                for i in range(0, num_elements):
                    if len(data) < pos + 1:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    varint_len = varint.get_varuint64_length_from_bytes(data[pos:])
                    if len(data) < pos + varint_len:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    length, _ = varint.deserialize_varuint64(data[pos:])
                    pos += varint_len
                    if len(data) < pos + length:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    if length < 1:
                        raise ValueError("Invalid data. Unexpected end of bytes while parsing image format.")
                    format_length = data[pos]
                    if length < 1 + format_length:
                        raise ValueError("Invalid data. Unexpected end of bytes while parsing image format.")
                    res[i] = DecthingsElementImage(data[pos + 1 : pos + 1 + format_length].decode(), data[pos + 1 + format_length : pos + length])
                    pos += length
            elif data_type == "audio":
                for i in range(0, num_elements):
                    if len(data) < pos + 1:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    varint_len = varint.get_varuint64_length_from_bytes(data[pos:])
                    if len(data) < pos + varint_len:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    length, _ = varint.deserialize_varuint64(data[pos:])
                    pos += varint_len
                    if len(data) < pos + length:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    if length < 1:
                        raise ValueError("Invalid data. Unexpected end of bytes while parsing audio format.")
                    format_length = data[pos]
                    if length < 1 + format_length:
                        raise ValueError("Invalid data. Unexpected end of bytes while parsing audio format.")
                    res[i] = DecthingsElementAudio(data[pos + 1 : pos + 1 + format_length].decode(), data[pos + 1 + format_length : pos + length])
                    pos += length
            elif data_type == "video":
                for i in range(0, num_elements):
                    if len(data) < pos + 1:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    varint_len = varint.get_varuint64_length_from_bytes(data[pos:])
                    if len(data) < pos + varint_len:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    length, _ = varint.deserialize_varuint64(data[pos:])
                    pos += varint_len
                    if len(data) < pos + length:
                        raise ValueError("Invalid data. Unexpected end of bytes.")
                    if length < 1:
                        raise ValueError("Invalid data. Unexpected end of bytes while parsing video format.")
                    format_length = data[pos]
                    if length < 1 + format_length:
                        raise ValueError("Invalid data. Unexpected end of bytes while parsing video format.")
                    res[i] = DecthingsElementVideo(data[pos + 1 : pos + 1 + format_length].decode(), data[pos + 1 + format_length : pos + length])
                    pos += length

            return (DecthingsTensor(res, data_type, shape), pos)

    @staticmethod
    def deserialize_many(data: bytes) -> list["DecthingsTensor"]:
        res = []
        
        pos = 0
        while pos < len(data):
            tensor, length = DecthingsTensor.deserialize(data[pos:])
            pos += length
            res.append(tensor)

        return res

    def serialized_byte_size(self) -> int:
        size = 2

        for shape in self.shape():
            size += varint.get_varuint64_length(shape)
        
        num_elements = int(np.prod(np.array(self.shape())))

        element_size = _type_element_sizes[self._type]
        if isinstance(element_size, int):
            size += element_size * num_elements
        else:
            header_size = size

            if self._type == "string":
                for i in range(0, num_elements):
                    el = self._data[i]
                    if not isinstance(el, str):
                        raise ValueError(f"For type string, expected all elements to be strings. Got {str(type(el))}.")
                    size += varint.get_varuint64_length(len(el.encode())) + len(el.encode())
            elif self._type == "binary":
                for i in range(0, num_elements):
                    el = self._data[i]
                    if not isinstance(el, bytes):
                        raise ValueError(f"For type binary, expected all elements to be instances of bytes. Got {str(type(el))}.")
                    size += varint.get_varuint64_length(len(el)) + len(el)
            elif self._type == "image":
                for i in range(0, num_elements):
                    el = self._data[i]
                    if not isinstance(el, DecthingsElementImage):
                        raise ValueError(f"For type image, expected all elements to be instances of DecthingsElementImage. Got {str(type(el))}.")
                    encoded_format = el._format.encode()
                    if len(encoded_format) > 255:
                        raise ValueError("Corrupt data. Expected the 'format' field of each image to be no more than 255 bytes long.")
                    size += varint.get_varuint64_length(1 + len(encoded_format) + len(el._data)) + 1 + len(encoded_format) + len(el._data)
            elif self._type == "audio":
                for i in range(0, num_elements):
                    el = self._data[i]
                    if not isinstance(el, DecthingsElementAudio):
                        raise ValueError(f"For type audio, expected all elements to be instances of DecthingsElementAudio. Got {str(type(el))}.")
                    encoded_format = el._format.encode()
                    if len(encoded_format) > 255:
                        raise ValueError("Corrupt data. Expected the 'format' field of each audio to be no more than 255 bytes long.")
                    size += varint.get_varuint64_length(1 + len(encoded_format) + len(el._data)) + 1 + len(encoded_format) + len(el._data)
            else:
                for i in range(0, num_elements):
                    el = self._data[i]
                    if not isinstance(el, DecthingsElementVideo):
                        raise ValueError(f"For type video, expected all elements to be instances of DecthingsElementVideo. Got {str(type(el))}.")
                    encoded_format = el._format.encode()
                    if len(encoded_format) > 255:
                        raise ValueError("Corrupt data. Expected the 'format' field of each video to be no more than 255 bytes long.")
                    size += varint.get_varuint64_length(1 + len(encoded_format) + len(el._data)) + 1 + len(encoded_format) + len(el._data)

            size += varint.get_varuint64_length(size - header_size)

        return size

    def serialize(self) -> bytes:
        res = [
            _type_specifiers[self._type].to_bytes(1, 'little'),
            len(self.shape()).to_bytes(1, 'little')
        ]

        for shape in self.shape():
            res.append(varint.serialize_varuint64(shape))
        
        num_elements = int(np.prod(np.array(self.shape())))

        element_size = _type_element_sizes[self._type]
        if isinstance(element_size, int):
            np_bytes = self._data.tobytes()
            if len(np_bytes) != element_size * num_elements:
                raise ValueError("Corrupt tensor.")
            res.append(np_bytes)
        else:
            after_header: list[bytes] = []

            elements = list(self._data.reshape(-1))
            if self._type == "string":
                for el in elements:
                    if not isinstance(el, str):
                        raise ValueError("Corrupt tensor.")
                    after_header.append(varint.serialize_varuint64(len(el.encode())))
                    after_header.append(el.encode())
            elif self._type == "binary":
                for el in elements:
                    if not isinstance(el, bytes):
                        raise ValueError("Corrupt tensor.")
                    after_header.append(varint.serialize_varuint64(len(el)))
                    after_header.append(el)
            elif self._type == "image":
                for el in elements:
                    if not isinstance(el, DecthingsElementImage):
                        raise ValueError("Corrupt tensor.")
                    if len(el._format.encode()) != 3:
                        raise ValueError("Corrupt data. Expected the 'format' field of each image to be three bytes long.")
                    after_header.append(varint.serialize_varuint64(3 + len(el._data)))
                    after_header.append(el._format.encode())
                    after_header.append(el._data)
            elif self._type == "audio":
                for el in elements:
                    if not isinstance(el, DecthingsElementAudio):
                        raise ValueError("Corrupt tensor.")
                    encoded_format = el._format.encode()
                    if len(encoded_format) > 255:
                        raise ValueError("Corrupt data. Expected the 'format' field of each audio to be no more than 255 bytes long.")
                    after_header.append(varint.serialize_varuint64(1 + len(encoded_format) + len(el._data)))
                    after_header.append(bytes([len(encoded_format)]))
                    after_header.append(encoded_format)
                    after_header.append(el._data)
            else:
                for el in elements:
                    if not isinstance(el, DecthingsElementVideo):
                        raise ValueError("Corrupt tensor.")
                    encoded_format = el._format.encode()
                    if len(encoded_format) > 255:
                        raise ValueError("Corrupt data. Expected the 'format' field of each video to be no more than 255 bytes long.")
                    after_header.append(varint.serialize_varuint64(1 + len(encoded_format) + len(el._data)))
                    after_header.append(bytes([len(encoded_format)]))
                    after_header.append(encoded_format)
                    after_header.append(el._data)

            res.append(varint.serialize_varuint64(sum([len(x) for x in after_header])))
            res.extend(after_header)

        return b''.join(res)
