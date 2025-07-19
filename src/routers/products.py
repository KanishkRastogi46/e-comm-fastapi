from fastapi import APIRouter, status, HTTPException, Query
from loguru import logger
from dotenv import load_dotenv
import os
from src.models.products import Products
from src.schemas.requests_schema import CreateProductsRequest, RequestQueryParams

load_dotenv()

router = APIRouter(
    prefix=f"/{os.environ.get("API_PREFIX")}/products",
    tags=["products"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: CreateProductsRequest):
    """
    Create a new product.
    """
    try:
        if not product.name or not product.price or not product.sizes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product data")
        
        is_product_exists = Products.objects(name=product.name.lower()).first()
        if is_product_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this name already exists")
        
        new_product = Products(name=product.name, price=product.price, sizes=product.sizes)
        new_product.save()
        logger.info(f"Product created successfully: {new_product.id}")
        return {"id": str(new_product.id)}
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create product")
    
    
@router.get("/", status_code=status.HTTP_200_OK)
async def list_products(queryParams: RequestQueryParams = Query()):
    """
    List products with optional filtering by name and size.
    """
    try:
        name = queryParams.name
        size = queryParams.size
        limit = queryParams.limit if queryParams.limit else 10
        offset = queryParams.offset if queryParams.offset else 0

        # Start with all products
        query = Products.objects.all()
        
        # Apply name filter if provided (with regex support for partial matching)
        if name:
            query = query.filter(name__icontains=name.lower())
        
        # Apply size filter if provided
        if size:
            query = query.filter(sizes__in=[size])
        
        # Get total count before pagination
        total_count = query.count()
        
        # Apply pagination
        paginated_query = query.skip(offset).limit(limit)
        
        # Execute query and build response
        products = paginated_query
        data = []
        
        for product in products:
            data.append({
                "id": str(product.id),
                "name": product.name,
                "price": product.price
            })
        
        # Calculate pagination info
        next_offset = offset + limit if (offset + limit) < total_count else None
        previous_offset = offset - limit if offset > 0 else None
        
        logger.info(f"Listed {len(data)} products with filters: name={name}, size={size}")
        
        return {
            "data": data,
            "page": {
                "next": next_offset,
                "limit": limit,
                "previous": previous_offset
            }
        }
        
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list products")
    