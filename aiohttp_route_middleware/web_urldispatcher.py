import logging
logger = logging.getLogger(__name__)

from functools import partial
from aiohttp import web, hdrs


def _prepare_middleware(middlewares):
    for middleware in middlewares:
        if getattr(middleware, '__middleware_version__', None) == 1:
            yield middleware, True
        else:
            logger.warn(
                'old-style middleware "{!r}" deprecated'.format(middleware))
            yield middleware, False


def _make_middleware_handler(middleware, handler):
    async def invoke(request):
        return await middleware(request, handler)
    return invoke


def _make_handler(handlers):

    reverse_handlers = reversed(handlers)
    handler = next(reverse_handlers)
    for middleware, new_style in _prepare_middleware(reverse_handlers):
        if new_style:
            handler = partial(middleware, handler=handler)
        else:
            handler = _make_middleware_handler(middleware, handler)
    return handler


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
        return self.add_route(hdrs.METH_POST, path, *handlers, **kwargs)

    def add_put(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with method PUT
        """
        return self.add_route(hdrs.METH_PUT, path, *handlers, **kwargs)

    def add_patch(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with method PATCH
        """
        return self.add_route(hdrs.METH_PATCH, path, *handlers, **kwargs)

    def add_delete(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with method DELETE
        """
        return self.add_route(hdrs.METH_DELETE, path, *handlers, **kwargs)

    def add_view(self, path, *handlers, **kwargs):
        """
        Shortcut for add_route with ANY methods for a class-based view
        """
        return self.add_route(hdrs.METH_ANY, path, *handlers, **kwargs)
