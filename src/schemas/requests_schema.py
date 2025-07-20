from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any


class RequestQueryParams(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: Optional[str] = Field(default=None, description="Name of the product")
    size: Optional[str | int] = Field(default=None, description="Size of the product")
    limit: Optional[int] = Field(default=10, description="Number of items to return per page")
    offset: Optional[int] = Field(default=0, description="Number of items to skip for pagination")


class CreateProductsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: str = Field(..., description="Name of the product")
    price: float = Field(..., description="Price of the product")
    sizes: List[Dict[str, Any]] = Field(..., description="List of sizes and their quantities")
    
    
class CreateOrdersRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    userId: int | str = Field(..., description="ID of the user placing the order")
    items: List[Dict[str, Any]] = Field(..., description="List of items in the order with product IDs and quantities")
    