import typing

class DecthingsEvent:
    pass

class SubscriptionsRemovedEvent(DecthingsEvent):
    pass

class RpcEvent(DecthingsEvent):
    def __init__(self, api: str, event_name: str, data: typing.Dict):
        self.api = api
        self.event_name = event_name
        self.data = data

def parse_event(
    event: typing.Dict,
    data: list[bytes],
    remove_keepalive: typing.Callable[[str], None]
) -> DecthingsEvent:
    api = event["api"]
    event_name = event["event"]
    params = event["params"]
    
    if api == "Debug":
        if event_name == "exit":
            remove_keepalive(params["debugSessionId"])
        elif event_name == "stdout" or event_name == "stderr" or event_name == "remoteInspectorData":
            params["data"] = data[0]
    elif api == "Language":
        if event_name == "exit":
            remove_keepalive(params["languageServerId"])
        elif event_name == "data":
            params["data"] = data[0]
    elif api == "Spawned":
        if event_name == "exit":
            remove_keepalive(params["spawnedCommandId"])
        elif event_name == "stdout" or event_name == "stderr":
            params["data"] = data[0]
    elif api == "Terminal":
        if event_name == "exit":
            remove_keepalive(params["spawnedCommandId"])
        elif event_name == "stdout" or event_name == "stderr":
            params["data"] = data[0]

    return RpcEvent(api, event_name, params)
