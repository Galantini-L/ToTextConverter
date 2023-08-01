import json

def upload(file, fs, sqsChannel, access):
    """ Upload the given file to mongodb using the given gridFS instance. Then inserts a messagge to SQS queue.

    Arguments:
        file {_type_} -- file to be updated
        fs {_type_} -- gridFS Instance
        sqsChannel {_type_} -- AWS SQS channel
        access {_type_} -- user access information    
    
    {
        "Version": "2012-10-17",
        "Id": "__default_policy_ID",
        "Statement": [
            {
            "Sid": "__owner_statement",
            "Effect": "Allow",
            "Principal": {
                "AWS": "917414156098"
            },
            "Action": [
                "SQS:*"
            ],
            "Resource": "arn:aws:sqs:us-east-2:917414156098:image-to-convert-queue.fifo"
            }
        ]
    }
    """

    

    