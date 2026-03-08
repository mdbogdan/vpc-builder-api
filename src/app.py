import json
import os
import boto3
from datetime import datetime

ec2 = boto3.client('ec2')
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name) if table_name else None

def create_vpc_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        vpc_cidr = body.get('vpc_cidr', '10.0.0.0/16')
        subnet_cidrs = body.get('subnet_cidrs', ['10.0.1.0/24', '10.0.2.0/24'])

        vpc_response = ec2.create_vpc(CidrBlock=vpc_cidr)
        vpc_id = vpc_response['Vpc']['VpcId']
        
        ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'ApiCreatedVpc'}])

        created_subnets = []
        for cidr in subnet_cidrs:
            subnet_response = ec2.create_subnet(VpcId=vpc_id, CidrBlock=cidr)
            subnet_id = subnet_response['Subnet']['SubnetId']
            created_subnets.append({
                'subnet_id': subnet_id,
                'cidr_block': cidr
            })

        record = {
            'vpc_id': vpc_id,
            'vpc_cidr': vpc_cidr,
            'subnets': created_subnets,
            'created_at': datetime.utcnow().isoformat(),
            'created_by': event.get('requestContext', {}).get('authorizer', {}).get('claims', {}).get('email', 'unknown')
        }
        table.put_item(Item=record)

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'VPC created successfully', 'data': record})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_vpc_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps({'vpcs': items})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
