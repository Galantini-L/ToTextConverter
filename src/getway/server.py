import os, pika, gridfs, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import access, validate
from store import utils


"""
    To do for production:
        - mongo_img/txt: env var for uri
        - debug mode FALSE
        - access.py: env var for url loggin service
"""

server = Flask(__name__)

try:
    mongo_image = PyMongo(server, os.environ.get("MONGO_IMAGES"))
    mongo_text = PyMongo(server, os.environ.get("MONGO_IMAGES"))
    
    fs_image= gridfs.GridFS(mongo_image.db)
    fs_text= gridfs.GridFS(mongo_text.db)

except Exception as e:
    print (f"--> [*] ERROR: Error while connecting to mongodb\n \t[*] {e}")


sqsChannel = None

@server.route("/test", methods=["GET"])
def testConnection():   
    try: 
        #isMongo = mongo_image.db.get_collection
        #print ("=> [x] Result: %r" %isMongo)
        return "True", 200
    except Exception as e:
        print(e)
        return "False", 500
    

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if err:
        print(f"--> {err}")
        return err
    return token


@server.route("/upload", methods=["POST"])
def upload():
    response, err = validate.token(request)
    
    if err:
        return err
    
    print(f"--> {response}")
    access = json.loads(response)

    if access["admin"]:
        if len(request.files) != 1:
            return "Required file is missing or more that one file is given.", 400
        
        for fileName,file in request.files.items():
            # upload image to mongo and insert queue on AWS SQS
            err = utils.upload(file,fs_image,sqsChannel,access)
            print(f"--> format '{fileName}' uploaded by user {access['username']}")

        if err:
            return err
        
        return "Success upload!", 200
        

@server.route("/download", methods=["POST"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=4000, debug= True)