import boto3

# Initialize the DynamoDB client and specify your region and table name
dynamodb = boto3.client('dynamodb', region_name='ap-southeast-1', endpoint_url="http://dynamodb-local:8000")
table_name = 'RPAFlowStatus' # Replace with your actual table name

try:
    # Use the describe_table method to retrieve information about your table
    response = dynamodb.describe_table(TableName=table_name)

    # Check if the response contains the TableDescription and the attribute KeySchema
    if 'Table' in response and 'KeySchema' in response['Table']:
        key_schema = response['Table']['KeySchema']

        # Iterate through the KeySchema to find secondary indexes
        secondary_indexes = [index['IndexName'] for index in response['Table'].get('GlobalSecondaryIndexes', [])]

        print(f"Primary Key Schema: {key_schema}")
        print(f"Secondary Indexes: {secondary_indexes}")
    else:
        print(f"Table {table_name} doesn't exist or doesn't have KeySchema defined.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
