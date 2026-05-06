from src.domain.schemas.product.product_model import ProductModel
from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import Field
from datetime import datetime, timezone
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.infra.utils.convert_id import convert_database_id

class ProductCollection(ProductModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    category_id: int | PydanticObjectId | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "Product"
    
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