import os, pika, gridfs, json
from flask import Flask, request, send_file
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
            return "Required file is missing or more that one file was sent.", 400
        
        for fileName,file in request.files.items():
            # upload image to mongo and insert queue on AWS SQS
            err = utils.upload(file,fs_image,access)
            print(f"--> format '{fileName}' uploaded by user {access['username']}")

        if err:
            return err
        
        return "Success upload!", 200
        

@server.route("/download", methods=["POST"])
def download():

    response, err = validate.token(request)
    if err:
        return err
    
    access = json.loads(response)
    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is missing", 400
        
        try:
            out = fs_text.get(fid_string)

            return send_file(out,download_name=f"{fid_string}.pdf")

        except Exception as exc:
            print(exc)
            return "Internal server error", 400

        
    return "Not authorized", 400
        

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=4000, debug= True)