from aiohttp import web
from aiohttp_route_middleware import UrlDispatcherEx

async def test(request):
    return web.Response(text="Success")

@web.middleware
async def authenticate(request, handler):
    request.user = 'tom'
    return await handler(request)

@web.middleware
async def authorise(request, handler):
    if request.user == 'dick':
        return None
    return web.Response(body="unauthorised", status=403)

app = web.Application(router=UrlDispatcherEx())
app.router.add_get('/', authenticate, authorise, test)
web.run_app(app)
