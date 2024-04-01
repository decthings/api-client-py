import typing

if typing.TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

class PersistentLauncherRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def create_persistent_launcher(self, params):
        res = await self.__client._raw_method_call('PersistentLauncher', 'createPersistentLauncher', params, [])
        return res[1], res[2]

    async def get_persistent_launchers(self, params):
        res = await self.__client._raw_method_call('PersistentLauncher', 'getPersistentLaunchers', params, [])
        return res[1], res[2]

    async def get_sysinfo(self, params):
        res = await self.__client._raw_method_call('PersistentLauncher', 'getSysinfo', params, [])
        return res[1], res[2]

    async def delete_persistent_launcher(self, params):
        res = await self.__client._raw_method_call('PersistentLauncher', 'deletePersistentLauncher', params, [])
        return res[1], res[2]

class PersistentLauncherRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def create_persistent_launcher(self, params):
        res = self.__client._raw_method_call('PersistentLauncher', 'createPersistentLauncher', params, [])
        return res[1], res[2]

    def get_persistent_launchers(self, params):
        res = self.__client._raw_method_call('PersistentLauncher', 'getPersistentLaunchers', params, [])
        return res[1], res[2]

    def get_sysinfo(self, params):
        res = self.__client._raw_method_call('PersistentLauncher', 'getSysinfo', params, [])
        return res[1], res[2]

    def delete_persistent_launcher(self, params):
        res = self.__client._raw_method_call('PersistentLauncher', 'deletePersistentLauncher', params, [])
        return res[1], res[2]
