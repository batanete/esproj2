value=`cat faces/messiother.jpg`

aws rekognition search-faces-by-image --collection-id 'faces' --region 'us-west-2' --image '{"S3Object":{"Bytes":$value}'

#aws rekognition search-faces-by-image --collection-id 'faces' --region 'us-west-2' --image '{"S3Object":{"Bucket":"es2bata","Name":"messiother.jpg"}}'
