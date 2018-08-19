from aiohttp import web
from aiohttp_route_middleware import UrlDispatcherEx

async def test(request):
    print("..entering handler")
    response = web.Response(text=f"extra_stuff=[{', '.join(request.extra_stuff)}]")
    print("..exiting handler")
    return response

async def middleware1(request, handler):
    print("entering middleware 1")
    request.extra_stuff = ['foo']
    response = await handler(request)
    print("exiting middleware 1")
    return response

async def middleware2(request, handler):
    print(".entering middleware 2")
    request.extra_stuff.append('bar')
    response = await handler(request)
    print(".exiting middleware 2")
    return response

app = web.Application(router=UrlDispatcherEx())
app.router.add_get('/', middleware1, middleware2, test)
web.run_app(app)
