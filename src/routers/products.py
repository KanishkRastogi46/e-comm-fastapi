from fastapi import APIRouter, status, HTTPException, Query
from loguru import logger
from dotenv import load_dotenv
from src.models.products import Products
from src.schemas.requests_schema import CreateProductsRequest, ProductsRequestQueryParams, ProductSizes
from src.schemas.response_schema import ListProductsResponse, CreateProductsResponse

load_dotenv()

router = APIRouter(
    prefix='/products',
    tags=["products"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateProductsResponse)
async def create_product(product: CreateProductsRequest):
    """
    Create a new product.
    """
    try:
        if not product.name or not product.price or not product.sizes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product data")
        
        # Validate sizes data
        try:
            from src.models.products import Sizes, SizesEnum
            validated_sizes = []
            total_quantity = 0
            
            for size_data in product.sizes:
                # Validate size enum
                size_enum = SizesEnum(str(size_data.size).lower())
                quantity = int(size_data.quantity)
                
                if quantity < 0:
                    raise ValueError("Quantity must be non-negative")
                
                validated_sizes.append(Sizes(size=size_enum, quantity=quantity))
                total_quantity += quantity
        except (ValueError, AttributeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid sizes data: {str(e)}"
            )
        
        # Check for existing product (case-insensitive)
        is_product_exists = Products.objects(name__iexact=product.name).first()
        if is_product_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this name already exists")
        
        new_product = Products(name=product.name, price=product.price, sizes=validated_sizes, total_quantity=total_quantity)
        new_product.save()
        logger.info(f"Product created successfully: {new_product.id}")
        return {"id": str(new_product.id)}
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create product")
    
    
@router.get("/", status_code=status.HTTP_200_OK, response_model=ListProductsResponse)
async def list_products(queryParams: ProductsRequestQueryParams = Query()):
    """
    List products with optional filtering by name and size.
    """
    try:
        name = queryParams.name
        size = queryParams.size
        limit = queryParams.limit
        offset = queryParams.offset

        # Start with all products
        query = Products.objects.all()
        
        # Apply name filter if provided (case-insensitive partial matching)
        if name:
            query = query.filter(name__icontains=name)
        
        # Apply size filter if provided
        if size:
            # Validate size enum value
            try:
                from src.models.products import SizesEnum
                size_enum = SizesEnum(str(size).lower())
                # Filter products that have the specified size in their sizes list
                query = query.filter(__raw__={"sizes": {"$elemMatch": {"size": size_enum.value}}})
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"Invalid size value. Must be one of: {[s.value for s in SizesEnum]}"
                )
        
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
    