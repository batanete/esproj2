import boto3
from boto3.dynamodb.conditions import Key, Attr
import decimal

REGION='us-west-2'


def get_keys():
    global keys
    with open('keys','r') as f:
        lines=f.readlines()
        keys=[]
        keys.append(lines[0].replace('\n',''))
        keys.append(lines[1].replace('\n',''))


def init():
    # Get the service resource.
    global table
    get_keys()
    dynamodb = boto3.resource('dynamodb',REGION,aws_access_key_id=keys[0], aws_secret_access_key=keys[1])
    table = dynamodb.Table('users')

#returns user with the given username
def get_user(username):
    response=table.query(
        KeyConditionExpression=Key('name').eq(username)
    )
    items = response['Items']

    if len(items)==0:
        return None
    else:
        return items[0]

#set money to given amount
def update_money(name,final_amount):
    response=table.update_item(
        Key={
            'name':name
        },
        UpdateExpression="set money = :m",
        ExpressionAttributeValues={
            ':m': decimal.Decimal(final_amount)
        },
        ReturnValues="UPDATED_NEW"
    )

    print('resp:',response)


#init()
