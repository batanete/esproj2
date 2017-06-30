import sqs
import s3
import signal
import rekognition
import dynamodb
from time import sleep


def init():
    #s3.init()
    #simpledb.init()
    sqs.init()
    s3.init()
    dynamodb.init()
    rekognition.init()

def exit(signal,frame):
    sqs.exit()


def main():
    init()
    sqs.deleteAllMessages()

    #signal.signal(signal.SIGINT,exit)
    while True:
        #checks for messages each time a second passes(prevent active wait)
        sleep(1)
        messages=sqs.inputqueue.receive_messages()

        if len(messages)<1:
            continue

        for message in messages:
            body=message.body

            print('request received:',body)

            toks=body.split(':')

            amount=int(toks[1])
            filename=toks[0]

            #get photo bytes from s3 bucket
            #get user name associated with photo
            #user=rekognition.get_user(filename)
            username=rekognition.get_user_bytes(s3.get_request_photo(filename))

            if username is None:
                resp='user not recognised'
            else:
                #get user details
                user=dynamodb.get_user(username)
                money=user['money']
                res=money-amount
                if(res<0):
                    resp='manual payment'
                else:
                    dynamodb.update_money(username,res)
                    resp='auto payment'

            print('response:'+resp)
            sqs.post_response(resp)

            #TODO: send answer to user via outputqueue, handle payment

            #deletes request photo after processing request
            s3.delete_request_photo(filename)
            #message.delete()

if __name__ == "__main__":
    main()
