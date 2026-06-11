import grpc


REST_TO_GRPC_MAP = {
    # 1xx
    100: grpc.StatusCode.OK,
    101: grpc.StatusCode.OK,
    102: grpc.StatusCode.OK,
    103: grpc.StatusCode.OK,

    # 2xx
    200: grpc.StatusCode.OK,
    201: grpc.StatusCode.OK,
    202: grpc.StatusCode.OK,
    203: grpc.StatusCode.OK,
    204: grpc.StatusCode.OK,
    205: grpc.StatusCode.OK,
    206: grpc.StatusCode.OK,
    207: grpc.StatusCode.OK,
    208: grpc.StatusCode.OK,
    226: grpc.StatusCode.OK,

    # 3xx
    300: grpc.StatusCode.OK,
    301: grpc.StatusCode.OK,
    302: grpc.StatusCode.OK,
    303: grpc.StatusCode.OK,
    304: grpc.StatusCode.OK,
    305: grpc.StatusCode.OK,
    307: grpc.StatusCode.OK,
    308: grpc.StatusCode.OK,

    # 4xx
    400: grpc.StatusCode.INVALID_ARGUMENT,
    401: grpc.StatusCode.UNAUTHENTICATED,
    402: grpc.StatusCode.UNKNOWN,
    403: grpc.StatusCode.PERMISSION_DENIED,
    404: grpc.StatusCode.NOT_FOUND,
    405: grpc.StatusCode.UNIMPLEMENTED,
    406: grpc.StatusCode.INVALID_ARGUMENT,
    407: grpc.StatusCode.UNAUTHENTICATED,
    408: grpc.StatusCode.DEADLINE_EXCEEDED,
    409: grpc.StatusCode.ALREADY_EXISTS,
    410: grpc.StatusCode.NOT_FOUND,
    411: grpc.StatusCode.INVALID_ARGUMENT,
    412: grpc.StatusCode.FAILED_PRECONDITION,
    413: grpc.StatusCode.OUT_OF_RANGE,
    414: grpc.StatusCode.INVALID_ARGUMENT,
    415: grpc.StatusCode.INVALID_ARGUMENT,
    416: grpc.StatusCode.OUT_OF_RANGE,
    417: grpc.StatusCode.FAILED_PRECONDITION,
    418: grpc.StatusCode.UNKNOWN,
    421: grpc.StatusCode.FAILED_PRECONDITION,
    422: grpc.StatusCode.FAILED_PRECONDITION,
    423: grpc.StatusCode.FAILED_PRECONDITION,
    424: grpc.StatusCode.FAILED_PRECONDITION,
    425: grpc.StatusCode.FAILED_PRECONDITION,
    426: grpc.StatusCode.FAILED_PRECONDITION,
    428: grpc.StatusCode.FAILED_PRECONDITION,
    429: grpc.StatusCode.RESOURCE_EXHAUSTED,
    431: grpc.StatusCode.INVALID_ARGUMENT,
    451: grpc.StatusCode.PERMISSION_DENIED,

    # 5xx
    500: grpc.StatusCode.INTERNAL,
    501: grpc.StatusCode.UNIMPLEMENTED,
    502: grpc.StatusCode.UNAVAILABLE,
    503: grpc.StatusCode.UNAVAILABLE,
    504: grpc.StatusCode.DEADLINE_EXCEEDED,
    505: grpc.StatusCode.UNIMPLEMENTED,
    506: grpc.StatusCode.INTERNAL,
    507: grpc.StatusCode.RESOURCE_EXHAUSTED,
    508: grpc.StatusCode.INTERNAL,
    510: grpc.StatusCode.UNIMPLEMENTED,
    511: grpc.StatusCode.UNAUTHENTICATED,
}

GRPC_TO_REST_MAP = {
    grpc.StatusCode.OK: 200,
    grpc.StatusCode.CANCELLED: 499,
    grpc.StatusCode.UNKNOWN: 500,
    grpc.StatusCode.INVALID_ARGUMENT: 400,
    grpc.StatusCode.DEADLINE_EXCEEDED: 504,
    grpc.StatusCode.NOT_FOUND: 404,
    grpc.StatusCode.ALREADY_EXISTS: 409,
    grpc.StatusCode.PERMISSION_DENIED: 403,
    grpc.StatusCode.RESOURCE_EXHAUSTED: 429,
    grpc.StatusCode.FAILED_PRECONDITION: 412,
    grpc.StatusCode.ABORTED: 409,
    grpc.StatusCode.OUT_OF_RANGE: 416,
    grpc.StatusCode.UNIMPLEMENTED: 501,
    grpc.StatusCode.INTERNAL: 500,
    grpc.StatusCode.UNAVAILABLE: 503,
    grpc.StatusCode.DATA_LOSS: 500,
    grpc.StatusCode.UNAUTHENTICATED: 401,
}

def rest_to_grpc_status(rest_code: int) -> grpc.StatusCode:
    return REST_TO_GRPC_MAP.get(rest_code, grpc.StatusCode.UNKNOWN)

def grpc_to_rest_status(grpc_code) -> int:
    return GRPC_TO_REST_MAP.get(grpc_code, 500)