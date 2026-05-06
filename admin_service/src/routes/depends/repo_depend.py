from fastapi import Request, Response
from src.repo.interface.Iauth_repo import IAuthRepo
from src.repo.registry.auth_registry_repo import AuthRegistryRepo

def auth_repo_depend(
    request: Request,
    response: Response,
) -> IAuthRepo:
    
    return AuthRegistryRepo(request, response)