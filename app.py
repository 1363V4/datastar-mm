from sanic import Sanic

from datastar_py.sanic import datastar_response, ServerSentEventGenerator as SSE

import asyncio
from datetime import datetime, timedelta

app = Sanic("mm")
app.static('/static/', './static/')
app.static("/", "index.html", name="index")

@app.get("/init")
@datastar_response
async def init(request):
    release = datetime(2025, 7, 18, 23, 59, 59)
    current_time = datetime.now()
    while current_time < release:
        time_difference = release - current_time
        time_difference_str = str(timedelta(seconds=time_difference.seconds))
        yield SSE.patch_elements(f'<main id="main"><div>{time_difference.days}d {time_difference_str}</div></main>')
        await asyncio.sleep(1)
        current_time = datetime.now()
    else:
        yield SSE.patch_elements(f'<main id="main"><div>???</div></main>')
