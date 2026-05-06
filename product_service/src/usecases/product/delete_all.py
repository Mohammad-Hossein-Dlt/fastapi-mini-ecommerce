from src.repo.interface.Iproduct_repo import IProductRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteProducts:
    
    def __init__(
        self,
        product_repo: IProductRepo,
    ):        
        self.product_repo = product_repo   
    
    async def execute(
        self,
    ) -> OperationOutput:
        
        try:
            status = await self.product_repo.delete_all()
            return OperationOutput(id=None, request="delete/all_products", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  