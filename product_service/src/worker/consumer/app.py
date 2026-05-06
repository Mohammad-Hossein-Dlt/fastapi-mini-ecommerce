from src.infra.broker_config.app import app
from src.worker.consumer.rabbitmq import client
from src.domain.schemas.category.category_model import CategoryModel
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
import json
import time
from typing import Any

app.set_broker(client.broker)

@app.after_startup
async def startup():
    
    token = '''

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxODgxNDgwOTM2fQ.9BXrX-ljcIenRL2NI_s2GPgKhe7JH4fHSMLhUZKriXA
    
'''

    refresh_token = '''

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MjAwMTQ4MDkzNn0.c9u87eBrW3TSlt1_0eyvx1gAFlIKi16Y-kN27HsZr5U
    
'''
    
    token = token.strip()
    refresh_token = refresh_token.strip()
    
    while True:
        response = await client.broker.request(
            
            message=CategoryFilterInput(id=2, based_on="child-to-parent"),
                        
            headers={
                "token": token,
            },
            
            routing_key="product_service.category.get.all",
            exchange=client.exchange,
            timeout=10,
        )

        data: Any = json.loads(response.body.decode())
                     
        if isinstance(data, dict):             
            if data.get("status_code", None):
                output = data
            else:     
                output = CategoryModel.model_validate(data).model_dump()
        elif isinstance(data, list):
            output = [ CategoryModel.model_validate(order).model_dump() for order in data ]
        else:
            output = data
            
        print(output)
        print(type(output))
        
        time.sleep(2)
