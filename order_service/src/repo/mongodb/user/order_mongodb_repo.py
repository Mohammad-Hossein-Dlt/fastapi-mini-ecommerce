from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.domain.schemas.order.order_model import OrderModel
from src.infra.database.mongodb.collections.order_collection import OrderCollection
from src.models.schemas.filter.order_filter_input import OrderFilterInput
from src.infra.utils.convert_id import convert_database_id
from src.infra.exceptions.exceptions import EntityNotFoundError
from beanie.operators import And

class OrderMongodbRepo(IOrderRepo):
        
    async def create(
        self,
        order: OrderModel,
    ) -> OrderModel:
        
        try:
            new_order = await OrderCollection.insert(
                OrderCollection(**order.model_dump_for_db(dump_for="create")),
            )
            return OrderModel.model_validate(new_order, from_attributes=True)
        except:
            raise
        
    async def get_by_id(
        self,
        order_id: str,
    ) -> OrderModel:
        
        try:
            order_id = convert_database_id(order_id)
            order = await OrderCollection.find_one(
                OrderCollection.id == order_id,
            )
            return OrderModel.model_validate(order, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")    
    
    async def get_by_id_and_user_id(
        self,
        order_id: str,
        user_id: str,
    ) -> OrderModel:
                
        try:
            order_id = convert_database_id(order_id)
            user_id = convert_database_id(user_id) 
            order = await OrderCollection.find_one(
                And(
                    OrderCollection.id == order_id,
                    OrderCollection.user_id == user_id,
                ),
            )
            return OrderModel.model_validate(order, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")

    async def update(
        self,
        order: OrderModel,
    ) -> OrderModel:
        
        try:
                        
            to_update: dict = order.model_dump_for_db(
                dump_for="update",
                exclude_none=True,
                exclude_unset=True,
                exclude={"user_id", "product_id"},
            )
            
            await OrderCollection.find_one(
                And(
                    OrderCollection.id == order.id,
                    OrderCollection.user_id == order.user_id,
                ),
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_id_and_user_id(order.id, order.user_id)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")
    
    async def delete_by_id(
        self,
        order_id: str,
        user_id: str,
    ) -> bool:
        
        try:
            order_id = convert_database_id(order_id)
            user_id = convert_database_id(user_id)
            result = await OrderCollection.find(
                OrderCollection.id == order_id,
            ).delete()
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")
        
    async def get_by_criteria(
        self,
        criteria: OrderFilterInput,
    ) -> list[OrderModel]:
        
        try:
            query = OrderCollection.create_filter_query(criteria)   
            orders = await OrderCollection.find(query).to_list()            
            return [ OrderModel.model_validate(t, from_attributes=True) for t in orders ]
        except:
            raise EntityNotFoundError(status_code=404, message="There are no orders")
        
    async def delete_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            user_id = convert_database_id(user_id)
            result = await OrderCollection.find(
                OrderCollection.user_id == user_id,
            ).delete()                
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="There are no orders")
    