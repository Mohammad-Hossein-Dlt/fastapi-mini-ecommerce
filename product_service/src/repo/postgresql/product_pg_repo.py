from sqlalchemy.orm import Session
from src.models.schemas.filter.products_filter_input import ProductFilterInput
from src.repo.interface.Iproduct_repo import IProductRepo
from src.domain.schemas.product.product_model import ProductModel
from src.infra.db.postgresql.models.product_db_model import ProductDBModel
from src.infra.exceptions.exceptions import EntityNotFoundError

class ProductPgRepo(IProductRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
        
    async def insert_product(
        self,
        product: ProductModel,
    ) -> ProductModel:
        
        try:
            new_product = ProductDBModel(**product.model_dump(exclude_none=True))
            self.db.add(new_product)
            self.db.commit()
            return ProductModel.model_validate(new_product, from_attributes=True)
        except:
            # self.db.rollback()
            raise

    async def get_all_products(
        self,
        product_filter: ProductFilterInput,
    ) ->  list[ProductModel]:
        
        try:
            query = ProductDBModel.create_filter_query(product_filter)
            products = self.db.execute(query).scalars().all()
        
            return [ ProductModel.model_validate(t, from_attributes=True) for t in products ]
        except:
            # self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="There are no products")
    
    async def get_product_by_id(
        self,
        product_id: int,
    ) ->  ProductModel:
        
        try:
            product = self.db.query(
                ProductDBModel   
            ).where(
                ProductDBModel.id == int(product_id),
            ).first()
            
            return ProductModel.model_validate(product, from_attributes=True)
        except:
            # self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="Product not found")
    
    async def update_product(
        self,
        product: ProductModel,
    ) ->  ProductModel:
        
        try:
            
            to_update: dict = product.custom_model_dump(
                exclude_unset=True,
                exclude={
                    "id",
                },
                db_stack="sql",
            )

            self.db.query(
                ProductDBModel   
            ).where(
                ProductDBModel.id == product.id
            ).update(
                to_update,
                synchronize_session='fetch',
            )
            
            self.db.commit()
            
            return await self.get_product_by_id(product.id)
        except EntityNotFoundError:
            raise
        except:
            # self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="Product not found")
    
    async def delete_all_products(
        self,
    ) -> bool:
        
        try:
            products = await self.get_all_products(
                ProductFilterInput(category_id=None),
            )
            if products:
                for product in products:
                    product = self.db.merge(ProductDBModel(**product.model_dump()))
                    if isinstance(product, ProductDBModel):
                        self.db.delete(product)
                
                self.db.commit()        
                return True 
            else:
                return False
        except EntityNotFoundError:
            raise
        except:
            # self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="There are no products")
    
    async def delete_product(
        self,
        product_id: int,
    ) -> bool:
        
        try:
            product = await self.get_product_by_id(product_id)
            if product:
                product = self.db.merge(ProductDBModel(**product.model_dump()))
                
            if isinstance(product, ProductDBModel):
                self.db.delete(product)
                self.db.commit()
                return True
            else:
                return False
        except EntityNotFoundError:
            raise
        except:
            # self.db.rollback()
            raise EntityNotFoundError(status_code=404, message="Product not found")