from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
import boto3
import config
from typing import List
from boto3.dynamodb.conditions import Key, Attr

app = FastAPI()

api_keys = [config.api_key] 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1', endpoint_url="http://dynamodb-local:8000")
table = dynamodb.Table('RPAFlowStatus')

class FlowStatusCreate(BaseModel):
    name: str = Field(example="flow_name", description="Name of the flow")
    status: str = Field("IN_PROGRESS", example="IN_PROGRESS", description="Status of the flow")

class FlowStatus(BaseModel):
    name: str
    status: str
    createdAt: int  # Change data type to int for Unix timestamps
    updatedAt: int  # Change data type to int for Unix timestamps
    
class FlowStatusUpdate(BaseModel):
    name: str = "flow_name"
    status: str = "COMPLETED"

# Create a new flow status
@app.post("/flows/", response_model=FlowStatus, dependencies=[Depends(api_key_auth)])
def create_flow(flow: FlowStatusCreate):
    current_time_unix = int(datetime.utcnow().timestamp())  # Convert to Unix timestamp (seconds)
    item = {
        "name": flow.name,
        "status": flow.status,
        "createdAt": current_time_unix,
        "updatedAt": current_time_unix
    }
    table.put_item(Item=item)  # Store the item in DynamoDB
    return FlowStatus(**item)

@app.get("/flows/recent", dependencies=[Depends(api_key_auth)])
async def get_recent_updates():
    # Calculate the Unix timestamp for the date 365 days ago
    days_ago_unix = int((datetime.utcnow() - timedelta(days=365)).timestamp())
    # Use the scan operation to retrieve items based on a filter condition
    response = table.scan(
        IndexName='UpdatedAtIndex',  # Specify the GSI name for the query
        FilterExpression=Attr('updatedAt').gte(days_ago_unix),  # Query for items with 'updatedAt' greater than 0
        Limit=100 # Limit the result to the top 100 items
    )
    # Extract the items into a list
    items = response['Items']
    # Sort the items by updatedAt timestamp descending
    sorted_items = sorted(items, key=lambda x: x['updatedAt'], reverse=True)
    # Return the first 10 items after sorting, which represent the most recent updates.
    return sorted_items[:15]

@app.put("/flows", response_model=FlowStatus, dependencies=[Depends(api_key_auth)]) 
def update_flow(flow: FlowStatusUpdate):
    name = flow.name
    try:
        response = table.get_item(Key={'name': name})
        item = response['Item']
    except: 
        raise HTTPException(404, f"Flow {name} not found")  
    item['status'] = flow.status
    item['updatedAt'] = int(datetime.utcnow().timestamp()) # Convert to Unix timestamp (seconds)
    table.put_item(Item=item)
    return FlowStatus(**item)

@app.delete("/flows/{name}", dependencies=[Depends(api_key_auth)])
def delete_flow(name: str):
    try:
        response = table.get_item(Key={'name': name})
        item = response['Item']
    except:
        raise HTTPException(404, f"Flow {name} not found")
    
    table.delete_item(Key={'name': name})
    return {"message": f"Flow {name} deleted successfully"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    custom_response = {"error_code": exc.status_code, "error_message": exc.detail}
    return JSONResponse(content=custom_response, status_code=exc.status_code)