from enum import Enum

class Environment(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"
    
class ServiceCommunication(str, Enum):
    BROKER = "broker"
    HTTP = "http"    

class DBStack(str, Enum):
    POSTGRESQL = "postgresql"
    MONGO_DB = "mongo_db"

class Status(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    