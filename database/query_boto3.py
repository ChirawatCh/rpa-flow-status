import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1', endpoint_url="http://dynamodb-local:8000")

# Reference to your DynamoDB table
table_name = 'RPAFlowStatus'

# Get a reference to the table
table = dynamodb.Table(table_name)

# Calculate the Unix timestamp for the date 30 days ago
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

# Extract and print the items
for item in sorted_items:
    print(item)
