import typing

from ..rpc_impl.convert import serialize_parameter_providers
from ..tensor import DecthingsTensor
if typing.TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

class ModelRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def create_model(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "options" in params or not isinstance(params["options"], dict):
            raise TypeError('Invalid parameter "options": Expected a dict.')
        options = params["options"]
        if not "type" in options:
            raise TypeError('Invalid parameter "options": Expected a field "type".')
        if options["type"] == "basedOnModelSnapshot":
            if not "initialState" in options:
                raise TypeError('Invalid parameter "options": For type = "basedOnModelSnapshot", expected a field "initialState".')
            initial_state = options["initialState"]
            if not isinstance(initial_state, dict):
                raise TypeError('Invalid parameter "options": Expected the field "initialState" to be a dict.')
            if initial_state["method"] == "create":
                if not "params" in initial_state:
                    raise TypeError('Invalid parameter "options": Expected the field "initialState" to contain a field "params".')
                new_params = params.copy()
                new_options = options.copy()
                new_initial_state = initial_state.copy()
                new_parameter_providers, data = serialize_parameter_providers(initial_state["params"])
                new_initial_state["params"] = new_parameter_providers
                new_options["initialState"] = new_initial_state
                new_params["options"] = new_options
            if initial_state["method"] == "upload":
                if not "data" in initial_state:
                    raise TypeError('Invalid parameter "options": Expected the field "initialState" to contain a field "data".')
                if not isinstance(initial_state["data"], list):
                    raise TypeError('Invalid parameter "options": Expected the field "data" of "initialState" to be a list.')
                for entry in initial_state["data"]:
                    if not isinstance(entry, dict) or not "key" in entry or not "data" in entry or not isinstance(entry["key"], str) or not isinstance(entry["data"], bytes):
                        raise TypeError('Invalid parameter "options": Expected the field "data" of "initialState" to be a list of dicts like { "key": str, "data": bytes }.')
                data = [entry["data"] for entry in initial_state["data"]]
                new_params = params.copy()
                new_options = options.copy()
                new_initial_state = initial_state.copy()
                del new_initial_state["data"]
                new_initial_state["stateKeyNames"] = [entry["key"] for entry in initial_state["data"]]
                new_options["initialState"] = new_initial_state
                new_params["options"] = new_options
            else:
                new_params = params
                data = []
        elif options["type"] == "upload":
            if not "data" in options or not isinstance(options["data"], bytes):
                raise TypeError('For type "upload", expected an option "data" of type bytes.')
            data = [options["data"]]
            new_options = params["options"].copy()
            del new_options["data"]
            new_params = params.copy()
            new_params["options"] = new_options
        else:
            new_params = params
            data = []
        res = await self.__client._raw_method_call(
            'Model',
            'createModel',
            new_params,
            data
        )
        return res[1], res[2]

    async def wait_for_model_to_be_created(self, params):
        res = await self.__client._raw_method_call('Model', 'waitForModelToBeCreated', params, [])
        return res[1], res[2]

    async def delete_model(self, params):
        res = await self.__client._raw_method_call('Model', 'deleteModel', params, [])
        return res[1], res[2]

    async def snapshot_model(self, params):
        res = await self.__client._raw_method_call('Model', 'snapshotModel', params, [])
        return res[1], res[2]

    async def update_snapshot(self, params):
        res = await self.__client._raw_method_call('Model', 'updateSnapshot', params, [])
        return res[1], res[2]

    async def delete_snapshot(self, params):
        res = await self.__client._raw_method_call('Model', 'deleteSnapshot', params, [])
        return res[1], res[2]

    async def update_model(self, params):
        res = await self.__client._raw_method_call('Model', 'updateModel', params, [])
        return res[1], res[2]

    async def get_models(self, params):
        res = await self.__client._raw_method_call('Model', 'getModels', params, [])
        return res[1], res[2]

    async def set_filesystem_size(self, params):
        res = await self.__client._raw_method_call('Model', 'setFilesystemSize', params, [])
        return res[1], res[2]

    async def create_state(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "params" in params:
            raise TypeError('Invalid parameter "params": Missing parameter.')
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = await self.__client._raw_method_call('Model', 'createState', new_params, data)
        return res[1], res[2]

    async def upload_state(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "data" in params:
            raise TypeError('Invalid parameter "data": Missing parameter.')
        if not isinstance(params["data"], list):
            raise TypeError('Invalid parameter "data": Expected a list.')
        for entry in params["data"]:
            if not isinstance(entry, dict) or not "key" in entry or not "data" in entry or not isinstance(entry["key"], str) or not isinstance(entry["data"], bytes):
                raise TypeError('Invalid parameter "data": Expected a list of dicts like { "key": str, "data": bytes }.')
        new_params = params.copy()
        del new_params["data"]
        data = [x["data"] for x in params["data"]]
        new_params["stateKeyNames"] = [x["key"] for x in params["data"]]
        res = await self.__client._raw_method_call('Model', 'uploadState', new_params, data)
        return res[1], res[2]

    async def get_creating_states(self, params):
        res = await self.__client._raw_method_call('Model', 'getCreatingStates', params, [])
        return res[1], res[2]

    async def wait_for_state_to_be_created(self, params):
        res = await self.__client._raw_method_call('Model', 'waitForStateToBeCreated', params, [])
        return res[1], res[2]

    async def update_model_state(self, params):
        res = await self.__client._raw_method_call('Model', 'updateModelState', params, [])
        return res[1], res[2]

    async def set_current_model_state(self, params):
        res = await self.__client._raw_method_call('Model', 'setCurrentModelState', params, [])
        return res[1], res[2]

    async def delete_model_state(self, params):
        res = await self.__client._raw_method_call('Model', 'deleteModelState', params, [])
        return res[1], res[2]

    async def get_model_state(self, params):
        res = await self.__client._raw_method_call("Model", "getModelState", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["data"] = [{ "key": key, "data": res[3][idx] } for idx, key in enumerate(res[1]["stateKeyNames"])]
        del res[1]["stateKeyNames"]
        return res[1], res[2]

    async def get_snapshot_state(self, params):
        res = await self.__client._raw_method_call("Model", "getSnapshotState", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["data"] = [{ "key": key, "data": res[3][idx] } for idx, key in enumerate(res[1]["stateKeyNames"])]
        del res[1]["stateKeyNames"]
        return res[1], res[2]

    async def train(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = await self.__client._raw_method_call("Model", "train", new_params, data)
        return res[1], res[2]

    async def get_training_status(self, params):
        res = await self.__client._raw_method_call('Model', 'getTrainingStatus', params, [])
        return res[1], res[2]

    async def get_training_metrics(self, params):
        res = await self.__client._raw_method_call('Model', 'getTrainingMetrics', params, [])
        if res[1] is None:
            return res[1], res[2]
        metrics = res[1]["metrics"]
        i = 0
        for metric in metrics:
            for entry in metric["entries"]:
                entry["data"] = DecthingsTensor.deserialize(res[3][i])[0]
                i += 1
        return res[1], res[2]

    async def get_training_sysinfo(self, params):
        res = await self.__client._raw_method_call('Model', 'getTrainingSysinfo', params, [])
        return res[1], res[2]

    async def cancel_training_session(self, params):
        res = await self.__client._raw_method_call("Model", "cancelTrainingSession", params, [])
        return res[1], res[2]

    async def clear_previous_training_session(self, params):
        res = await self.__client._raw_method_call("Model", "clearPreviousTrainingSession", params, [])
        return res[1], res[2]

    async def evaluate(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = await self.__client._raw_method_call("Model", "evaluate", new_params, data)
        if res[1] is None:
            return res[1], res[2]
        if "success" in res[1]:
            for i, param in enumerate(res[1]["success"]["output"]):
                param["data"] = DecthingsTensor.deserialize_many(res[3][i])
        return res[1], res[2]

    async def get_evaluations(self, params):
        res = await self.__client._raw_method_call("Model", "getEvaluations", params, [])
        return res[1], res[2]

    async def get_finished_evaluation_result(self, params):
        res = await self.__client._raw_method_call("Model", "getFinishedEvaluationResult", params, [])
        if res[1] is None:
            return res[1], res[2]
        if "evaluationSuccess" in res[1]:
            for i, param in enumerate(res[1]["success"]["output"]):
                param["data"] = DecthingsTensor.deserialize_many(res[3][i])
        return res[1], res[2]

    async def cancel_evaluation(self, params):
        res = await self.__client._raw_method_call("Model", "cancelEvaluation", params, [])
        return res[1], res[2]

    async def set_used_persistent_launchers_for_evaluate(self, params):
        res = await self.__client._raw_method_call("Model", "setUsedPersistentLaunchersForEvaluate", params, [])
        return res[1], res[2]

    async def get_used_persistent_launchers_for_evaluate(self, params):
        res = await self.__client._raw_method_call("Model", "getUsedPersistentLaunchersForEvaluate", params, [])
        return res[1], res[2]

class ModelRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def create_model(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "options" in params or not isinstance(params["options"], dict):
            raise TypeError('Invalid parameter "options": Expected a dict.')
        options = params["options"]
        if not "type" in options:
            raise TypeError('Invalid parameter "options": Expected a field "type".')
        if options["type"] == "basedOnModelSnapshot":
            if not "initialState" in options:
                raise TypeError('Invalid parameter "options": For type = "basedOnModelSnapshot", expected a field "initialState".')
            initial_state = options["initialState"]
            if not isinstance(initial_state, dict):
                raise TypeError('Invalid parameter "options": Expected the field "initialState" to be a dict.')
            if initial_state["method"] == "create":
                if not "params" in initial_state:
                    raise TypeError('Invalid parameter "options": Expected the field "initialState" to contain a field "params".')
                new_params = params.copy()
                new_options = options.copy()
                new_initial_state = initial_state.copy()
                new_parameter_providers, data = serialize_parameter_providers(initial_state["params"])
                new_initial_state["params"] = new_parameter_providers
                new_options["initialState"] = new_initial_state
                new_params["options"] = new_options
            if initial_state["method"] == "upload":
                if not "data" in initial_state:
                    raise TypeError('Invalid parameter "options": Expected the field "initialState" to contain a field "data".')
                if not isinstance(initial_state["data"], list):
                    raise TypeError('Invalid parameter "options": Expected the field "data" of "initialState" to be a list.')
                for entry in initial_state["data"]:
                    if not isinstance(entry, dict) or not "key" in entry or not "data" in entry or not isinstance(entry["key"], str) or not isinstance(entry["data"], bytes):
                        raise TypeError('Invalid parameter "options": Expected the field "data" of "initialState" to be a list of dicts like { "key": str, "data": bytes }.')
                data = [entry["data"] for entry in initial_state["data"]]
                new_params = params.copy()
                new_options = options.copy()
                new_initial_state = initial_state.copy()
                del new_initial_state["data"]
                new_initial_state["stateKeyNames"] = [entry["key"] for entry in initial_state["data"]]
                new_options["initialState"] = new_initial_state
                new_params["options"] = new_options
            else:
                new_params = params
                data = []
        elif options["type"] == "upload":
            if not "data" in options or not isinstance(options["data"], bytes):
                raise TypeError('For type "upload", expected an option "data" of type bytes.')
            data = [options["data"]]
            new_options = params["options"].copy()
            del new_options["data"]
            new_params = params.copy()
            new_params["options"] = new_options
        else:
            new_params = params
            data = []
        res = self.__client._raw_method_call(
            'Model',
            'createModel',
            new_params,
            data
        )
        return res[1], res[2]

    def wait_for_model_to_be_created(self, params):
        res = self.__client._raw_method_call('Model', 'waitForModelToBeCreated', params, [])
        return res[1], res[2]

    def delete_model(self, params):
        res = self.__client._raw_method_call('Model', 'deleteModel', params, [])
        return res[1], res[2]

    def snapshot_model(self, params):
        res = self.__client._raw_method_call('Model', 'snapshotModel', params, [])
        return res[1], res[2]

    def update_snapshot(self, params):
        res = self.__client._raw_method_call('Model', 'updateSnapshot', params, [])
        return res[1], res[2]

    def delete_snapshot(self, params):
        res = self.__client._raw_method_call('Model', 'deleteSnapshot', params, [])
        return res[1], res[2]

    def update_model(self, params):
        res = self.__client._raw_method_call('Model', 'updateModel', params, [])
        return res[1], res[2]

    def get_models(self, params):
        res = self.__client._raw_method_call('Model', 'getModels', params, [])
        return res[1], res[2]

    def set_filesystem_size(self, params):
        res = self.__client._raw_method_call('Model', 'setFilesystemSize', params, [])
        return res[1], res[2]

    def create_state(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "params" in params:
            raise TypeError('Invalid parameter "params": Missing parameter.')
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = self.__client._raw_method_call('Model', 'createState', new_params, data)
        return res[1], res[2]

    def upload_state(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        if not "data" in params:
            raise TypeError('Invalid parameter "data": Missing parameter.')
        if not isinstance(params["data"], list):
            raise TypeError('Invalid parameter "data": Expected a list.')
        for entry in params["data"]:
            if not isinstance(entry, dict) or not "key" in entry or not "data" in entry or not isinstance(entry["key"], str) or not isinstance(entry["data"], bytes):
                raise TypeError('Invalid parameter "data": Expected a list of dicts like { "key": str, "data": bytes }.')
        new_params = params.copy()
        del new_params["data"]
        data = [x["data"] for x in params["data"]]
        new_params["stateKeyNames"] = [x["key"] for x in params["data"]]
        res = self.__client._raw_method_call('Model', 'uploadState', new_params, data)
        return res[1], res[2]

    def get_creating_states(self, params):
        res = self.__client._raw_method_call('Model', 'getCreatingStates', params, [])
        return res[1], res[2]

    def wait_for_state_to_be_created(self, params):
        res = self.__client._raw_method_call('Model', 'waitForStateToBeCreated', params, [])
        return res[1], res[2]

    def update_model_state(self, params):
        res = self.__client._raw_method_call('Model', 'updateModelState', params, [])
        return res[1], res[2]

    def set_current_model_state(self, params):
        res = self.__client._raw_method_call('Model', 'setCurrentModelState', params, [])
        return res[1], res[2]

    def delete_model_state(self, params):
        res = self.__client._raw_method_call('Model', 'deleteModelState', params, [])
        return res[1], res[2]

    def get_model_state(self, params):
        res = self.__client._raw_method_call("Model", "getModelState", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["data"] = [{ "key": key, "data": res[3][idx] } for idx, key in enumerate(res[1]["stateKeyNames"])]
        del res[1]["stateKeyNames"]
        return res[1], res[2]

    def get_snapshot_state(self, params):
        res = self.__client._raw_method_call("Model", "getSnapshotState", params, [])
        if res[1] is None:
            return res[1], res[2]
        res[1]["data"] = [{ "key": key, "data": res[3][idx] } for idx, key in enumerate(res[1]["stateKeyNames"])]
        del res[1]["stateKeyNames"]
        return res[1], res[2]

    def train(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = self.__client._raw_method_call("Model", "train", new_params, data)
        return res[1], res[2]

    def get_training_status(self, params):
        res = self.__client._raw_method_call('Model', 'getTrainingStatus', params, [])
        return res[1], res[2]

    def get_training_metrics(self, params):
        res = self.__client._raw_method_call('Model', 'getTrainingMetrics', params, [])
        if res[1] is None:
            return res[1], res[2]
        metrics = res[1]["metrics"]
        i = 0
        for metric in metrics:
            for entry in metric["entries"]:
                entry["data"] = DecthingsTensor.deserialize(res[3][i])[0]
                i += 1
        return res[1], res[2]

    def get_training_sysinfo(self, params):
        res = self.__client._raw_method_call('Model', 'getTrainingSysinfo', params, [])
        return res[1], res[2]

    def cancel_training_session(self, params):
        res = self.__client._raw_method_call("Model", "cancelTrainingSession", params, [])
        return res[1], res[2]

    def clear_previous_training_session(self, params):
        res = self.__client._raw_method_call("Model", "clearPreviousTrainingSession", params, [])
        return res[1], res[2]

    def evaluate(self, params):
        if not isinstance(params, dict):
            raise TypeError("Invalid params: Expected a dict.")
        new_parameter_providers, data = serialize_parameter_providers(params["params"])
        new_params = params.copy()
        new_params["params"] = new_parameter_providers
        res = self.__client._raw_method_call("Model", "evaluate", new_params, data)
        if res[1] is None:
            return res[1], res[2]
        if "success" in res[1]:
            for i, param in enumerate(res[1]["success"]["output"]):
                param["data"] = DecthingsTensor.deserialize_many(res[3][i])
        return res[1], res[2]

    def get_evaluations(self, params):
        res = self.__client._raw_method_call("Model", "getEvaluations", params, [])
        return res[1], res[2]

    def get_finished_evaluation_result(self, params):
        res = self.__client._raw_method_call("Model", "getFinishedEvaluationResult", params, [])
        if res[1] is None:
            return res[1], res[2]
        if "evaluationSuccess" in res[1]:
            for i, param in enumerate(res[1]["success"]["output"]):
                param["data"] = DecthingsTensor.deserialize_many(res[3][i])
        return res[1], res[2]

    def cancel_evaluation(self, params):
        res = self.__client._raw_method_call("Model", "cancelEvaluation", params, [])
        return res[1], res[2]

    def set_used_persistent_launchers_for_evaluate(self, params):
        res = self.__client._raw_method_call("Model", "setUsedPersistentLaunchersForEvaluate", params, [])
        return res[1], res[2]

    def get_used_persistent_launchers_for_evaluate(self, params):
        res = self.__client._raw_method_call("Model", "getUsedPersistentLaunchersForEvaluate", params, [])
        return res[1], res[2]
