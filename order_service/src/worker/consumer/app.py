from src.infra.broker_config.app import app
from src.worker.consumer.rabbitmq import client
from src.domain.schemas.order.order_model import OrderModel
from src.models.schemas.filter.order_filter_input import OrderFilterInput
import json
import time
from typing import Any

app.set_broker(client.broker)

@app.after_startup
async def startup():
    
    token = '''

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE1NDY2fQ.1KtJwinlRLNaTK4IN87mzf7C9LysOdVIpGV9XTAvwKk
    
'''
    
    token = token.strip()
    
    while True:
        response = await client.broker.request(
            
            # message=ModifyOrderInput(id="68f5f70ee8f872d17207e5c3", status=Status.delivered),
            message=OrderFilterInput(),
            
            # message={
            #     "order": PlaceOrderInput(product_id=2, quantity=120),
            # },
            
            # message="68f740120805e2b26e7692fc",
            
            # message={
            #     "order_id": "68f740120805e2b26e7692fc",
            # },
            
            # message=PlaceOrderInput(product_id=2, quantity=120),
                        
            headers={
                "token": token,
            },
            
            routing_key="order_service.user.get.all",
            exchange=client.exchange,
            timeout=10,
        )

        data: Any = json.loads(response.body.decode())
                     
        if isinstance(data, dict):             
            if data.get("status_code", None):
                output = data
            else:     
                output = OrderModel.model_validate(data).model_dump()
        elif isinstance(data, list):
            output = [ OrderModel.model_validate(order).model_dump() for order in data ]
        else:
            output = data
            
        print(output)
        print(type(output))
        
        time.sleep(2)
