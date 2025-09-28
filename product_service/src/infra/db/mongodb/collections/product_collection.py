from src.domain.schemas.product.product_model import ProductModel
from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import Field
from datetime import datetime, timezone
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.infra.utils.convert_id import convert_id

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
        name = "Products"
    
    @classmethod
    def create_filter_query(
        cls,
        product_filter: ProductFilterInput,
    ) -> dict:
        
        query = {}

        if product_filter.category_id:
            query[str(cls.category_id)] = convert_id(product_filter.category_id)

        if product_filter.start_price:
            query[str(cls.price)] = {"$gte": product_filter.start_price}

        if product_filter.end_price:
            query.setdefault(str(cls.price), {})
            query[str(cls.price)]["$lte"] = product_filter.end_price
                    
        return query