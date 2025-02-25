from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional

app = FastAPI()

# In-memory storage for orders
orders = {}

# Pydantic model to represent the pizza order
class PizzaOrder(BaseModel):
    customerName: str
    pizzaType: str
    toppingOnFirstHalf: str
    toppingOnSecondHalf: str

class UpdatePizzaOrder(BaseModel):
    customerName: Optional[str] = None
    pizzaType: Optional[str] = None
    toppingOnFirstHalf: Optional[str] = None
    toppingOnSecondHalf: Optional[str] = None

# Create a new pizza order
@app.post("/orders", response_model=dict)
async def create_order(order: PizzaOrder):
    order_id = str(uuid4())
    orders[order_id] = order
    print(f"Order created: {order_id}")
    return {"orderId": order_id}

# Update an existing pizza order (no pizza id provided in the request as per the bug)
@app.put("/orders/", response_model=dict)
async def update_order(updated_order: UpdatePizzaOrder):
    bug_result = orders[0] if orders else "12345678"

    return {"orderId": bug_result}
    

    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update the order with the provided fields
    existing_order = orders[order_id]
    updated_data = updated_order.dict(exclude_unset=True)
    
    for field, value in updated_data.items():
        setattr(existing_order, field, value)
    
    orders[order_id] = existing_order
    return {"orderId": order_id}

# Delete a pizza order
@app.delete("/orders/{order_id}", response_model=dict)
async def delete_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    
    del orders[order_id]
    return {"message": "Order deleted successfully"}

# Retrieve an existing pizza order (GET /orders/{order_id})
@app.get("/orders/{order_id}", response_model=PizzaOrder)
async def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return orders[order_id]
