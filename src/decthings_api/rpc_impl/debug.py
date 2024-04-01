import typing

from decthings_api.rpc_impl.convert import serialize_parameter_providers
from decthings_api.tensor import DecthingsTensor
if typing.TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

class DebugRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def launch_debug_session(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "subscribeToEvents" in params:
            subscribed = True
        else:
            subscribed = params["subscribeToEvents"] != False
        def get_keepalive_change(result, _):
            if not subscribed or result is None:
                return [], []
            return [result["debugSessionId"]], []
        res = await self.__client._raw_method_call("Debug", "launchDebugSession", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]
    
    async def get_debug_sessions(self, params):
        res = await self.__client._raw_method_call("Debug", "getDebugSessions", params, [])
        return res[1], res[2]

    async def terminate_debug_session(self, params):
        res = await self.__client._raw_method_call("Debug", "terminateDebugSession", params, [])
        return res[1], res[2]

    async def call_create_model_state(self, params = {}):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = await self.__client._raw_method_call("Debug", "callCreateModelState", new_params, data)
        return res[1], res[2]

    async def call_instantiate_model(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "stateData" in params or not isinstance(params["stateData"], dict):
            raise TypeError('Invalid parameter "stateData": Expected a dict.')
        state_data = params["stateData"]
        if not "type" in state_data:
            raise TypeError('Invalid parameter "stateData": Expected a field "type".')
        if state_data["type"] == "data":
            if not "data" in state_data:
                raise TypeError('Invalid parameter "stateData": For type="data", expected a field "data".')
            if not isinstance(state_data["data"], list):
                raise TypeError('Invalid parameter "stateData": For type="data", expected the field "data" to be a list.')
            for entry in state_data["data"]:
                if not isinstance(entry, dict) or not "key" in entry or not "data" in entry or not isinstance(entry["key"], str) or not isinstance(entry["data"], bytes):
                    raise TypeError('Invalid parameter "stateData": For type="data", expected each element of field "data" to be an dict like { "key": str, "data": bytes }.')
            data = [entry["data"] for entry in state_data["data"]]
            new_state_data = state_data.copy()
            del new_state_data["data"]
            new_state_data["stateKeyNames"] = [entry["key"] for entry in state_data["data"]]
            new_params = params.copy()
            new_params["stateData"] = new_state_data
        else:
            new_params = params
            data = []
        res = await self.__client._raw_method_call(
            'Debug',
            'callInstantiateModel',
            new_params,
            data
        )
        return res[1], res[2]

    async def call_train(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = await self.__client._raw_method_call('Debug', 'callTrain', new_params, data)
        return res[1], res[2]

    async def get_training_status(self, params):
        res = await self.__client._raw_method_call('Debug', 'getTrainingStatus', params, [])
        return res[1], res[2]

    async def get_training_metrics(self, params):
        res = await self.__client._raw_method_call('Debug', 'getTrainingMetrics', params, [])
        if res[1] is None:
            return res[1], res[2]
        metrics = res[1]["metrics"]
        i = 0
        for metric in metrics:
            for entry in metric["entries"]:
                entry["data"] = DecthingsTensor.deserialize(res[3][i])[0]
                i += 1
        return res[1], res[2]

    async def cancel_training_session(self, params):
        res = await self.__client._raw_method_call("Debug", "cancelTrainingSession", params, [])
        return res[1], res[2]

    async def call_evaluate(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = await self.__client._raw_method_call("Debug", "callEvaluate", new_params, data)
        if res[1] is None:
            return res[1], res[2]
        for i, el in enumerate(res[1]["output"]):
            el["data"] = DecthingsTensor.deserialize_many(res[3][i])
        return res[1], res[2]

    async def call_get_model_state(self, params):
        res = await self.__client._raw_method_call("Debug", "callGetModelState", params, [])
        return res[1], res[2]

    async def download_state_data(self, params):
        res = await self.__client._raw_method_call("Debug", "removeNeedsReviewEntries", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["data"] = [{ "key": key, "data": res[3][idx] } for idx, key in enumerate(res[1]["stateKeyNames"])]
        del res[1]["stateKeyNames"]
        return res[1], res[2]

    async def send_to_remote_inspector(self, params):
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
        res = await self.__client._raw_method_call("Debug", "sendToRemoteInspector", params, [data])
        return res[1], res[2]

    async def subscribe_to_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "debugSessionId" in params or not isinstance(params["debugSessionId"], str):
            raise TypeError('Invalid params: Expected a field "debugSessionId" of type str.')
        debug_session_id = params["debugSessionId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [debug_session_id], []
        res = await self.__client._raw_method_call("Debug", "subscribeToEvents", params, [], "ws", get_keepalive_change)
        return res[1], res[2]

    async def unsubscribe_from_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "debugSessionId" in params or not isinstance(params["debugSessionId"], str):
            raise TypeError('Invalid params: Expected a field "debugSessionId" of type str.')
        debug_session_id = params["debugSessionId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [], [debug_session_id]
        res = await self.__client._raw_method_call("Debug", "unsubscribeFromEvents", params, [], "wsIfAvailableOtherwiseNone", get_keepalive_change)
        if res[0]:
            return None, { "code": "not_subscribed" }
        return res[1], res[2]

class DebugRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def launch_debug_session(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "subscribeToEvents" in params:
            subscribed = True
        else:
            subscribed = params["subscribeToEvents"] != False
        def get_keepalive_change(result, _):
            if not subscribed or result is None:
                return [], []
            return [result["debugSessionId"]], []
        res = self.__client._raw_method_call("Debug", "launchDebugSession", params, [], get_keepalive_change=get_keepalive_change)
        return res[1], res[2]
    
    def get_debug_sessions(self, params):
        res = self.__client._raw_method_call("Debug", "getDebugSessions", params, [])
        return res[1], res[2]

    def terminate_debug_session(self, params):
        res = self.__client._raw_method_call("Debug", "terminateDebugSession", params, [])
        return res[1], res[2]

    def call_create_model_state(self, params = {}):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = self.__client._raw_method_call("Debug", "callCreateModelState", new_params, data)
        return res[1], res[2]

    def call_instantiate_model(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "stateData" in params or not isinstance(params["stateData"], dict):
            raise TypeError('Invalid parameter "stateData": Expected a dict.')
        state_data = params["stateData"]
        if not "type" in state_data:
            raise TypeError('Invalid parameter "stateData": Expected a field "type".')
        if state_data["type"] == "data":
            if not "data" in state_data:
                raise TypeError('Invalid parameter "stateData": For type="data", expected a field "data".')
            if not isinstance(state_data["data"], list):
                raise TypeError('Invalid parameter "stateData": For type="data", expected the field "data" to be a list.')
            for entry in state_data["data"]:
                if not isinstance(entry, dict) or not "key" in entry or not "data" in entry or not isinstance(entry["key"], str) or not isinstance(entry["data"], bytes):
                    raise TypeError('Invalid parameter "stateData": For type="data", expected each element of field "data" to be an dict like { "key": str, "data": bytes }.')
            data = [entry["data"] for entry in state_data["data"]]
            new_state_data = state_data.copy()
            del new_state_data["data"]
            new_state_data["stateKeyNames"] = [entry["key"] for entry in state_data["data"]]
            new_params = params.copy()
            new_params["stateData"] = new_state_data
        else:
            new_params = params
            data = []
        res = self.__client._raw_method_call(
            'Debug',
            'callInstantiateModel',
            new_params,
            data
        )
        return res[1], res[2]

    def call_train(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = self.__client._raw_method_call('Debug', 'callTrain', new_params, data)
        return res[1], res[2]

    def get_training_status(self, params):
        res = self.__client._raw_method_call('Debug', 'getTrainingStatus', params, [])
        return res[1], res[2]

    def get_training_metrics(self, params):
        res = self.__client._raw_method_call('Debug', 'getTrainingMetrics', params, [])
        if res[1] is None:
            return res[1], res[2]
        metrics = res[1]["metrics"]
        i = 0
        for metric in metrics:
            for entry in metric["entries"]:
                entry["data"] = DecthingsTensor.deserialize(res[3][i])[0]
                i += 1
        return res[1], res[2]

    def cancel_training_session(self, params):
        res = self.__client._raw_method_call("Debug", "cancelTrainingSession", params, [])
        return res[1], res[2]

    def call_evaluate(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = self.__client._raw_method_call("Debug", "callEvaluate", new_params, data)
        if res[1] is None:
            return res[1], res[2]
        for i, el in enumerate(res[1]["output"]):
            el["data"] = DecthingsTensor.deserialize_many(res[3][i])
        return res[1], res[2]

    def call_get_model_state(self, params):
        res = self.__client._raw_method_call("Debug", "callGetModelState", params, [])
        return res[1], res[2]

    def download_state_data(self, params):
        res = self.__client._raw_method_call("Debug", "removeNeedsReviewEntries", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["data"] = [{ "key": key, "data": res[3][idx] } for idx, key in enumerate(res[1]["stateKeyNames"])]
        del res[1]["stateKeyNames"]
        return res[1], res[2]

    def send_to_remote_inspector(self, params):
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
        res = self.__client._raw_method_call("Debug", "sendToRemoteInspector", params, [data])
        return res[1], res[2]

    def subscribe_to_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "debugSessionId" in params or not isinstance(params["debugSessionId"], str):
            raise TypeError('Invalid params: Expected a field "debugSessionId" of type str.')
        debug_session_id = params["debugSessionId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [debug_session_id], []
        res = self.__client._raw_method_call("Debug", "subscribeToEvents", params, [], "ws", get_keepalive_change)
        return res[1], res[2]

    def unsubscribe_from_events(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "debugSessionId" in params or not isinstance(params["debugSessionId"], str):
            raise TypeError('Invalid params: Expected a field "debugSessionId" of type str.')
        debug_session_id = params["debugSessionId"]
        def get_keepalive_change(result, _):
            if result is None:
                return [], []
            return [], [debug_session_id]
        res = self.__client._raw_method_call("Debug", "unsubscribeFromEvents", params, [], "wsIfAvailableOtherwiseNone", get_keepalive_change)
        if res[0]:
            return None, { "code": "not_subscribed" }
        return res[1], res[2]
