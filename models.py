from pydantic import BaseModel, Field
from typing import List, Optional

# Product Models
class Size(BaseModel):
    size: str
    quantity: int

class ProductIn(BaseModel):
    name: str
    price: float
    sizes: List[Size]

class ProductOut(BaseModel):
    id: str

class ProductList(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    price: float

# Order Models
class OrderItemIn(BaseModel):
    productId: str
    qty: int

class OrderIn(BaseModel):
    userId: str
    items: List[OrderItemIn]

class OrderOut(BaseModel):
    id: str

class ProductDetails(BaseModel):
    id: str = Field(..., alias="_id")
    name: str

class OrderItemList(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderList(BaseModel):
    id: str = Field(..., alias="_id")
    total: float
    items: List[OrderItemList]

# Pagination Models
class Pagination(BaseModel):
    next: Optional[str] = None
    limit: int
    previous: Optional[str] = None

class ProductPage(BaseModel):
    data: List[ProductList]
    page: Pagination

class OrderPage(BaseModel):
    data: List[OrderList]
    page: Pagination