from aiohttp import web
from aiohttp_route_middleware import UrlDispatcherEx

async def test(request):
    return web.Response(text=f"extra_stuff=[{', '.join(request.extra_stuff)}]")

async def middleware1(request):
    request.extra_stuff = ['foo']
    return None

async def middleware2(request):
    request.extra_stuff.append('bar')
    return None

app = web.Application(router=UrlDispatcherEx())
app.router.add_get('/', middleware1, middleware2, test)
web.run_app(app)
