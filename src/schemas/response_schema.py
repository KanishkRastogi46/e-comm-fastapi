from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union


class CreateProductsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: Union[str, int] = Field(..., description="ID of the created product")
    
    
class CreateOrdersResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: Union[str, int] = Field(..., description="ID of the created order")


class PageInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    next: Optional[int] = Field(None, description="Next offset value")
    limit: int = Field(..., description="Current limit value")
    previous: Optional[int] = Field(None, description="Previous offset value")


class ProductItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: Union[str, int] = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    total_quantity: int = Field(..., description="Total quantity available across all sizes")


class ListProductsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    data: List[ProductItem] = Field(..., description="List of products")
    page: PageInfo = Field(..., description="Pagination information")


class ProductDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: Union[str, int] = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")


class OrderItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    productDeails: ProductDetails = Field(..., description="Product details")
    quantity: int = Field(..., description="Quantity of the product")


class OrderData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: Union[str, int] = Field(..., description="Order ID")
    items: List[OrderItem] = Field(..., description="List of order items")
    totalPrice: float = Field(..., description="Total price of the order")


class ListOrdersResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    data: List[OrderData] = Field(..., description="List of orders")
    page: PageInfo = Field(..., description="Pagination information")