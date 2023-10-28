import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1', endpoint_url="http://dynamodb-local:8000")

# Name of the table you want to delete
table_name = 'RPAFlowStatus'

# Reference to the table
table = dynamodb.Table(table_name)

# Delete the table
table.delete()

print(f"Table '{table_name}' is being deleted.")
