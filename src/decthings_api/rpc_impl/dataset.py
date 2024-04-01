from typing import TYPE_CHECKING
import typing

from ..tensor import DecthingsTensor
if TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

def serialize_add_dataset_data(keys) -> typing.Tuple[list[str], list[bytes]]:
    def validate_key(key):
        if not isinstance(key, dict):
            return False
        if not "key" in key:
            return False
        if not isinstance(key["key"], str):
            return False
        if not "data" in key:
            return False
        if not isinstance(key["data"], list):
            return False
        if any([not isinstance(x, DecthingsTensor) for x in key["data"]]):
            return False
        return True
    
    if not isinstance(keys, list):
        raise TypeError('Invalid parameter "keys": Expected an array of dicts.')

    for key in keys:
        if not validate_key(key):
            raise TypeError('Invalid parameter "keys": Expected an array of dicst like { "key": str, "data": list[DecthingsTensor] }.')
    if len(keys) == 0:
        raise TypeError('Invalid parameter "keys": Got zero keys, but a dataset always has at least one key.')

    num_entries = len(keys[0]["data"])
    for key in keys:
        if len(key["data"]) != num_entries:
            raise TypeError(f'Invalid parameter "keys": All keys must contain the same amount of data. Key {keys[0]["key"]} had {num_entries} elements, but key {key["name"]} had {len(key["data"])} elements.')
            
    sorted_keys = [x["key"] for x in keys]
    sorted_keys.sort()

    if len(set(sorted_keys)) != len(sorted_keys):
        raise TypeError('Invalid parameter "keys": Got duplicate keys. Keys were: {sorted_keys}')

    res: list[bytes] = []

    for i in range(0, num_entries):
        for sorted_key in sorted_keys:
            for key in keys:
                if key["key"] == sorted_key:
                    res.append(key["data"][i].serialize())

    return sorted_keys, res

class DatasetRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def create_dataset(self, params):
        res = await self.__client._raw_method_call("Dataset", "createDataset", params, [])
        return res[1], res[2]
    
    async def update_dataset(self, params):
        res = await self.__client._raw_method_call("Dataset", "updateDataset", params, [])
        return res[1], res[2]

    async def delete_dataset(self, params):
        res = await self.__client._raw_method_call("Dataset", "deleteDataset", params, [])
        return res[1], res[2]

    async def get_datasets(self, params = {}):
        res = await self.__client._raw_method_call("Dataset", "getDatasets", params, [])
        return res[1], res[2]

    async def add_entries(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "keys" in params:
            raise TypeError('Invalid parameter "keys": Parameter missing.')

        keys, serialized = serialize_add_dataset_data(params["keys"])

        new_params = params.copy()
        new_params["keys"] = keys

        res = await self.__client._raw_method_call(
            'Dataset',
            'addEntries',
            new_params,
            serialized
        )
        return res[1], res[2]

    async def add_entries_to_needs_review(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "keys" in params:
            raise TypeError('Invalid parameter "keys": Parameter missing.')

        keys, serialized = serialize_add_dataset_data(params["keys"])

        new_params = params.copy()
        new_params["keys"] = keys

        res = await self.__client._raw_method_call(
            'Dataset',
            'addEntriesToNeedsReview',
            new_params,
            serialized,
        )
        return res[1], res[2]

    async def finalize_needs_review_entries(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "keys" in params:
            raise TypeError('Invalid parameter "keys": Parameter missing.')

        keys, serialized = serialize_add_dataset_data(params["keys"])

        new_params = params.copy()
        new_params["keys"] = keys

        res = await self.__client._raw_method_call('Dataset', 'finalizeNeedsReviewEntries', new_params, serialized)
        return res[1], res[2]

    async def get_entries(self, params):
        res = await self.__client._raw_method_call('Dataset', 'getEntries', params, [])
        if res[1] is None:
            return res[1], res[2]

        keys = [{ "key": key, "data": [] } for key in res[1]["keys"]]

        indexes = res[1]["indexes"]

        pos = 0
        for index in indexes:
            for key in keys:
                key["data"].append({ "index": index, "data": DecthingsTensor.deserialize(res[3][pos])[0] })
                pos += 1

        res[1]["keys"] = keys
        del res[1]["indexes"]
        return res[1], res[2]

    async def get_needs_review_entries(self, params):
        res = await self.__client._raw_method_call('Dataset', 'getNeedsReviewEntries', params, [])
        if res[1] is None:
            return res[1], res[2]

        keys = [{ "key": key, "data": [] } for key in res[1]["keys"]]

        indexes = res[1]["indexes"]

        pos = 0
        for index in indexes:
            for key in keys:
                key["data"].append({ "index": index, "data": DecthingsTensor.deserialize(res[3][pos])[0] })
                pos += 1

        res[1]["keys"] = keys
        del res[1]["indexes"]
        return res[1], res[2]

    async def remove_entries(self, params):
        res = await self.__client._raw_method_call("Dataset", "removeEntries", params, [])
        return res[1], res[2]

    async def remove_needs_review_entries(self, params):
        res = await self.__client._raw_method_call("Dataset", "removeNeedsReviewEntries", params, [])
        return res[1], res[2]

class DatasetRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def create_dataset(self, params):
        res = self.__client._raw_method_call("Dataset", "createDataset", params, [])
        return res[1], res[2]
    
    def update_dataset(self, params):
        res = self.__client._raw_method_call("Dataset", "updateDataset", params, [])
        return res[1], res[2]

    def delete_dataset(self, params):
        res = self.__client._raw_method_call("Dataset", "deleteDataset", params, [])
        return res[1], res[2]

    def get_datasets(self, params = {}):
        res = self.__client._raw_method_call("Dataset", "getDatasets", params, [])
        return res[1], res[2]

    def add_entries(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "keys" in params:
            raise TypeError('Invalid parameter "keys": Parameter missing.')

        keys, serialized = serialize_add_dataset_data(params["keys"])

        new_params = params.copy()
        new_params["keys"] = keys

        res = self.__client._raw_method_call(
            'Dataset',
            'addEntries',
            new_params,
            serialized
        )
        return res[1], res[2]

    def add_entries_to_needs_review(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "keys" in params:
            raise TypeError('Invalid parameter "keys": Parameter missing.')

        keys, serialized = serialize_add_dataset_data(params["keys"])

        new_params = params.copy()
        new_params["keys"] = keys

        res = self.__client._raw_method_call(
            'Dataset',
            'addEntriesToNeedsReview',
            new_params,
            serialized
        )
        return res[1], res[2]

    def finalize_needs_review_entries(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "keys" in params:
            raise TypeError('Invalid parameter "keys": Parameter missing.')

        keys, serialized = serialize_add_dataset_data(params["keys"])

        new_params = params.copy()
        new_params["keys"] = keys

        res = self.__client._raw_method_call('Dataset', 'finalizeNeedsReviewEntries', new_params, serialized)
        return res[1], res[2]

    def get_entries(self, params):
        res = self.__client._raw_method_call('Dataset', 'getEntries', params, [])
        if res[1] is None:
            return res[1], res[2]
        keys = [{ "key": key, "data": [] } for key in res[1]["keys"]]

        indexes = res[1]["indexes"]

        for i, index in enumerate(indexes):
            tensors = DecthingsTensor.deserialize_many(res[3][i])
            for i2, key in enumerate(keys):
                key["data"].append({ "index": index, "data": tensors[i2] })

        res[1]["keys"] = keys
        del res[1]["indexes"]
        return res[1], res[2]

    def get_needs_review_entries(self, params):
        res = self.__client._raw_method_call('Dataset', 'getNeedsReviewEntries', params, [])
        if res[1] is None:
            return res[1], res[2]
        keys = [{ "key": key, "data": [] } for key in res[1]["keys"]]

        indexes = res[1]["indexes"]

        for i, index in enumerate(indexes):
            tensors = DecthingsTensor.deserialize_many(res[3][i])
            for i2, key in enumerate(keys):
                key["data"].append({ "index": index, "data": tensors[i2] })

        res[1]["keys"] = keys
        del res[1]["indexes"]
        return res[1], res[2]

    def remove_entries(self, params):
        res = self.__client._raw_method_call("Dataset", "removeEntries", params, [])
        return res[1], res[2]

    def remove_needs_review_entries(self, params):
        res = self.__client._raw_method_call("Dataset", "removeNeedsReviewEntries", params, [])
        return res[1], res[2]
