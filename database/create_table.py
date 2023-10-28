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
                'AttributeType': 'S'
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
    table = dynamodb.Table(table_name)
    print("Table status:", table.table_status)
    print("Key Schema:", table.key_schema)  # Fixed this line

else:
    print("Table already exists.")
