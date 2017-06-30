import boto3

REGION='us-west-2'
PATHREQS='es3reqs'

def get_keys():
    global keys
    with open('keys','r') as f:
        lines=f.readlines()
        keys=[]
        keys.append(lines[0].replace('\n',''))
        keys.append(lines[1].replace('\n',''))


def init():
    global rekogclient
    get_keys()
    rekogclient=boto3.client('rekognition',REGION, aws_access_key_id=keys[0], aws_secret_access_key=keys[1])

    try:
        response = rekogclient.create_collection(
            CollectionId='faces'
        )
    #collection already exists
    except:
        pass



#adds a face to the collection
def add_face(username,imagebytes):
    rekogclient.index_faces(
        CollectionId='faces',
        ExternalImageId=username,
        Image={'Bytes': imagebytes}
    )

#add sample faces to the collection
def add_faces():
    for user in ['rooney','messi','ronaldo']:
        with open('faces/'+user+'.jpg','rb') as f:
            imagebytes=f.read()
            add_face(user,imagebytes)

#gets the user which looks the most like the given photo (minimum 80% similarity)
def get_user(photopath):

    print(photopath)
    print(PATHREQS+'/'+photopath)

    res=rekogclient.search_faces_by_image(
        CollectionId='faces',
        Image={
            'S3Object': {
                'Bucket':'es2bata',
                'Name':PATHREQS+'/'+photopath
            }
        },

        MaxFaces=1
    )

    matches=res['FaceMatches']

    if len(matches)==0:
        return None

    match=matches[0]
    similarity=match['Similarity']
    user=match['Face']['ExternalImageId']
    print(similarity,user)
    return user

#gets the user which looks the most like the given photo (minimum 80% similarity)
def get_user_bytes(photobytes):
    res=rekogclient.search_faces_by_image(
        CollectionId='faces',
        Image={
            'Bytes':photobytes
        },

        MaxFaces=1
    )

    matches=res['FaceMatches']

    if len(matches)==0:
        return None

    match=matches[0]
    similarity=match['Similarity']
    user=match['Face']['ExternalImageId']
    print(similarity,user)
    return user



init()
#add_faces()
get_user_bytes(open('faces/messiother.jpg','rb').read())
