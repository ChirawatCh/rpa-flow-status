# Flow Management API

This is a simple API for managing "flows" stored in DynamoDB, built with FastAPI.

## Endpoints

### Create Flow

- Endpoint: POST /flows/
- Request body:

```json
{
  "name": "flow_name", 
  "status": "IN_PROGRESS" 
}
```

- Response body:

```json 
{
  "name": "flow_name",
  "status": "IN_PROGRESS",
  "createdAt": 1674320164,
  "updatedAt": 1674320164  
}
```

Creates a new flow item in DynamoDB.

### Get Recent Flow Updates

- Endpoint: GET /flows/recent

- Response body: 

```json
[
  {
    "name": "flow1",
    "status": "COMPLETED", 
    "createdAt": 1673897221,
    "updatedAt": 1674320164
  },
  {
    "name": "flow2",
    "status": "IN_PROGRESS",
    "createdAt": 1673897021, 
    "updatedAt": 1674310164
  }
]
```

Gets up to 100 recently updated flows from the past year, sorted by updatedAt timestamp.

### Update Flow

- Endpoint: PUT /flows
- Request body:

```json
{
  "name": "flow1",
  "status": "COMPLETED"  
}
```

- Response body:

```json
{
  "name": "flow1",
  "status": "COMPLETED",
  "createdAt": 1673897221,
  "updatedAt": 1674320164  
}
```

Updates the status of an existing flow.

### Delete Flow

- Endpoint: DELETE /flows/{name}

Deletes a flow by name.

## Error Handling

Errors return JSON response with `error_code` and `error_message`:

```json
{
  "error_code": 404,
  "error_message": "Flow flow1 not found"
}
```
