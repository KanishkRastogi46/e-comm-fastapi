from fastapi import APIRouter, HTTPException, Query, status
from loguru import logger
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime
from src.models.orders import Orders, OrderItems
from src.models.products import Products
from src.schemas.requests_schema import CreateOrdersRequest, OrdersRequestQueryParams
from src.schemas.response_schema import ListOrdersResponse, CreateOrdersResponse

load_dotenv()

router = APIRouter(
    prefix='/orders',
    tags=["orders"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: CreateOrdersRequest):
    """
    Create a new order.
    """
    try:
        if not order.userId or not order.items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order data")
        
        # Validate and convert userId to int if needed
        try:
            user_id = int(order.userId)
        except (ValueError, TypeError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="userId must be a valid integer")
        
        items = []
        processed_products = set()  # Track processed products to avoid duplicates
        
        for item in order.items:
            if not item.productId or not item.quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item data")
            
            # Check for duplicate products in the same order
            if item.productId in processed_products:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Duplicate product {item.productId} in order")
            
            product = Products.objects(id=ObjectId(item.productId)).first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {item.productId} not found")
            if item.quantity < 1:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be at least 1")
            # Check if product has sufficient stock using total_quantity
            if item.quantity > product.total_quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock for the product")
            
            # Create OrderItems with the product reference (not ObjectId)
            order_item = OrderItems(productId=product, quantity=item.quantity)
            items.append(order_item)
            processed_products.add(item.productId)
            
            # Update product quantities (reduce stock)
            product.total_quantity -= item.quantity
            product.updated_at = datetime.now()
            product.save()
            
        # Generate a default order name
        order_name = f"Order-{user_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        new_order = Orders(name=order_name, userId=user_id, items=items)
        new_order.save()
        logger.info(f"Order created successfully: {new_order.id}")
        return {"id": str(new_order.id)}
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail="Failed to create order")
    

@router.get("/{userId}", status_code=status.HTTP_200_OK, response_model=ListOrdersResponse)
async def list_orders_by_userId(userId: str, queryParams: OrdersRequestQueryParams = Query()):
    """
    List orders for a specific user with optional pagination.
    """
    try:
        limit = queryParams.limit
        offset = queryParams.offset
        
        # Validate userId
        if not userId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID is required")
        
        # Start with orders for the specific user
        query = Orders.objects(userId=userId)
        
        # Get total count before pagination
        total_count = query.count()
        
        # Apply pagination
        paginated_query = query.skip(offset).limit(limit)
        
        # Execute query and build response
        orders = paginated_query
        data = []
        
        for order in orders:
            items = []
            total_price = 0.0
            
            for item in order.items:
                # Get product details - item.productId is already a reference
                product = item.productId
                if product:
                    product_details = {
                        "id": str(product.id),
                        "name": product.name
                    }
                    items.append({
                        "productDeails": product_details,
                        "quantity": item.quantity
                    })
                    # Calculate total price
                    total_price += product.price * item.quantity
            
            data.append({
                "id": str(order.id),
                "items": items,
                "totalPrice": total_price
            })
        
        # Calculate pagination info
        next_offset = offset + limit if (offset + limit) < total_count else None
        previous_offset = offset - limit if offset > 0 else None
        
        logger.info(f"Listed {len(data)} orders for user {userId}")
        
        return {
            "data": data,
            "page": {
                "next": next_offset,
                "limit": limit,
                "previous": previous_offset
            }
        }
        
    except Exception as e:
        logger.error(f"Error listing orders for user {userId}: {e}")
        raise HTTPException(status_code=500, detail="Failed to list orders")
