import csv
import boto3
import time
from datetime import datetime

# Path to your CSV file
csv_file = 'database/data-mock.csv'

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1', endpoint_url="http://dynamodb-local:8000")

# Reference to your DynamoDB table
table_name = 'RPAFlowStatus'
table = dynamodb.Table(table_name)

with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        time.sleep(1) # Sleep for 3 seconds
        item = {
            'name': row['name'],  # Use 'name' as the primary key
            'status': row['status'],
            'createdAt': datetime.utcnow().isoformat(),
            'updatedAt': datetime.utcnow().isoformat()
        }
        print(type(item["name"]), type(item["status"]), type(item["createdAt"]), type(item["updatedAt"]))
        table.put_item(Item=item)
