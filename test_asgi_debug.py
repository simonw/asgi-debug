from asgiref.testing import ApplicationCommunicator
from asgi_debug import asgi_debug
import pytest


async def hello_world_app(scope, receive, send):
    assert scope["type"] == "http"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"application/json"]],
        }
    )
    await send({"type": "http.response.body", "body": b'{"hello": "world"}'})


@pytest.mark.asyncio
async def test_asgi_debug():
    captured = []
    app = asgi_debug(hello_world_app, log_to=captured.append)
    instance = ApplicationCommunicator(
        app, {"type": "http", "http_version": "1.0", "method": "GET", "path": "/"}
    )
    await instance.send_input({"type": "http.request"})
    assert (await instance.receive_output(1)) == {
        "type": "http.response.start",
        "status": 200,
        "headers": [[b"content-type", b"application/json"]],
    }
    assert (await instance.receive_output(1)) == {
        "type": "http.response.body",
        "body": b'{"hello": "world"}',
    }
    assert [
        "{'http_version': '1.0', 'method': 'GET', 'path': '/', 'type': 'http'}",
        "{'headers': [[b'content-type', b'application/json']],\n 'status': 200,\n 'type': 'http.response.start'}",
        "{'body': b'{\"hello\": \"world\"}', 'type': 'http.response.body'}",
    ] == captured
