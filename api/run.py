import os
from sanic import Sanic
from sanic.response import html, stream

from utils.camera import Camera

app = Sanic()


@app.route("/")
async def index(request):
    return html("""<img src="/api/camera-stream/">""")


@app.route("/camera-stream/")
async def camera_stream(request):
    camera = Camera()
    return stream(
        camera.stream, content_type="multipart/x-mixed-replace; boundary=frame"
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
