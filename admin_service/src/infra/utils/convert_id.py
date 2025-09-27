from bson.objectid import ObjectId

def convert_id(
    _id: str | None,
) -> ObjectId | int | str | None:
    
    if not _id:
        return None
    
    try:
        return ObjectId(_id)
    except:
        pass
    
    try:
        return int(_id)
    except:
        pass
        
    try:
        return str(_id)
    except:
        pass
    
    return None