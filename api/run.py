import os
from sanic import Sanic
from sanic.response import html, stream

from utils.client import Client

app = Sanic()


@app.route("/")
async def index(request):
    return html("""<img src="/api/camera-stream/">""")


@app.route("/camera-stream/")
async def camera_stream(request):
    camera = Client()

    async def streaming_fn(response):
        async for i in camera.recv_array():
            await response.write(
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + i + b"\r\n"
            )

    return stream(
        streaming_fn, content_type="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    debug_mode = os.getenv("API_MODE", "") == "dev"

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=debug_mode,
        access_log=debug_mode,
        auto_reload=debug_mode,
    )
