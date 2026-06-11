from src.infra.context.app_context import AppContext
from typing import Callable, Any

Depends: Callable[..., Any] = lambda: None
inject: Callable[..., Any] = lambda func: func

if AppContext.auth_communication_type == "broker":
    from faststream import Depends as _Depends
    Depends: Callable[..., Any] = _Depends
elif AppContext.auth_communication_type == "grpc":
    from fast_depends import Depends as _Depends, inject as _inject
    Depends = _Depends
    inject: Callable[..., Any] = _inject