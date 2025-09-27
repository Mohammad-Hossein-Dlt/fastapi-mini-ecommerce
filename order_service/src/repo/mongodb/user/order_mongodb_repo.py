from src.repo.interface.user.Iorder_repo import IOrderRepo
from src.domain.schemas.order.order_model import OrderModel
from src.domain.enums import Status
from src.infra.db.mongodb.collections.order_collection import OrderCollection
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from beanie.operators import And
from src.infra.utils.convert_id import convert_id
from src.infra.exceptions.exceptions import EntityNotFoundError

class OrderMongodbRepo(IOrderRepo):
        
    async def place_order(
        self,
        order: OrderModel,
    ) -> OrderModel:
        
        # try:
        #     check_order = await self.check_order(order.user_id, order.product_id)
        # except EntityNotFoundError:
        #     check_order = None
        # finally:
            
        #     if check_order:
        #         return check_order
            
        new_order = await OrderCollection.insert(
            OrderCollection(**order.model_dump(exclude={"id"})),
        )
        
        return OrderModel.model_validate(new_order, from_attributes=True)
    
    async def get_all_orders(
        self,
        filter_order: FilterOrderInput,
    ) ->  list[OrderModel]:
        
        try:
            
            query = OrderCollection.create_query_by_filter(filter_order)
                        
            orders = await OrderCollection.find(query).to_list()
                        
            return [ OrderModel.model_validate(t, from_attributes=True) for t in orders ]
        except:
            raise EntityNotFoundError(status_code=404, message="There are no orders")
    
    async def get_order_by_id(
        self,
        order_id: str,
        user_id: str,
    ) ->  OrderModel:
        
        try:
            
            order_id = convert_id(order_id)
            user_id = convert_id(user_id)
            
            order = await OrderCollection.find_one(
                OrderCollection.id == order_id,
                OrderCollection.user_id == user_id,
            )
            return OrderModel.model_validate(order, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")
        
    async def check_order(
        self,
        user_id: str,
        product_id: str,
    ) ->  OrderModel:
        
        try:
            
            user_id = convert_id(user_id)
            product_id = convert_id(product_id)
            
            order = await OrderCollection.find_one(
                OrderCollection.user_id == user_id,
                OrderCollection.product_id == product_id,
                OrderCollection.status != Status.cancelled,
            )
            return OrderModel.model_validate(order, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")
    
    async def update_order(
        self,
        order: OrderModel,
    ) ->  OrderModel:
        
        try:
            
            await OrderCollection.find_one(
                And(
                    OrderCollection.id == order.id,
                    OrderCollection.user_id == order.user_id,
                )
            ).update(
                {
                    "$set": order.model_dump(exclude_unset=True, exclude_none=True, exclude={"id", "user_id"}),
                },
            )
                        
            return await self.get_order_by_id(order.id, order.user_id)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")
    
    async def delete_all_orders(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            
            user_id = convert_id(user_id)
            
            result = await OrderCollection.find(
                OrderCollection.user_id == user_id,
            ).delete()                
                        
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="There are no orders")
    
    async def delete_order(
        self,
        order_id: str,
        user_id: str,
    ) -> bool:
        
        try:
            
            order_id = convert_id(order_id)
            user_id = convert_id(user_id)
            
            result = await OrderCollection.find(
                OrderCollection.id == order_id,
                OrderCollection.user_id == user_id,
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")