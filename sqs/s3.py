import boto3

import json

PATHREQS='es3reqs'
PATHFACES='es3faces'

def get_keys():
    global keys
    with open('keys','r') as f:
        lines=f.readlines()
        keys=[]
        keys.append(lines[0].replace('\n',''))
        keys.append(lines[1].replace('\n',''))

def init():
    global s3
    get_keys()
    s3 = boto3.resource('s3','us-west-2', aws_access_key_id = keys[0], aws_secret_access_key = keys[1])


#post a request's auth photo on the s3 bucket
def post_photo(photofile,filename):
    s3.Bucket('es2bata').put_object(Key = PATHREQS+'/'+filename, Body = photofile)
    print(PATHREQS+'/'+filename)

#returns bytes from photo with the given filename from requests bucket folder
def get_request_photo(filename):

    obj=s3.Object('es2bata',PATHREQS+'/'+filename).get()

    photobytes = obj['Body'].read()
    #print(photobytes)

    return photobytes

#deletes request photo file from bucket.returns True on success
def delete_request_photo(filename):
    response = s3.Object('es2bata', PATHREQS+'/'+filename).delete()

    #return response['DeleteMarker']


#init()
#get_photo('rooney.jpg')
