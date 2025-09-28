from src.repo.interface.admin.Iorder_repo import IAdminOrderRepo
from src.domain.schemas.order.order_model import OrderModel
from src.infra.db.mongodb.collections.order_collection import OrderCollection
from src.models.schemas.filter.filter_order_input import FilterOrderInput
from src.infra.utils.convert_id import convert_id
from src.infra.exceptions.exceptions import EntityNotFoundError

class AdminOrderMongodbRepo(IAdminOrderRepo):
        
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
    ) ->  OrderModel:
        
        try:
            order_id = convert_id(order_id)
            order = await OrderCollection.find_one(
                OrderCollection.id == order_id,
            )
            
            return OrderModel.model_validate(order, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")
    
    async def modify_order(
        self,
        order: OrderModel,
    ) ->  OrderModel:
        
        try:
            
            await OrderCollection.find(
                OrderCollection.id == order.id,
            ).update(
                {
                    "$set": order.model_dump(exclude_unset=True, exclude_none=True, exclude={"id", "user_id"}),
                },
            )
                        
            return await self.get_order_by_id(order.id)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")
    
    async def delete_all_orders(
        self,
        filter_order: FilterOrderInput,
    ) -> bool:
        
        try:
            query = OrderCollection.create_query_by_filter(filter_order)
            result = await OrderCollection.find(query).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="There are no orders")
    
    async def delete_order(
        self,
        order_id: str,
    ) -> bool:
        
        try:
            
            order_id = convert_id(order_id)
            
            result = await OrderCollection.find(
                OrderCollection.id == order_id,
            ).delete()    
                        
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")