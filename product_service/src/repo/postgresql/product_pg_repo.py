from sqlalchemy.orm import Session
from src.models.schemas.filter.product_filter_input import ProductFilterInput
from src.repo.interface.Iproduct_repo import IProductRepo
from src.domain.schemas.product.product_model import ProductModel
from src.infra.database.postgresql.models.product_db_model import ProductDBModel
from src.infra.utils.convert_id import convert_database_id
from src.infra.exceptions.exceptions import EntityNotFoundError

class ProductPgRepo(IProductRepo):
    
    def __init__(
        self,
        db: Session,
    ):
        
        self.db = db
        
    async def create(
        self,
        product: ProductModel,
    ) -> ProductModel:
        
        try:
            new_product = ProductDBModel(**product.model_dump_for_db())
            self.db.add(new_product)
            self.db.commit()
            return ProductModel.model_validate(new_product, from_attributes=True)
        except:
            raise
    
    async def get_by_id(
        self,
        product_id: str,
    ) -> ProductModel:
        
        try:
            product_id = convert_database_id(product_id)
            product = self.db.query(
                ProductDBModel   
            ).where(
                ProductDBModel.id == product_id,
            ).first()
            
            return ProductModel.model_validate(product, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Product not found")
    
    async def update(
        self,
        product: ProductModel,
    ) -> ProductModel:
        
        try:
            
            to_update: dict = product.model_dump_for_db(
                exclude_none=True,
                exclude_unset=True,
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
            
            return await self.get_by_id(product.id)
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="Product not found")
    
    async def delete_by_id(
        self,
        product_id: str,
    ) -> bool:
        
        try:
            product_id = convert_database_id(product_id)
            try:
                product = await self.get_by_id(product_id)
            except:
                return False
            
            if not product:
                return False
            
            to_delete = self.db.merge(ProductDBModel(**product.model_dump()))
                
            if isinstance(to_delete, ProductDBModel):
                self.db.delete(to_delete)
                self.db.commit()
                return True

            return False
                        
        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="Product not found")
        
    async def get_by_criteria(
        self,
        criteria: ProductFilterInput,
    ) -> list[ProductModel]:
        
        try:
            query = ProductDBModel.create_filter_query(criteria)
            products = self.db.execute(query).scalars().all()
        
            return [ ProductModel.model_validate(t, from_attributes=True) for t in products ]
        except:
            raise EntityNotFoundError(status_code=404, message="There are no products")
        
    async def delete_all(
        self,
    ) -> bool:
        try:
            
            try:
                products: list[ProductModel] = await self.get_by_criteria(
                    ProductFilterInput(category_id=None),
                )
            except:
                return False
            
            if products:
                for product in products:
                    product = self.db.merge(ProductDBModel(**product.model_dump()))
                    if isinstance(product, ProductDBModel):
                        self.db.delete(product)
                
                self.db.commit()        
                return True 

            return False

        except EntityNotFoundError:
            raise
        except:
            raise EntityNotFoundError(status_code=404, message="There are no products")