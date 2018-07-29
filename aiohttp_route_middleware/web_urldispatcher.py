from aiohttp import web, hdrs

def _make_handler(handlers):
    async def invoke(request):
        for handler in handlers:
            response = await handler(request)
            if response is not None:
                return response
    return invoke

class UrlDispatcherEx(web.UrlDispatcher):

    def add_route(self, method, path, *handlers,
                  name=None, expect_handler=None):
        resource = self.add_resource(path, name=name)
        handler = _make_handler(handlers)
        return resource.add_route(method, handler,
                                  expect_handler=expect_handler)

    def add_head(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with method HEAD
        """
        return self.add_route(hdrs.METH_HEAD, path, *handlers, **kwargs)

    def add_options(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with method OPTIONS
        """
        return self.add_route(hdrs.METH_OPTIONS, path, *handlers, **kwargs)

    def add_get(self, path, *handlers, name=None, allow_head=True, **kwargs):
        """
        Shortcut for add_route with method GET, if allow_head is true another
        route is added allowing head requests to the same endpoint
        """
        handler = _make_handler(handlers)
        resource = self.add_resource(path, name=name)
        if allow_head:
            resource.add_route(hdrs.METH_HEAD, handler, **kwargs)
        return resource.add_route(hdrs.METH_GET, handler, **kwargs)

    def add_post(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with method POST
        """
        return self.add_route(hdrs.METH_POST, path, handlers, **kwargs)

    def add_put(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with method PUT
        """
        return self.add_route(hdrs.METH_PUT, path, handlers, **kwargs)

    def add_patch(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with method PATCH
        """
        return self.add_route(hdrs.METH_PATCH, path, handlers, **kwargs)

    def add_delete(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with method DELETE
        """
        return self.add_route(hdrs.METH_DELETE, path, handlers, **kwargs)

    def add_view(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with ANY methods for a class-based view
        """
        return self.add_route(hdrs.METH_ANY, path, handlers, **kwargs)