import typing

if typing.TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

class TerminalRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def launch_terminal_session(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "subscribeToEvents" in params:
            subscribed = True
        else:
            subscribed = params["subscribeToEvents"] != False
        def get_keepalive_change(result, _):
            if not subscribed or result is None:
                return [], []
            return [result["terminalSessionId"]], []
        res = await self.__client._raw_method_call("Terminal", "launchTerminalSession", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]
    
    async def terminate_terminal_session(self, params):
        res = await self.__client._raw_method_call('Terminal', 'terminateTerminalSession', params, [])
        return res[1], res[2]

    async def get_terminal_sessions(self, params):
        res = await self.__client._raw_method_call('Terminal', 'getTerminalSessions', params, [])
        return res[1], res[2]

    async def write_to_terminal_session(self, params):
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
        res = await self.__client._raw_method_call("Terminal", "writeToTerminalSession", params, [data])
        return res[1], res[2]

    async def resize_terminal_session(self, params):
        res = await self.__client._raw_method_call('Terminal', 'resizeTerminalSession', params, [])
        return res[1], res[2]

    async def add_filesystem_access_for_terminal_session(self, params):
        res = await self.__client._raw_method_call('Terminal', 'addFilesystemAccessForTerminalSession', params, [])
        return res[1], res[2]

    async def subscribe_to_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "terminalSessionId" in params or not isinstance(params["terminalSessionId"], str):
            raise TypeError('Invalid params: Expected a field "terminalSessionId" of type str.')
        terminal_session_id = params["terminalSessionId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [terminal_session_id], []
        res = await self.__client._raw_method_call("Terminal", "subscribeToEvents", params, [], "ws", get_keepalive_change)
        return res[1], res[2]

    async def unsubscribe_from_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "terminalSessionId" in params or not isinstance(params["terminalSessionId"], str):
            raise TypeError('Invalid params: Expected a field "terminalSessionId" of type str.')
        terminal_session_id = params["terminalSessionId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [], [terminal_session_id]
        res = await self.__client._raw_method_call("Terminal", "unsubscribeFromEvents", params, [], "wsIfAvailableOtherwiseNone", get_keepalive_change)
        if res[0]:
            return None, { "code": "not_subscribed" }
        return res[1], res[2]

class TerminalRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def launch_terminal_session(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "subscribeToEvents" in params:
            subscribed = True
        else:
            subscribed = params["subscribeToEvents"] != False
        def get_keepalive_change(result, _):
            if not subscribed or result is None:
                return [], []
            return [result["terminalSessionId"]], []
        res = self.__client._raw_method_call("Terminal", "launchTerminalSession", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]
    
    def terminate_terminal_session(self, params):
        res = self.__client._raw_method_call('Terminal', 'terminateTerminalSession', params, [])
        return res[1], res[2]

    def get_terminal_sessions(self, params):
        res = self.__client._raw_method_call('Terminal', 'getTerminalSessions', params, [])
        return res[1], res[2]

    def write_to_terminal_session(self, params):
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
        res = self.__client._raw_method_call("Terminal", "writeToTerminalSession", params, [data])
        return res[1], res[2]

    def resize_terminal_session(self, params):
        res = self.__client._raw_method_call('Terminal', 'resizeTerminalSession', params, [])
        return res[1], res[2]

    def add_filesystem_access_for_terminal_session(self, params):
        res = self.__client._raw_method_call('Terminal', 'addFilesystemAccessForTerminalSession', params, [])
        return res[1], res[2]

    def subscribe_to_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "terminalSessionId" in params or not isinstance(params["terminalSessionId"], str):
            raise TypeError('Invalid params: Expected a field "terminalSessionId" of type str.')
        terminal_session_id = params["terminalSessionId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [terminal_session_id], []
        res = self.__client._raw_method_call("Terminal", "subscribeToEvents", params, [], "ws", get_keepalive_change)
        return res[1], res[2]

    def unsubscribe_from_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "terminalSessionId" in params or not isinstance(params["terminalSessionId"], str):
            raise TypeError('Invalid params: Expected a field "terminalSessionId" of type str.')
        terminal_session_id = params["terminalSessionId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [], [terminal_session_id]
        res = self.__client._raw_method_call("Terminal", "unsubscribeFromEvents", params, [], "wsIfAvailableOtherwiseNone", get_keepalive_change)
        if res[0]:
            return None, { "code": "not_subscribed" }
        return res[1], res[2]
