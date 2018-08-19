from aiohttp import web
from aiohttp_route_middleware import UrlDispatcherEx

async def test(request):
    return web.Response(text="Success")

async def authenticate(request, handler):
    return web.Response(body="unauthenticated", status=401)

app = web.Application(router=UrlDispatcherEx())
app.router.add_get('/', authenticate, test)
web.run_app(app)
