from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError

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
    name: str
    status: str
    updatedAt: str

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

# Get a list of the last updated items
@app.get("/flows/last-updated/", response_model=list[FlowStatus])
def get_last_updated_items():
    # Calculate a timestamp representing a time before the current time
    # (e.g., 24 hours ago)
    cutoff_time = (datetime.utcnow() - timedelta(hours=24)).isoformat()

    try:
        response = table.scan(
            FilterExpression='#updatedAt > :cutoff',
            ExpressionAttributeNames={'#updatedAt': 'updatedAt'},
            ExpressionAttributeValues={':cutoff': cutoff_time},
            Limit=10
        )

        # Return the items in descending order based on the updatedAt attribute
        items = sorted(response['Items'], key=lambda item: item['updatedAt'], reverse=True)
        return items
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB error: {e}")

# Update the status of a flow by name
@app.put("/flows/{flow_name}", response_model=FlowStatus)
def update_flow_status(flow_name: str, flow_update: FlowStatusUpdate):
    # Check if the flow with the given name exists
    # try:
    response = table.get_item(Key={"name": flow_name})
    item = response.get("Item")

    if item is None:
        raise HTTPException(status_code=404, detail="Flow not found")
    # except ClientError as e:
    #     raise HTTPException(status_code=500, detail=f"DynamoDB error: {e}")

    # Update the status and updatedAt attribute
    current_time = datetime.utcnow().isoformat()
    item["status"] = flow_update.status
    item["updatedAt"] = current_time

    # Save the updated item
    table.put_item(Item=item)

    return FlowStatus(**item)
