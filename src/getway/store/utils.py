import json

def upload(file, fs, sqsChannel, access):
    """ Upload the given file to mongodb using the given gridFS instance. Then inserts a messagge to SQS queue.

    Arguments:
        file {_type_} -- file to be updated
        fs {_type_} -- gridFS Instance
        sqsChannel {_type_} -- AWS SQS channel
        access {_type_} -- user access information
    """


print(upload.__doc__)