import boto3
import json


PATHREQS='es3reqs'
PATHFACES='es3faces'

keys=[
    "AKIAJMMEIX7PDFFUDFQQ",
    "Gw6LsMMTdsJbSdvEUtLqbZsG2U7+vOl3EZaPACe6"
]



def init():
    global s3,rekogclient
    s3 = boto3.resource('s3','us-west-2', aws_access_key_id = keys[0], aws_secret_access_key = keys[1])
    rekogclient=boto3.client('rekognition','us-west-2', aws_access_key_id=keys[0], aws_secret_access_key=keys[1])


#returns bytes from photo with the given filename from requests bucket folder
def get_request_photo(filename):
    print('path: es2bata',PATHREQS+'/'+filename)
    
    
    obj=s3.Object('es2bata',PATHREQS+'/'+filename).get()

    photobytes = obj['Body'].read()
    #print(photobytes)

    return photobytes



#gets the user which looks the most like the given photo (minimum 80% similarity)
def get_user_bytes(photobytes):
    try:
        res=rekogclient.search_faces_by_image(
            CollectionId='faces',
            Image={
                'Bytes':photobytes
            },
    
            MaxFaces=1
        )
    #no faces match
    except:
        return None
    matches=res['FaceMatches']

    if len(matches)==0:
        return None

    match=matches[0]
    similarity=match['Similarity']
    user=match['Face']['ExternalImageId']
    print(similarity,user)
    return user

#deletes request photo file from bucket.returns True on success
def delete_request_photo(filename):
    response = s3.Object('es2bata', PATHREQS+'/'+filename).delete()


def authentication(event,context):

    
    filename=str(event['filename'])
    amount=int(event['amount'])

    init()

    res=get_request_photo(filename)
    username=get_user_bytes(res)
    delete_request_photo(filename)

    if username is None:
        res = {"auth":0,"payment_type":"failed auth"}
    else:
        res = {"auth":1,"username":username,"amount":amount}

    return res
    
