import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

keys=[
    "AKIAJMMEIX7PDFFUDFQQ",
    "Gw6LsMMTdsJbSdvEUtLqbZsG2U7+vOl3EZaPACe6"
]

def init():
    # Get the service resource.
    global table
    dynamodb = boto3.resource('dynamodb','us-west-2',aws_access_key_id=keys[0], aws_secret_access_key=keys[1])
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
    print(name)
    
    
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

def payment(event,context):
    name=event['username']
    amount=event['amount']

    init()

    user=get_user(name)
    
    money=user['money']
    user=user['name']

    if money<amount:
        return {"auth":0,"payment_type":"manual"}
    else:
        update_money(user,money-amount)
        return {"auth":1,"payment_type":"automatic"}
