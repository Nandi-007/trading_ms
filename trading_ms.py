import asyncio
import random
from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from starlette.websockets import WebSocketDisconnect

from models import OrderInput

app = FastAPI()

orders = []
active_connections: List[WebSocket] = []


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_messages = []
    for error in exc.errors():
        error_messages.append(
            {
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"]
            }
        )
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid input"}
    )


@app.get("/orders")
async def get_orders():
    return orders


@app.post("/orders", status_code=201)
async def place_order(order: OrderInput):
    await asyncio.sleep(random.uniform(0.1, 1))
    status = "pending"
    order_id = str(len(orders) + 1)
    updated_order = OrderInput(id=order_id, stoks=order.stoks, quantity=order.quantity, status=status)
    orders.append(updated_order)

    # Notify all subscribed clients about the order execution
    for connection in active_connections:
        await connection.send_json(updated_order.dict())

    return JSONResponse(
        content=updated_order.dict(),
        status_code=201
    )


@app.get("/orders/{order_id}", status_code=200)
async def get_order(order_id: str):
    for order in orders:
        if order.id == order_id:
            return order
    return JSONResponse(
        content={"description": f"Order with id {order_id} not found"},
        status_code=404)


@app.delete("/orders/{order_id}", status_code=204)
async def cancel_order(order_id: str):
    status = "canceled"
    for order in orders:
        if order.id == order_id:
            order.status = status
            return Response(status_code=204)
    return JSONResponse(
        content={"description": f"Order with id {order_id} not found"},
        status_code=404)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    #active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")

            await asyncio.sleep(random.uniform(0.1, 100))

            for order in orders:
                if order.status == "pending":
                    order.status = "executed"

            # Notify all subscribed clients about the order execution
            for connection in active_connections:
                await connection.send_json({"message": "Order executed"})
    except WebSocketDisconnect as e:
        # active_connections.remove(websocket)
        print(f"WebSocket disconnected with status code: {e.code}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
