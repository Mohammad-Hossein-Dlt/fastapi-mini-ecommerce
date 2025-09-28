from src.repo.interface.Iproduct_repo import IProductRepo
from src.domain.schemas.product.product_model import ProductModel
from src.infra.db.mongodb.collections.product_collection import ProductCollection
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.infra.exceptions.exceptions import EntityNotFoundError
from src.infra.utils.convert_id import convert_id

class ProductMongodbRepo(IProductRepo):
        
    async def insert_product(
        self,
        product: ProductModel,
    ) -> ProductModel:
        
        new_product = await ProductCollection.insert(
            ProductCollection(**product.model_dump(exclude={"id"})),
        )
        return ProductModel.model_validate(new_product, from_attributes=True)

    async def get_all_products(
        self,
        product_filter: ProductFilterInput,
    ) ->  list[ProductModel]:
        
        try:
            query = ProductCollection.create_filter_query(product_filter)
            products = await ProductCollection.find(query).to_list()
        
            return [ ProductModel.model_validate(t, from_attributes=True) for t in products ]
        except:
            raise EntityNotFoundError(status_code=404, message="There are no products")
    
    async def get_product_by_id(
        self,
        product_id: str,
    ) ->  ProductModel:
        
        try:
            product_id = convert_id(product_id)
            product = await ProductCollection.find_one(
                ProductCollection.id == product_id,
            )
            
            return ProductModel.model_validate(product, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Product not found")
    
    async def update_product(
        self,
        product: ProductModel,
    ) ->  ProductModel:
        
        try:
            
            to_update: dict = product.model_dump_to_update(exclude_unset=True)
                
            await ProductCollection.find(
                ProductCollection.id == product.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_product_by_id(product.id)
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="Product not found")
    
    async def delete_all_products(
        self,
    ) -> bool:
        
        try:
            delete_products = await ProductCollection.delete_all()
            return bool(delete_products.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="There are no products")
    
    async def delete_product(
        self,
        product_id: str,
    ) -> bool:
        
        try:
            product_id = convert_id(product_id)
            delete_product = await ProductCollection.find(
                ProductCollection.id == product_id,
            ).delete()                       
            return bool(delete_product.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Product not found")