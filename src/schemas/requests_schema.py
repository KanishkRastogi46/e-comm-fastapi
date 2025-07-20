from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any, Union


class ProductsRequestQueryParams(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: Optional[str] = Field(default=None, description="Name of the product")
    size: Optional[Union[str, int]] = Field(default=None, description="Size of the product")
    limit: Optional[int] = Field(default=10, description="Number of items to return per page")
    offset: Optional[int] = Field(default=0, description="Number of items to skip for pagination")

class ProductSizes(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    size: Union[str, int] = Field(..., description="Size of the product")
    quantity: int = Field(..., description="Quantity of the product")


class CreateProductsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: str = Field(..., description="Name of the product")
    price: float = Field(..., description="Price of the product")
    sizes: List[ProductSizes] = Field(..., description="List of sizes and their quantities")
    
    
class OrdersRequestQueryParams(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    limit: Optional[int] = Field(default=10, description="Number of items to return per page")
    offset: Optional[int] = Field(default=0, description="Number of items to skip for pagination")
    
   
class OrderItems(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    productId: Union[str, int] = Field(..., description="ID of the product")
    quantity: int = Field(..., description="Quantity of the product")
    
class CreateOrdersRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    userId: Union[int, str] = Field(..., description="ID of the user placing the order")
    items: List[OrderItems] = Field(..., description="List of items in the order with product IDs and quantities")
    