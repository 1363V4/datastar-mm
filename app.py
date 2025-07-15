from sanic import Sanic

from datastar_py.sanic import datastar_response, ServerSentEventGenerator as SSE

app = Sanic("mm")
app.static('/static/', './static/')
app.static("/", "index.html", name="index")

@app.get("/init")
@datastar_response
async def init(request):
    return SSE.patch_elements("<main id='main'>ok</main>")