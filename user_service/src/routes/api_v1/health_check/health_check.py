from ._router import router

@router.get("")
async def health_check():
    status = "Ok"
    return {
        "status": status,
    }
