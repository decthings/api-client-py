import base64
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

def text_or_binary_to_base64(field_name: str, s: str | bytes) -> str:
    if isinstance(s, str):
        b = s.encode()
    elif isinstance(s, bytes):
        b = s
    else:
        raise TypeError(f'Invalid parameter "{field_name}": Expected str or bytes.')
    return base64.b64encode(b).decode()

class FsRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def lookup(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = await self.__client._raw_method_call("FS", "lookup", new_params, [])
        return res[1], res[2]
    
    async def setattr(self, params):
        res = await self.__client._raw_method_call("FS", "setattr", params, [])
        return res[1], res[2]

    async def getattr(self, params):
        res = await self.__client._raw_method_call("FS", "getattr", params, [])
        return res[1], res[2]

    async def mknod(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = await self.__client._raw_method_call("FS", "mknod", new_params, [])
        return res[1], res[2]
    
    async def read(self, params):
        res = await self.__client._raw_method_call("FS", "read", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["data"] = res[3][0]
        return res[1], res[2]

    async def write(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "data" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        if isinstance(params["data"], bytes):
            data = [params["data"]]
        elif isinstance(params["data"], str):
            data = [params["data"].encode()]
        else:
            raise TypeError('Invalid parameter "data": Expected bytes or str.')
        new_params = params.copy()
        del new_params["data"]
        res = await self.__client._raw_method_call("FS", "mknod", new_params, data)
        return res[1], res[2]

    async def symlink(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        if not "link" in params:
            raise TypeError('Invalid parameter "link": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        new_params["link"] = text_or_binary_to_base64("link", new_params["link"])
        res = await self.__client._raw_method_call("FS", "symlink", new_params, [])
        return res[1], res[2]
    
    async def readlink(self, params):
        res = await self.__client._raw_method_call("FS", "readlink", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["link"] = res[3][0]
        return res[1], res[2]

    async def mkdir(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = await self.__client._raw_method_call("FS", "mkdir", new_params, [])
        return res[1], res[2]

    async def unlink(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = await self.__client._raw_method_call("FS", "unlink", new_params, [])
        return res[1], res[2]

    async def rmdir(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = await self.__client._raw_method_call("FS", "rmdir", new_params, [])
        return res[1], res[2]

    async def rename(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        if not "newname" in params:
            raise TypeError('Invalid parameter "newname": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        new_params["newname"] = text_or_binary_to_base64("newname", new_params["newname"])
        res = await self.__client._raw_method_call("FS", "rename", new_params, [])
        return res[1], res[2]

    async def link(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "newname" in params:
            raise TypeError('Invalid parameter "newname": Missing parameter.')
        new_params = params.copy()
        new_params["newname"] = text_or_binary_to_base64("newname", new_params["newname"])
        res = await self.__client._raw_method_call("FS", "link", new_params, [])
        return res[1], res[2]

    async def readdir(self, params):
        res = await self.__client._raw_method_call("FS", "readdir", params, [])
        if res[1] is None:
            return res[1], res[2]
        for entry in res[1]["entries"]:
            entry["basename"] = base64.b64decode(entry["basename"])
        return res[1], res[2]

    async def rmdir_all(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = await self.__client._raw_method_call("FS", "rmdirAll", new_params, [])
        return res[1], res[2]

    async def copy(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "newname" in params:
            raise TypeError('Invalid parameter "newname": Missing parameter.')
        new_params = params.copy()
        new_params["newname"] = text_or_binary_to_base64("newname", new_params["newname"])
        res = await self.__client._raw_method_call("FS", "copy", new_params, [])
        return res[1], res[2]

class FsRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def lookup(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = self.__client._raw_method_call("FS", "lookup", new_params, [])
        return res[1], res[2]
    
    def setattr(self, params):
        res = self.__client._raw_method_call("FS", "setattr", params, [])
        return res[1], res[2]

    def getattr(self, params):
        res = self.__client._raw_method_call("FS", "getattr", params, [])
        return res[1], res[2]

    def mknod(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = self.__client._raw_method_call("FS", "mknod", new_params, [])
        return res[1], res[2]
    
    def read(self, params):
        res = self.__client._raw_method_call("FS", "read", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["data"] = res[3][0]
        return res[1], res[2]

    def write(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "data" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        if isinstance(params["data"], bytes):
            data = [params["data"]]
        elif isinstance(params["data"], str):
            data = [params["data"].encode()]
        else:
            raise TypeError('Invalid parameter "data": Expected bytes or str.')
        new_params = params.copy()
        del new_params["data"]
        res = self.__client._raw_method_call("FS", "mknod", new_params, data)
        return res[1], res[2]

    def symlink(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        if not "link" in params:
            raise TypeError('Invalid parameter "link": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        new_params["link"] = text_or_binary_to_base64("link", new_params["link"])
        res = self.__client._raw_method_call("FS", "symlink", new_params, [])
        return res[1], res[2]
    
    def readlink(self, params):
        res = self.__client._raw_method_call("FS", "readlink", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["link"] = res[3][0]
        return res[1], res[2]

    def mkdir(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = self.__client._raw_method_call("FS", "mkdir", new_params, [])
        return res[1], res[2]

    def unlink(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = self.__client._raw_method_call("FS", "unlink", new_params, [])
        return res[1], res[2]

    def rmdir(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = self.__client._raw_method_call("FS", "rmdir", new_params, [])
        return res[1], res[2]

    def rename(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        if not "newname" in params:
            raise TypeError('Invalid parameter "newname": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        new_params["newname"] = text_or_binary_to_base64("newname", new_params["newname"])
        res = self.__client._raw_method_call("FS", "rename", new_params, [])
        return res[1], res[2]

    def link(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "newname" in params:
            raise TypeError('Invalid parameter "newname": Missing parameter.')
        new_params = params.copy()
        new_params["newname"] = text_or_binary_to_base64("newname", new_params["newname"])
        res = self.__client._raw_method_call("FS", "link", new_params, [])
        return res[1], res[2]

    def readdir(self, params):
        res = self.__client._raw_method_call("FS", "readdir", params, [])
        if res[1] is None:
            return res[1], res[2]
        for entry in res[1]["entries"]:
            entry["basename"] = base64.b64decode(entry["basename"])
        return res[1], res[2]

    def rmdir_all(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "name" in params:
            raise TypeError('Invalid parameter "name": Missing parameter.')
        new_params = params.copy()
        new_params["name"] = text_or_binary_to_base64("name", new_params["name"])
        res = self.__client._raw_method_call("FS", "rmdirAll", new_params, [])
        return res[1], res[2]

    def copy(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "newname" in params:
            raise TypeError('Invalid parameter "newname": Missing parameter.')
        new_params = params.copy()
        new_params["newname"] = text_or_binary_to_base64("newname", new_params["newname"])
        res = self.__client._raw_method_call("FS", "copy", new_params, [])
        return res[1], res[2]
