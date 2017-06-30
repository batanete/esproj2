import boto3
import json
import s3
from sys import argv,exit
from time import sleep

s3.get_keys()
keys=s3.keys
sfnarn="arn:aws:states:us-west-2:750984048303:stateMachine:main"

def send_auth(photopath,amount):
    global exearn,sfn
    filename=photopath.split('/')[-1]

    #post photo on s3 bucket
    s3.init()
    f=open(photopath,'rb')
    filebytes=f.read()

    s3.post_photo(filebytes,filename)

    #initiate state machine execution
    sfn=boto3.client('stepfunctions','us-west-2',aws_access_key_id = keys[0], aws_secret_access_key = keys[1])

    response = sfn.start_execution(
        stateMachineArn=sfnarn,
        input=json.dumps({
            "filename":filename,
            "amount":amount
        })
    )

    #get execution arn
    exearn=response['executionArn']



def wait_for_aswer():
    while True:
        response = sfn.describe_execution(
            executionArn=exearn
        )
        #still running, check again later
        if response['status']=='RUNNING':
            sleep(1)
            continue
        #finished successfully, handle response
        elif response['status']=='SUCCEEDED':
            output=eval(response['output'])
            print(output['payment_type'])
        #error ocorred
        else:
            print('sfn returned error')

        return




if __name__=='__main__':
    if len(argv)<3:
        print('usage:python3 userapp.py <photo\'s path> <amount to pay>')
    else:
        path=argv[1]
        amount=int(argv[2])

        send_auth(path,amount)
        wait_for_aswer()

        #TODO: wait for answer(auth failed, manual payment or auto payment)
