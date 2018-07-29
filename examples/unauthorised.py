from aiohttp import web
from aiohttp_route_middleware import UrlDispatcherEx

async def test(request):
    return web.Response(text="Success")

async def authenticate(request):
    request.user = 'tom'
    return None

async def authorise(request):
    if request.user == 'dick':
        return None
    return web.Response(body="unauthorised", status=403)

app = web.Application(router=UrlDispatcherEx())
app.router.add_get('/', authenticate, authorise, test)
web.run_app(app)
