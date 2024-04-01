import typing

if typing.TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

class SpawnedRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def spawn_command(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "subscribeToEvents" in params:
            subscribed = True
        else:
            subscribed = params["subscribeToEvents"] != False
        def get_keepalive_change(result, _):
            if not subscribed or result is None:
                return [], []
            return [result["spawnedCommandId"]], []
        res = await self.__client._raw_method_call("Spawned", "spawnCommand", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]

    async def spawn_command_for_model(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "subscribeToEvents" in params:
            subscribed = True
        else:
            subscribed = params["subscribeToEvents"] != False
        def get_keepalive_change(result, _):
            if not subscribed or result is None:
                return [], []
            return [result["spawnedCommandId"]], []
        res = await self.__client._raw_method_call("Spawned", "spawnCommandForModel", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]
    
    async def terminate_spawned_command(self, params):
        res = await self.__client._raw_method_call('Spawned', 'terminateSpawnedCommand', params, [])
        return res[1], res[2]

    async def get_spawned_commands(self, params):
        res = await self.__client._raw_method_call('Spawned', 'getSpawnedCommands', params, [])
        return res[1], res[2]

    async def write_to_spawned_command(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "data" in params:
            raise TypeError('Invalid params: Expected a field "data".')
        if isinstance(params["data"], str):
            data = params["data"].encode()
        elif isinstance(params["data"], bytes):
            data = params["data"]
        else:
            raise TypeError('Invalid parameter "data": Expected a str or bytes.')
        new_params = params.copy()
        del new_params["data"]
        res = await self.__client._raw_method_call("Spawned", "writeToSpawnedCommand", params, [data])
        return res[1], res[2]

    async def subscribe_to_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "spawnedCommandId" in params or not isinstance(params["spawnedCommandId"], str):
            raise TypeError('Invalid params: Expected a field "spawnedCommandId" of type str.')
        spawned_command_id = params["spawnedCommandId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [spawned_command_id], []
        res = await self.__client._raw_method_call("Spawned", "subscribeToEvents", params, [], "ws", get_keepalive_change)
        return res[1], res[2]

    async def unsubscribe_from_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "spawnedCommandId" in params or not isinstance(params["spawnedCommandId"], str):
            raise TypeError('Invalid params: Expected a field "spawnedCommandId" of type str.')
        spawned_command_id = params["spawnedCommandId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [], [spawned_command_id]
        res = await self.__client._raw_method_call("Spawned", "unsubscribeFromEvents", params, [], "wsIfAvailableOtherwiseNone", get_keepalive_change)
        if res[0]:
            return None, { "code": "not_subscribed" }
        return res[1], res[2]

class SpawnedRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def spawn_command(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "subscribeToEvents" in params:
            subscribed = True
        else:
            subscribed = params["subscribeToEvents"] != False
        def get_keepalive_change(result, _):
            if not subscribed or result is None:
                return [], []
            return [result["spawnedCommandId"]], []
        res = self.__client._raw_method_call("Spawned", "spawnCommand", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]

    def spawn_command_for_model(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "subscribeToEvents" in params:
            subscribed = True
        else:
            subscribed = params["subscribeToEvents"] != False
        def get_keepalive_change(result, _):
            if not subscribed or result is None:
                return [], []
            return [result["spawnedCommandId"]], []
        res = self.__client._raw_method_call("Spawned", "spawnCommandForModel", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]
    
    def terminate_spawned_command(self, params):
        res = self.__client._raw_method_call('Spawned', 'terminateSpawnedCommand', params, [])
        return res[1], res[2]

    def get_spawned_commands(self, params):
        res = self.__client._raw_method_call('Spawned', 'getSpawnedCommands', params, [])
        return res[1], res[2]

    def write_to_spawned_command(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "data" in params:
            raise TypeError('Invalid params: Expected a field "data".')
        if isinstance(params["data"], str):
            data = params["data"].encode()
        elif isinstance(params["data"], bytes):
            data = params["data"]
        else:
            raise TypeError('Invalid parameter "data": Expected a str or bytes.')
        new_params = params.copy()
        del new_params["data"]
        res = self.__client._raw_method_call("Spawned", "writeToSpawnedCommand", params, [data])
        return res[1], res[2]

    def subscribe_to_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "spawnedCommandId" in params or not isinstance(params["spawnedCommandId"], str):
            raise TypeError('Invalid params: Expected a field "spawnedCommandId" of type str.')
        spawned_command_id = params["spawnedCommandId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [spawned_command_id], []
        res = self.__client._raw_method_call("Spawned", "subscribeToEvents", params, [], "ws", get_keepalive_change)
        return res[1], res[2]

    def unsubscribe_from_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "spawnedCommandId" in params or not isinstance(params["spawnedCommandId"], str):
            raise TypeError('Invalid params: Expected a field "spawnedCommandId" of type str.')
        spawned_command_id = params["spawnedCommandId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [], [spawned_command_id]
        res = self.__client._raw_method_call("Spawned", "unsubscribeFromEvents", params, [], "wsIfAvailableOtherwiseNone", get_keepalive_change)
        if res[0]:
            return None, { "code": "not_subscribed" }
        return res[1], res[2]
