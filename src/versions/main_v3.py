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
    # Initialize the response with an initial scan of the DynamoDB table, limiting the result to 100 records.
    response = table.scan(Limit=100)

    # Extract the initial set of items from the response.
    items = response['Items']

    # Continue scanning the table in chunks of 100 records while there are more items to retrieve.
    while 'LastEvaluatedKey' in response:
        # Perform a scan with the ExclusiveStartKey to continue from where the previous scan left off.
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], Limit=100)
        
        # Extend the items list with the new batch of items obtained in the current scan.
        items.extend(response['Items'])

    # Sort the aggregated items by the 'updatedAt' field in descending order.
    items.sort(key=lambda x: x['updatedAt'], reverse=True)

    # Return the first 10 items after sorting, which represent the most recent updates.
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
