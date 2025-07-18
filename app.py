from sanic import Sanic

from datastar_py.sanic import datastar_response, ServerSentEventGenerator as SSE

import asyncio
from datetime import datetime, timedelta

app = Sanic("mm")
app.static("/static/", "./static/")
app.static("/", "index.html", name="index")


SURPRISE_HTML = """
<main id="main" data-signals-screen=0>
    <div data-show="$screen == 0">hello there</div>
    <div data-show="$screen == 1">i make music</div>
    <div data-show="$screen == 2">now it is done</div>
    <a href="https://mariemalheur.bandcamp.com/album/deathless">
        <img data-show="$screen == 3" src="/static/img/cover_final.png"/>
    </a>
    <div class="normal">
        <p data-show="$screen == 0">i have something to tell you</p>
        <p data-show="$screen == 1">and i have been working on a new album</p>
        <p data-show="$screen == 2">i really hope you will like it <3</p>
        <button data-on-click__viewTransition="$screen += 1" data-show="$screen < 3">Next</button>
    </div>                                                                  
</main>
"""


@app.get("/init")
@datastar_response
async def init(request):
    release = datetime(2025, 7, 18, 23, 59, 59)
    current_time = datetime.now()
    while current_time < release:
        time_difference = release - current_time
        time_difference_str = str(timedelta(seconds=time_difference.seconds))
        yield SSE.patch_elements(
            f'<main id="main"><div>{time_difference_str}</div></main>'
        )
        await asyncio.sleep(1)
        current_time = datetime.now()
    else:
        yield SSE.patch_elements(SURPRISE_HTML)
