from sqlalchemy.orm import Session
from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.domain.schemas.order.order_model import OrderModel
from src.infra.database.postgresql.models.order_db_model import OrderDBModel
from src.models.schemas.filter.order_filter_input import OrderFilterInput
from src.infra.utils.convert_id import convert_database_id
from src.infra.exceptions.exceptions import EntityNotFoundError

class AdminPgRepo(IAdminOrderRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
    
    async def get_by_id(
        self,
        order_id: str,
    ) -> OrderModel:
        
        try:
            order_id = convert_database_id(order_id)
            order = self.db.query(
                OrderDBModel
            ).where(
                OrderDBModel.id == order_id,
            ).first()
            return OrderModel.model_validate(order, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")
    
    async def modify(
        self,
        order: OrderModel,
    ) -> OrderModel:
        
        try:
            
            to_update: dict = order.model_dump_for_db(
                exclude_none=True,
                exclude_unset=True,
                exclude={"user_id", "product_id"},
                mode="json",
            )
                                    
            self.db.query(
                OrderDBModel
            ).where(
                OrderDBModel.id == order.id
            ).update(
                to_update,
                synchronize_session='fetch',
            )
            
            self.db.commit()
                        
            return await self.get_by_id(order.id)
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")

    async def delete_by_id(
        self,
        order_id: str,
    ) -> bool:
        
        try:
            order = await self.get_by_id(order_id)
            if order:
                order = self.db.merge(OrderDBModel(**order.model_dump()))
                
            if isinstance(order, OrderDBModel):
                self.db.delete(order)
                self.db.commit()
                return True
            else:
                return False
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")

    async def get_by_criteria(
        self,
        criteria: OrderFilterInput,
    ) -> list[OrderModel]:
        
        try:
            query = OrderDBModel.create_filter_query(criteria)
            orders = self.db.execute(query).scalars().all()
            return [ OrderModel.model_validate(t, from_attributes=True) for t in orders ]
        except:
            raise EntityNotFoundError(status_code=404, message="There are no orders")
    
    async def delete_by_criteria(
        self,
        criteria: OrderFilterInput,
    ) -> bool:
        
        try:
            orders = await self.get_by_criteria(criteria)            
            if orders:
                for order in orders:
                    order = self.db.merge(OrderDBModel(**order.model_dump()))
                    if isinstance(order, OrderDBModel):
                        self.db.delete(order)
                
                self.db.commit()        
                return True 

            return False
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="There are no orders")