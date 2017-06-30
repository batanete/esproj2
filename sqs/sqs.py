import boto3


inputqueue=None
outputqueue=None
sqs=None


REGION='us-west-2'

def get_keys():
    global keys
    with open('keys','r') as f:
        lines=f.readlines()
        keys=[]
        keys.append(lines[0].replace('\n',''))
        keys.append(lines[1].replace('\n',''))


#send response to user via output queue
def post_response(resp):
    outputqueue.send_message(MessageBody=resp, MessageAttributes={})


#creates input and output queues if they are not created and initializes them.
def init():
    global inputqueue,outputqueue,sqs
    get_keys()

    sqs = boto3.resource('sqs',REGION, aws_access_key_id=keys[0], aws_secret_access_key=keys[1])

    # Create the queue. This returns an SQS.Queue instance
    try:
        sqs.create_queue(QueueName='inputqueue', Attributes={'DelaySeconds': '1'})
    except Exception as e:
        print(e)
        pass

    try:
        sqs.create_queue(QueueName='outputqueue', Attributes={'DelaySeconds': '1'})

    except Exception as e:
        print(e)
        pass


    # Get the queue. This returns an SQS.Queue instance
    inputqueue=sqs.get_queue_by_name(QueueName='inputqueue')
    outputqueue=sqs.get_queue_by_name(QueueName='outputqueue')


def deleteAllMessages():
    outputqueue.purge()
    inputqueue.purge()

#executed when app closes. deletes all queues.
def exit():
    inputqueue.delete()
    outputqueue.delete()



#init()

#print(outputqueue.receive_messages(MaxNumberOfMessages=10))

#exit()
