from flask import Flask, request
from flask_mysqldb import MySQL
import jwt, os, datetime

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
    

@server.route("/login", methods=["POST"]) 
def login():
    auth = request.authorization

    if not auth:
        return "missing credentials", 401
    
    cursor = mysql.connection.cursor()
    try:
        res = cursor.execute(
            "SELECT email, password FROM user WHERE email= %s", (auth.username,)
        )
    except:
        print(f"--> username:{type(auth.username)}\n-->password:{auth.password}")
        return "User or Password is invalid", 401
    if res > 0:
        credentials_row = cursor.fetchone()
        email = credentials_row[0]
        password = credentials_row[1]

        if auth.username == email or auth.password == password:
            try: 
                return createJWT(email,os.environ.get("JWT_SECRET"),True)
            except:
                print (os.environ.get("JWT_SECRET"))
                return  "Internal server error", 501
        return "Invalid credentials", 401
    return "Invalid credentials", 401


@server.route("/validate", methods=["POST"])
def validate():
    try:
        auth_encoded_JWT = request.authorization
        if auth_encoded_JWT.type == "bearer":
            token_encoded_JWT = auth_encoded_JWT.token
            decoded_JWT = jwt.decode(
                token_encoded_JWT,
                os.environ.get("JWT_SECRET"),
                algorithms=["HS256"]
            )
            print(decoded_JWT)
            return decoded_JWT, 200
        return "Unauthorized", 401
    
    except Exception as e:
        print (f"-->{e}")

        if type(e) == jwt.ExpiredSignatureError:
            return str(e), 498
        return "Missing authorization header", 401


@server.route("/test", methods=["GET"])
def test():
    try:
        cursor = mysql.connection.cursor()
        tables = cursor.execute("SHOW tables;")
        print(tables)
        return 'success test', 200
    except Exception as e:
        print (e)
        return 'error test', 501

def createJWT(username, secret, authz):
    return jwt.encode({
        "username":username,
        "exp":datetime.datetime.now(tz=datetime.timezone.utc)
        + datetime.timedelta(days=1),
        #issue at
        "iat":datetime.datetime.utcnow(),
        "admin":authz
    },secret,algorithm="HS256")
    

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=5000)