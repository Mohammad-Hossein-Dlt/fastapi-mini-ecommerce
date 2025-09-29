from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.domain.schemas.order.order_model import OrderModel
from src.infra.db.postgresql.models.order_db_model import OrderDBModel
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.infra.exceptions.exceptions import EntityNotFoundError

class OrderPgRepo(IOrderRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        
    async def place_order(
        self,
        order: OrderModel,
    ) -> OrderModel:
        
        try:                        
            new_order = OrderDBModel(**order.custom_model_dump(exclude={"id"}))
            self.db.add(new_order)
            self.db.commit()
            return OrderModel.model_validate(new_order, from_attributes=True)
        except:
            self.db.rollback()
            raise
    
    async def get_all_orders(
        self,
        filter_order: FilterOrderInput,
    ) ->  list[OrderModel]:
        
        try:
            query = OrderDBModel.create_filter_query(filter_order)
            orders = self.db.execute(query).scalars().all()
        
            return [ OrderModel.model_validate(t, from_attributes=True) for t in orders ]
        except:
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="There are no orders")
    
    async def get_order_by_id(
        self,
        order_id: str,
        user_id: str,
    ) ->  OrderModel:
        
        try:
                                    
            order = self.db.query(
                OrderDBModel   
            ).where(
                and_(
                    OrderDBModel.id == order_id,
                    OrderDBModel.user_id == user_id,
                ),
            ).first()
            
            return OrderModel.model_validate(order, from_attributes=True)
        except:
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="Order not found")
        
    async def check_order(
        self,
        user_id: str,
        product_id: str,
    ) ->  OrderModel:
        
        try:         

            order = self.db.query(
                OrderDBModel   
            ).where(
                and_(
                    OrderDBModel.user_id == user_id,
                    OrderDBModel.product_id == product_id,
                ),
            ).first()
            
            return OrderModel.model_validate(order, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")
    
    async def update_order(
        self,
        order: OrderModel,
    ) ->  OrderModel:
        
        try:
            
            to_update: dict = order.custom_model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude={
                    "id",
                    "user_id",
                    "product_id",
                },
                db_stack="sql",
            )
                        
            self.db.query(
                OrderDBModel
            ).where(
                OrderDBModel.id == order.id,
            ).update(
                to_update,
                synchronize_session='fetch',
            )
            
            self.db.commit()
                        
            return await self.get_order_by_id(order.id, order.user_id)
        except EntityNotFoundError:
            raise
        except:
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="Order not found")
    
    async def delete_all_orders(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            orders = await self.get_all_orders(
                FilterOrderInput(
                    user_id=user_id,
                ),
            )
            
            if orders:
                for order in orders:
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
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="There are no orders")
    
    async def delete_order(
        self,
        order_id: str,
        user_id: str,
    ) -> bool:
        
        try:
            order = await self.get_order_by_id(order_id, user_id)
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
            self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="Order not found")