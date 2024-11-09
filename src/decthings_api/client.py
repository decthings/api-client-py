import aiohttp
import typing

from .event import parse_event, DecthingsEvent, SubscriptionsRemovedEvent
from .ws import DecthingsClientWebsocket
from . import protocol
from .rpc_impl.dataset import DatasetRpc
from .rpc_impl.debug import DebugRpc
from .rpc_impl.fs import FsRpc
from .rpc_impl.language import LanguageRpc
from .rpc_impl.model import ModelRpc
from .rpc_impl.persistent_launcher import PersistentLauncherRpc
from .rpc_impl.spawned import SpawnedRpc
from .rpc_impl.terminal import TerminalRpc
from .rpc_impl.user import UserRpc

class DecthingsClient:
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
            sync=False
        )

        self.dataset = DatasetRpc(self)
        self.debug = DebugRpc(self)
        self.fs = FsRpc(self)
        self.language = LanguageRpc(self)
        self.model = ModelRpc(self)
        self.persistent_launcher = PersistentLauncherRpc(self)
        self.spawned = SpawnedRpc(self)
        self.terminal = TerminalRpc(self)
        self.user = UserRpc(self)

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

    async def _raw_method_call(
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
            response, response_data = await ws.call(api, method, params, data, self.__api_key, get_keepalive_change)
        else:
            headers: list[typing.Tuple[str, str]] = [("Content-Type", "application/octet-stream")]
            if self.__api_key is not None:
                headers.append(("Authorization", f"Bearer {self.__api_key}"))
            if self.__extra_headers is not None:
                headers.extend(self.__extra_headers)
            body = protocol.serialize_for_http(params, data)
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.__http_server_address}/{api}/{method}", data=body, headers=headers) as response:
                    response.raise_for_status()
                    response_body = await response.read()
                    response, response_data = protocol.deserialize_for_http(response_body)
        if "error" in response:
            return (True, None, response["error"], response_data)
        return (True, response["result"], None, response_data)
