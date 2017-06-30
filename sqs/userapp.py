import sqs
import boto3
import s3
from sys import argv,exit
from time import sleep


keys=None


def send_auth(photopath,amount):

    #add request to sqs queue
    sqs.init()
    inputqueue=sqs.inputqueue
    # TODO Validation of the PATH
    filename=photopath.split('/')[-1]

    #post photo on s3 bucket
    s3.init()
    f=open(photopath,'rb')
    filebytes=f.read()

    s3.post_photo(filebytes,filename)

    message=filename+':'+str(amount)
    inputqueue.send_message(MessageBody=message, MessageAttributes={})



def wait_for_aswer():
    while True:
        messages=sqs.outputqueue.receive_messages()

        if len(messages)<1:
            sleep(1)
            continue

        message=messages[0]

        print(message.body)
        message.delete()
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
