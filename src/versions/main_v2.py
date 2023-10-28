from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import boto3

app = FastAPI()

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1', endpoint_url="http://dynamodb-local:8000")
table = dynamodb.Table('RPAFlowStatus')

class FlowStatusCreate(BaseModel):
    name: str = Field(example="flow_1", description="Name of the flow")
    status: str = Field("IN_PROGRESS", example="IN_PROGRESS", description="Status of the flow")

class FlowStatus(BaseModel):
    name: str
    status: str
    createdAt: str
    updatedAt: str
    
class FlowStatusUpdate(BaseModel):
    status: str = "COMPLEATED"

# Create a new flow status
@app.post("/flows/", response_model=FlowStatus)
def create_flow(flow: FlowStatusCreate):
    current_time = datetime.utcnow().isoformat()  # Store timestamps in UTC
    item = {
        "name": flow.name,
        "status": flow.status,
        "createdAt": current_time,
        "updatedAt": current_time
    }
    table.put_item(Item=item)  # Store the item in DynamoDB
    return FlowStatus(**item)

@app.get("/flows/recent")
async def get_recent_updates():

    # response = table.scan(Limit=20)
    response = table.scan()
    items = response['Items']

    # Sort items by updatedAt descending
    items.sort(key=lambda x: x['updatedAt'], reverse=True)

    # Return only the first 10
    return items[:10]

@app.put("/flows/{name}", response_model=FlowStatus)  
def update_flow(name: str, flow: FlowStatusUpdate):
    try:
        response = table.get_item(Key={'name': name})
        item = response['Item']
    except:
        raise HTTPException(status_code=404, detail=f"Flow {name} not found")

    item['status'] = flow.status
    item['updatedAt'] = datetime.utcnow().isoformat()

    table.put_item(Item=item)

    return FlowStatus(**item)
