from functools import wraps
from inspect import isclass
from typing import Callable, Type, TypeVar, Union
from fastapi import Request, Depends, Security
from core.exceptions import UnauthorizedException, ForbiddenException

T = TypeVar("T")

class Auth:
    def __init__(self, permissions=None):
        self.permissions = permissions

    def __call__(self, target: Union[Type[T], Callable]) -> Union[Type[T], Callable]:
        return self._wrap_class_methods(target) if isclass(target) else self._wrap_function(target)

    def _wrap_class_methods(self, cls):
        original_init = cls.__init__

        @wraps(original_init)
        def wrapped_init(self_instance, *args, **kwargs):
            self_instance._class_permissions = self.permissions
            original_init(self_instance, *args, **kwargs)

        cls.__init__ = wrapped_init

        if hasattr(cls, "_register_routes"):
            original_register_routes = cls._register_routes

            @wraps(original_register_routes)
            def wrapped_register_routes(self_instance):
                self_instance.router.add_api_route = self._add_route_dependencies(self_instance.router.add_api_route)
                original_register_routes(self_instance)

            cls._register_routes = wrapped_register_routes

        return cls

    def _wrap_function(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from either kwargs or args
            request = kwargs.get("req") or next((arg for arg in args if isinstance(arg, Request)), None)
            if not request:
                raise RuntimeError("Request object is missing.")
            
            user = await self._authentication_dependency(request)

            if self.permissions:
                self._check_permissions(user)

            return await func(*args, **kwargs)

        return wrapper

    def _add_route_dependencies(self, original_add_api_route):
        def patched_add_api_route(path, endpoint, **kwargs):
            dependencies = kwargs.get("dependencies", [])
            if dependencies is None:
                dependencies = []

            dependencies.append(Depends(self._authentication_dependency))  #
            if self.permissions:
                dependencies.append(Security(self._authorization_dependency()))  

            kwargs["dependencies"] = dependencies
            return original_add_api_route(path, endpoint, **kwargs)

        return patched_add_api_route


    async def _authentication_dependency(self, request: Request):
        user = request.state.user
        if not user:
            raise ForbiddenException("Invalid token.")
        return user

    def _authorization_dependency(self):
        async def check_permissions(user: dict = Depends(self._authentication_dependency)):
            self._check_permissions(user)
        return check_permissions

    def _check_permissions(self, user):
        if self.permissions and not all(p in user.get("permissions", []) for p in self.permissions):
            raise UnauthorizedException("You do not have permission to access this resource.")
