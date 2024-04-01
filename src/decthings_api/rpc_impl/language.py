import typing

if typing.TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

class LanguageRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def start_language_server(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [result["languageServerId"]], []
        res = await self.__client._raw_method_call("Language", "startLanguageServer", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]
    
    async def write_to_language_server(self, params):
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
        res = await self.__client._raw_method_call("Language", "writeToLanguageServer", params, [data])
        return res[1], res[2]

    async def unsubscribe_from_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "languageServerId" in params or not isinstance(params["languageServerId"], str):
            raise TypeError('Invalid params: Expected a field "languageServerId" of type str.')
        language_server_id = params["languageServerId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [], [language_server_id]
        res = await self.__client._raw_method_call("Language", "unsubscribeFromEvents", params, [], "wsIfAvailableOtherwiseNone", get_keepalive_change)
        if res[0]:
            return None, { "code": "not_subscribed" }
        return res[1], res[2]

class LanguageRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def start_language_server(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [result["languageServerId"]], []
        res = self.__client._raw_method_call("Language", "startLanguageServer", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]
    
    def write_to_language_server(self, params):
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
        res = self.__client._raw_method_call("Language", "writeToLanguageServer", params, [data])
        return res[1], res[2]

    def unsubscribe_from_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "languageServerId" in params or not isinstance(params["languageServerId"], str):
            raise TypeError('Invalid params: Expected a field "languageServerId" of type str.')
        language_server_id = params["languageServerId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [], [language_server_id]
        res = self.__client._raw_method_call("Language", "unsubscribeFromEvents", params, [], "wsIfAvailableOtherwiseNone", get_keepalive_change)
        if res[0]:
            return None, { "code": "not_subscribed" }
        return res[1], res[2]
