'''
CREATE PRODUCTS API:
ENDPOINT - /products
REQUEST BODY
{
    name: str,
    price: float,
    sizes: [
        {
            size: str,
            qty: int
        }
    ]
}
RESPONSE - {id: str | int}


LIST PRODUCTS API:
ENDPOINT - /products
QUERY PARAMETERS 
- name: str (can include regex for partial matching)
- size: str (optional, to filter by size)
- limit: int
- offset: int
RESPONSE 
{
    data: [
        {
            id: str | int,
            name: str,
            price: float,
        }
    ],
    page: {
        next: int,
        limit: int,
        previous: int,
    }
}


CREATE ORDERS API:
ENDPOINT - /orders
REQUEST BODY
{
    userId: str | int,
    items: [
        {
            productId: str | int,
            quantity: int
        }
    ]
}
RESPONSE - {id: str | int}


LIST ORDERS API:
ENDPOINT - /orders/{userId}
QUERY PARAMETERS
- limit: int
- offset: int
RESPONSE 
{
    data: [
        {
            id: str | int,
            items: [
                {
                    productDeails: {
                        id: str | int,
                        name: str,
                    },
                    quantity: int
                }
            ],
            totalPrice: float,
        }
    ],
    page: {
        next: int,
        limit: int,
        previous: int,
    }
}
'''
