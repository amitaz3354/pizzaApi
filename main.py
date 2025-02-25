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

# Update an existing pizza order (Bug: Doesn't actually update anything)
@app.put("/orders/{order_id}", response_model=dict)
async def update_order(order_id: str, updated_order: UpdatePizzaOrder):    
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")

    # BUG: Processing the update request, but doing nothing
    print(f"Update received for {order_id}, but nothing is actually updated.")
    
    return {"orderId": order_id}

# Delete a pizza order (Bug: No order_id in request but still deletes an order)
@app.delete("/orders", response_model=dict)
async def delete_order():
    if not orders:
        raise HTTPException(status_code=404, detail="No orders to delete")
    
    # BUG: Deleting a random order instead of receiving an ID
    order_id, _ = orders.popitem()
    print(f"Deleted order: {order_id}")
    
    return {"message": "Order deleted successfully"}
    
# Retrieve an existing pizza order
@app.get("/orders/{order_id}", response_model=PizzaOrder)
async def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return orders[order_id]
