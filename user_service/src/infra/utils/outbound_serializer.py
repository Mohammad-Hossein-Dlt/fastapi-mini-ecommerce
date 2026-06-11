from typing import Literal

def outbound_serializer[T](
    obj: T,
    mode: Literal["http", "broker", "grpc"] = "http",
) -> dict:
    
    """Remove None values before sending HTTP requests."""
        
    if mode == "grpc" and isinstance(obj, (int, float)):
        return str(obj)
    
    if mode != "grpc" and isinstance(obj, str):
        try:
            return int(obj)
        except:
            try:
                return float(obj)
            except: ...
            
    elif isinstance(obj, bool):
        return 1 if obj else 0
    elif isinstance(obj, dict):
        _dict = dict()
        for k, v in obj.items():
            k = str(k)
            if v is not None:
                _dict.update({k: outbound_serializer(v, mode)})
        return _dict
    elif isinstance(obj, list):
        _list = list()
        for i in obj:
            if i is not None:
                _list.append(outbound_serializer(i, mode))
        return _list
    
    return obj