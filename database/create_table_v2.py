import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1', endpoint_url="http://dynamodb-local:8000")
client = dynamodb.meta.client

# Reference to your DynamoDB table
table_name = 'RPAFlowStatus'

existing_tables = client.list_tables()['TableNames']

if table_name not in existing_tables:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'name',  # Use 'name' as the primary key (hash key)
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'updatedAt',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'UpdatedAtIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'updatedAt',
                        'KeyType': 'HASH'  # HASH key (not RANGE key)
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'  # You can choose a different projection type if needed
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ]
    )

    table.wait_until_exists()
    # Initialize the DynamoDB client and specify your region and table name
    dynamodb = boto3.client('dynamodb', region_name='ap-southeast-1', endpoint_url="http://dynamodb-local:8000")
    
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

else:
    print("Table already exists.")
