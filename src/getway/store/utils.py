import json
import boto3
import os
from botocore.exceptions import ClientError 

def upload(file, fs, access):
    """ Upload the given file to mongodb using the given gridFS instance. 
        After uploading to mongo, inserts a messagge to SQS queue.

    Arguments:
        file {_type_} -- file to be updated
        fs {_type_} -- gridFS Instance
        access {_type_} -- user access information    
    
    """

    try:
        fid = fs.put(file)
    except Exception as e:
        print(e)
        return "Internal server error", 501
    
    message = {
        "image_fid":str(fid),
        "text_fid":None,
        "username":access["username"]
    }

    message_atribute = {}

    try:
        sqs =  boto3.resource("sqs")
        queue = sqs.get_queue_by_name(QueueName = os.environ.get('SQS_QUEUE_NAME'))
        response = queue.send_message(
            MessageBody = json.dumps(message),
            MessageAttributes = message_atribute
        )
        print(f"--> Message sent: {response.get('MessageId')}")
    except ClientError as err:
        print(err)
        fs.delete(fid)
        return "Internal server Error", 501
