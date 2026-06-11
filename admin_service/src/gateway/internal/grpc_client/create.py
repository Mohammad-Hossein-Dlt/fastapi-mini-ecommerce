from pathlib import Path
from sharedlib.proto_builder.utils import ProtoConfig, FieldConfig
from sharedlib.proto_builder.service_builder import ServiceBuilder

from src.gateway.internal.interface.Iauth_service import IAuthService
from src.gateway.internal.interface.Icategory_service import ICategoryService
from src.gateway.internal.interface.Iproduct_service import IProductService
from src.gateway.internal.interface.Iorder_service import IOrderService

path = Path(__file__).parent / "service"
path.mkdir(exist_ok=True)

config = ProtoConfig(
    remove=[
        FieldConfig(name="AuthCredentials", condition="scope", include_self=True),
        FieldConfig(name="access_token", condition="scope", include_self=True),
        FieldConfig(name="refresh_token", condition="scope", include_self=True),
    ],
)
service_builder = ServiceBuilder(config)

protobuf = service_builder.build(IAuthService)
with open(path / "auth_service.proto", "w") as f:
    f.write(protobuf)
    
protobuf = service_builder.build(ICategoryService)
with open(path / "category_service.proto", "w") as f:
    f.write(protobuf)    
    
protobuf = service_builder.build(IProductService)
with open(path / "product_service.proto", "w") as f:
    f.write(protobuf)    

protobuf = service_builder.build(IOrderService)
with open(path / "order_service.proto", "w") as f:
    f.write(protobuf)