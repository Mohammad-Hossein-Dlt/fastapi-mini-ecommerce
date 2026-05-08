from src.domain.schemas.product.product_model import ProductModel
from src.models.schemas.filter.product_filter_input import ProductFilterInput
from src.infra.utils.convert_id import convert_database_id
from beanie import Document, PydanticObjectId, before_event, Update
from datetime import datetime, timezone

class ProductCollection(ProductModel, Document):
    
    id: PydanticObjectId = None
    category_id: int | PydanticObjectId | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    
    class Settings:
        name = "Product"
        
    @before_event(Update)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
    
    @classmethod
    def create_filter_query(
        cls,
        criteria: ProductFilterInput,
    ) -> dict:
        
        query = {}

        if criteria.category_id:
            query[str(cls.category_id)] = convert_database_id(criteria.category_id)

        if criteria.start_price:
            query[str(cls.price)] = {"$gte": criteria.start_price}

        if criteria.end_price:
            query.setdefault(str(cls.price), {})
            query[str(cls.price)]["$lte"] = criteria.end_price
                    
        return query