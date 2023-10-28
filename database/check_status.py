import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1', endpoint_url="http://dynamodb-local:8000")
client = dynamodb.meta.client

table_name = 'RPAFlowStatus'

existing_tables = client.list_tables()['TableNames']
print(existing_tables)

# Check if table exists
if table_name in existing_tables:
    # print(table_name)

    table = dynamodb.Table(table_name)
    response = table.key_schema
    print(response)
    # Print table status
    print(f"Table {table_name} exists:", table.table_status)
    
    response = client.describe_table(TableName='RPAFlowStatus')
    # print(response['Table'])
    print(response['Table']['AttributeDefinitions'])
    # print(response['Table']['ProvisionedThroughput'])

else:
    print(f"Table {table_name} does not exist")