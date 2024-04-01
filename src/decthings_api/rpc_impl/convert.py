import typing

from decthings_api.tensor import DecthingsTensor

def serialize_parameter_providers(params: typing.Any) -> typing.Tuple[list[typing.Dict], list[bytes]]:
    if not isinstance(params, list):
        raise TypeError("Invalid ParameterProviders: Expected a list.")
    new_params: list[typing.Dict] = []
    data: list[bytes] = []
    for param in params:
        if not isinstance(param, dict):
            raise TypeError("Invalid ParameterProviders: Expected each parameter to be a dict.")
        if not "data" in param:
            raise TypeError("Invalid ParameterProviders: Expected each parameter to have an entry \"data\".")
        if isinstance(param["data"], list):
            new_param = param.copy()
            del new_param["data"]
            new_params.append(new_param)

            serialized = []
            for x in param["data"]:
                if not isinstance(x, DecthingsTensor):
                    raise TypeError('Invalid ParameterProviders: Expected each elements of the field "data" to be an instance of DecthingsTensor.')
                serialized.append(x.serialize())
            data.append(b''.join(serialized))
        else:
            if not isinstance(param["data"], dict):
                raise TypeError("Invalid ParameterProviders: Expected each parameter to be a list or dict.")
            if not "type" in param["data"] or param["data"]["type"] != "dataset":
                raise TypeError(
                        'Invalid ParameterProviders: Expected the field "data" of each element to be a list or a dict like { "type": "dataset", "datasetId": "<datasetid>", "datasetKey": "<datasetkey>" }.'
                )
            new_params.append(param)
    return (new_params, data)
