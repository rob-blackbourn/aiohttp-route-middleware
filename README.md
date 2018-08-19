# aiohttp-routed-middleware

## Overview

An extension for [aiohttp](https://github.com/aio-libs/aiohttp) which provides route local middleware while remainining compatible with the existing router.

With the built in router the technique for managing route local middleware is to make nested applications.
However nested applications require a unique prefix. so the following cannot be achieved as they have the same url:

GET /post/{id} (middleware: authenticate, authorise(['post:read']))
POST /post/{id} (middleware: authenticate, authorise(['post:read:', 'post:write']))
DELETE /post/{id} (middleware: authenticate, authorise(['post:read:', 'post:write']))

This router allows a chain of middleware terminated by a handler. For example:

```python
sub_app = web.Application(router=UrlDispatcherEx())
sub_app.router.add_get('/', authenticate, authorise(['post:read']), get_posts)
sub_app.router.add_post('/', authenticate, authorise(['post:read', 'post:write']), get_posts)
sub_app.router.add_delete('/', authenticate, authorise(['post:read', 'post:write']), get_posts)
```

## Usage

### Basic

A middleware function differs from a normal request handler, in that it gets given the next handler to call.

The following example shows how to add middleware to a route.

```python
from aiohttp import web
from aiohttp_route_middleware import UrlDispatcherEx

app = web.Application(router=UrlDispatcherEx())
app.router.add_get('/', middleware1, middleware2, test)

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
```

This would print out the following:

```bash
entering middleware 1
.entering middleware 2
..entering handler
..exiting handler
.exiting middleware 2
exiting middleware 1
```

### Middleware failure

A middleware function may choose not to call the next handler; for example if there was an authentication error.

```python
from aiohttp import web
from aiohttp_route_middleware import UrlDispatcherEx

async def test(request):
    return web.Response(text="Success")

async def authenticate(request, handler):
    return web.Response(body="unauthenticated", status=401)

app = web.Application(router=UrlDispatcherEx())
app.router.add_get('/', authenticate, test)
web.run_app(app)
```

## Installation

I have no requirement to upload this package to the py store at the moment.

It can be installed directly from git in the following manner:

```bash
pip install git+git://github.com/rob-blackbourn/aiohttp-route-middleware
```

or

```bash
pip install https+git://github.com/rob-blackbourn/aiohttp-route-middleware
```

## Details

The extension provides a router `UrlDispatcherEx` which extends from the built in class `UrlDispatcher`. The class can be used in the following manner:

```python
from aiohttp_route_middleware import UrlDispatcherEx

...

app = web.Application(router=UrlDispatcherEx())
```

The extension allows multiple handlers to be specified. The handlers are called in order until a handler returns a non `None` response, at which point the response is returned and execution stops. 

An example of this might be a route to update a comment on a post, The sequence might be:
1. Authenticate the user.
2. Check the user is authorised to post a comment.
3. Fetch the post.
4. Post the comment.

```python
app.router.add_post('/comment?post_id=1234', authenticate, authorise, fetch_post, post_comment)
```

Each handler is written in the same manner as a normal handler, in that it takes a single request argument. The request argument may be modified or enriched by each handler.
