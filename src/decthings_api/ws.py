import asyncio
import threading
import typing
import queue
from websockets.client import WebSocketClientProtocol as Ws, connect as ws_connect
from websockets.sync.client import ClientConnection as WsSync, connect as ws_connect_sync

from . import protocol

class DecthingsClientConnectedWebsocket:
    def __init__(
        self,
        ws_server_address: str,
        extra_headers: list[typing.Tuple[str, str]] | None,
        on_event: typing.Callable[[typing.Any, list[bytes]], None],
        on_subscriptions_removed: typing.Callable[[], None],
        on_disposed: typing.Callable[[], None]
    ):
        self.keep_alive: set[str] = set()
        self.ws_server_address = ws_server_address
        self.extra_headers = extra_headers
        self.on_event = on_event
        self.on_subscriptions_removed = on_subscriptions_removed
        self.on_disposed = on_disposed
        self.disposed = False

        self.id_counter = 0
        self.waiting_for_responses: typing.Dict[int, typing.Tuple[typing.Callable[[typing.Any, list[bytes]], None], typing.Callable[[typing.Any], None]]] = {}

        self.socket: Ws | None = None
        self.socket_queue: list[asyncio.Queue[Ws]] = []
        self.socket_sync: WsSync | None = None
        self.socket_queue_sync: list[queue.Queue[WsSync]] = []

    def handle_data(self, data: str | bytes):
        if isinstance(data, str):
            data = data.encode()
        maybe_response, maybe_event, data_list = protocol.deserialize_for_ws(data)
        if maybe_response is not None:
            id, response = maybe_response
            if not id in self.waiting_for_responses:
                return
            cb = self.waiting_for_responses[id]
            del self.waiting_for_responses[id]
            cb[0](response, data_list)

        if maybe_event is not None:
            self.on_event(maybe_event, data_list)

    async def run(self):
        try:
            self.socket = await ws_connect(self.ws_server_address, extra_headers=self.extra_headers)
            for q in self.socket_queue:
                q.put_nowait(self.socket)

            while True:
                data = await self.socket.recv()
                self.handle_data(data)
        except Exception as e:
            if self.disposed:
                return
            for id in self.waiting_for_responses:
                self.waiting_for_responses[id][1](e)
            self.waiting_for_responses = {}
            self.dispose()


    def run_sync(self):
        try:
            self.socket_sync = ws_connect_sync(self.ws_server_address, additional_headers=self.extra_headers)
            for q in self.socket_queue_sync:
                q.put_nowait(self.socket_sync)

            while True:
                data = self.socket_sync.recv()
                self.handle_data(data)
        except Exception as e:
            if self.disposed:
                return
            for id in self.waiting_for_responses:
                self.waiting_for_responses[id][1](e)
            self.waiting_for_responses = {}
            self.dispose()

    def call(
        self,
        api: str,
        method: str,
        params: typing.Any,
        data: list[bytes],
        api_key: str | None,
        get_keepalive_change: typing.Callable[[typing.Any | None, typing.Any | None], typing.Tuple[list[str], list[str]]] | None
    ) -> typing.Coroutine[typing.Any, typing.Any, typing.Tuple[typing.Any, list[bytes]]]:
        id = self.id_counter
        self.id_counter += 1

        response_queue: asyncio.Queue[Exception | typing.Tuple[typing.Any, list[bytes]]] = asyncio.Queue(maxsize = 1)
        def on_response(params, data):
            response_queue.put_nowait((params, data))
            del self.waiting_for_responses[id]
        def on_error(e):
            response_queue.put_nowait(e)
            del self.waiting_for_responses[id]
        self.waiting_for_responses[id] = (on_response, on_error)

        async def inner():
            if self.socket is None:
                q: asyncio.Queue[Ws] = asyncio.Queue(maxsize = 1)
                self.socket_queue.append(q)
                socket = await q.get()
            else:
                socket = self.socket
            serialized = protocol.serialize_for_websocket(id, { "api": api, "method": method, "apiKey": api_key, "params": params }, data)
            await socket.send(serialized)

            res = await response_queue.get()

            if isinstance(res, Exception):
                raise(res)

            if get_keepalive_change is not None:
                add_to_keepalive, remove_from_keepalive = get_keepalive_change(res[0], res[1])
                for remove in remove_from_keepalive:
                    self.keep_alive.remove(remove)
                for add in add_to_keepalive:
                    self.keep_alive.add(add)
            self.dispose_if_unused()
            return res

        return inner()

    def call_sync(
        self,
        api: str,
        method: str,
        params: typing.Any,
        data: list[bytes],
        api_key: str | None,
        get_keepalive_change: typing.Callable[[typing.Any | None, typing.Any | None], typing.Tuple[list[str], list[str]]] | None
    ) -> typing.Tuple[typing.Any, list[bytes]]:
        id = self.id_counter
        self.id_counter += 1

        response_queue: queue.Queue[Exception | typing.Tuple[typing.Any, list[bytes]]] = queue.Queue(maxsize = 1)
        def on_response(params, data):
            response_queue.put_nowait((params, data))
            del self.waiting_for_responses[id]
        def on_error(e):
            response_queue.put_nowait(e)
            del self.waiting_for_responses[id]
        self.waiting_for_responses[id] = (on_response, on_error)

        if self.socket_sync is None:
            q: queue.Queue[WsSync] = queue.Queue(maxsize = 1)
            self.socket_queue_sync.append(q)
            socket = q.get()
        else:
            socket = self.socket_sync
        serialized = protocol.serialize_for_websocket(id, { "api": api, "method": method, "apiKey": api_key, "params": params }, data)
        socket.send(serialized)

        res = response_queue.get()
        if isinstance(res, Exception):
            raise res

        if get_keepalive_change is not None:
            add_to_keepalive, remove_from_keepalive = get_keepalive_change(res[0], res[1])
            for remove in remove_from_keepalive:
                self.keep_alive.remove(remove)
            for add in add_to_keepalive:
                self.keep_alive.add(add)
        self.dispose_if_unused()
        return res

    def dispose(self):
        self.disposed = True
        if self.socket is not None:
            asyncio.create_task(self.socket.close())
        elif self.socket_sync is not None:
            self.socket_sync.close()

        if len(self.keep_alive) != 0:
            self.on_subscriptions_removed()
        self.on_disposed()

    def dispose_if_unused(self):
        if len(self.keep_alive) == 0 and len(self.waiting_for_responses) == 0:
            self.dispose()


class DecthingsClientWebsocket:
    def __init__(
        self,
        ws_server_address: str,
        extra_headers: list[typing.Tuple[str, str]] | None,
        on_event: typing.Callable[[typing.Any, list[bytes]], None],
        on_subscriptions_removed: typing.Callable[[], None],
        sync: bool
    ):
        self.ws: DecthingsClientConnectedWebsocket | None = None
        self.ws_server_address = ws_server_address
        self.extra_headers = extra_headers
        self.on_event = on_event
        self.on_subscriptions_removed = on_subscriptions_removed
        self.sync = sync

    def add_keep_alive(self, id: str):
        if self.ws is None:
            return
        self.ws.keep_alive.add(id)

    def remove_keep_alive(self, id: str):
        if self.ws is None:
            return
        self.ws.keep_alive.remove(id)
        self.ws.dispose_if_unused()

    def maybe_get_socket(self):
        return self.ws
    
    def get_or_create_socket(self):
        if self.ws is None:
            def on_disposed():
                self.ws = None

            self.ws = DecthingsClientConnectedWebsocket(
                self.ws_server_address,
                self.extra_headers,
                self.on_event,
                self.on_subscriptions_removed,
                on_disposed
            )
            if self.sync:
                thread = threading.Thread(target = self.ws.run_sync)
                thread.start()
            else:
                asyncio.create_task(self.ws.run())

        return self.ws
    
    def dispose(self):
        if self.ws is None:
            return
        self.ws.dispose()
