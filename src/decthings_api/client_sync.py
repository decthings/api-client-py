import requests
import typing
from .event import parse_event, DecthingsEvent, SubscriptionsRemovedEvent
from .ws import DecthingsClientWebsocket
from . import protocol
from .rpc_impl.dataset import DatasetRpcSync
from .rpc_impl.debug import DebugRpcSync
from .rpc_impl.fs import FsRpcSync
from .rpc_impl.language import LanguageRpcSync
from .rpc_impl.model import ModelRpcSync
from .rpc_impl.persistent_launcher import PersistentLauncherRpcSync
from .rpc_impl.spawned import SpawnedRpcSync
from .rpc_impl.terminal import TerminalRpcSync
from .rpc_impl.user import UserRpcSync

class DecthingsClientSync:
    def __init__(
        self,
        api_key: str | None = None,
        http_server_address: str = "https://api.decthings.com/v0",
        ws_server_address: str = "wss://api.decthings.com/v0/ws",
        extra_headers: list[typing.Tuple[str, str]] | None = None,
    ):
        self.closed = False
        self.__api_key = api_key
        self.__http_server_address = http_server_address
        self.__extra_headers = extra_headers

        self.__event_listeners: typing.Dict[int, typing.Callable[[DecthingsEvent], None]] = {}

        def remove_keepalive(id: str):
            self.ws.remove_keep_alive(id)

        def on_event(ev: typing.Dict, data: list[bytes]):
            parsed = parse_event(ev, data, remove_keepalive)
            if parsed is None:
                return
            for listener in self.__event_listeners:
                self.__event_listeners[listener](parsed)

        def on_subscriptions_removed():
            ev = SubscriptionsRemovedEvent()
            for listener in self.__event_listeners:
                self.__event_listeners[listener](ev)

        self.ws = DecthingsClientWebsocket(
            ws_server_address=ws_server_address,
            extra_headers=extra_headers,
            on_event=on_event,
            on_subscriptions_removed=on_subscriptions_removed,
            sync=True
        )

        self.dataset = DatasetRpcSync(self)
        self.debug = DebugRpcSync(self)
        self.fs = FsRpcSync(self)
        self.language = LanguageRpcSync(self)
        self.model = ModelRpcSync(self)
        self.persistent_launcher = PersistentLauncherRpcSync(self)
        self.spawned = SpawnedRpcSync(self)
        self.terminal = TerminalRpcSync(self)
        self.user = UserRpcSync(self)

    def on_event(self, cb: typing.Callable[[DecthingsEvent], None]) -> typing.Callable[[], None]:
        id = 0
        while id in self.__event_listeners:
            id += 1
        self.__event_listeners[id] = cb
        
        def dispose():
            del self.__event_listeners[id]

        return dispose

    def close(self):
        self.closed = True
        self.ws.dispose()

    def _raw_method_call(
        self,
        api: str,
        method: str,
        params: typing.Any,
        data: list[bytes],
        mode: typing.Literal["http", "ws", "wsIfAvailableOtherwiseNone"] = "http",
        get_keepalive_change: typing.Callable[[typing.Any | None, typing.Any | None], typing.Tuple[list[str], list[str]]] | None = None
    ) -> typing.Tuple[bool, typing.Any | None, typing.Any | None, list[bytes]]:
        if self.closed:
            raise Exception("DecthingsClient was closed")
        if mode == "ws":
            ws = self.ws.get_or_create_socket()
        elif mode == "wsIfAvailableOtherwiseNone":
            ws = self.ws.maybe_get_socket()
            if ws is None:
                return (True, None, None, [])
        else:
            ws = None
        if ws is not None:
            response, response_data = ws.call_sync(api, method, params, data, self.__api_key, get_keepalive_change)
        else:
            headers: typing.Dict[str, str] = { "Content-Type": "application/octet-stream" }
            if not self.__api_key is None:
                headers["Authorization"] = f"Bearer {self.__api_key}"
            if not self.__extra_headers is None:
                for header in self.__extra_headers:
                    headers[header[0]] = header[1]
            body = protocol.serialize_for_http(params, data)
            response = requests.post(f"{self.__http_server_address}/{api}/{method}", data=body, headers=headers)
            response.raise_for_status()
            response_body = response.content
            response, response_data = protocol.deserialize_for_http(response_body)
        if "error" in response:
            return (True, None, response["error"], response_data)
        return (True, response["result"], None, response_data)
