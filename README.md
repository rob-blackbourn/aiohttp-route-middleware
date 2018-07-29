# aiohttp-routed-middleware

## Overview

An extension for [aiohttp](https://github.com/aio-libs/aiohttp) which provides route local middleware

It is common for routes to require specific authentication, authorisation, and enrichment. This pckage provides such functionality.

## Usage

### Basic

The following example shows how to add middleware to a route.

```python
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
```

### Middleware failure

If a route returns something other than `None` the route fails with the given response.

```python
from aiohttp import web
from aiohttp_route_middleware import UrlDispatcherEx

async def test(request):
    return web.Response(text="Success")

async def authenticate(request):
    return web.Response(body="unauthenticated", status=401)

app = web.Application(router=UrlDispatcherEx())
app.router.add_get('/', authenticate, test)
web.run_app(app)
```

## Details

The extension provides a router `UrlDispatcherEx` which extends from the built in class `UrlDispatcher`. The class can be used in the following manner:

```python
from aiohttp_route_middleware import UrlDispatcherEx

...

app = web.Application(router=UrlDispatcherEx())
```

The extension allows multiple handlers to be specified. The handlers are called in order until a handler returns a non `None` response, at which point the response is returned and execution stops.

Each handler is written in the same manner as a normal handler, in that it takes a single request argument. The request argument may be modified or enriched by each handler.
