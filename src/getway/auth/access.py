import os, requests

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing credentials", 401)
    
    basicAuth = (auth.username, auth.password)

    response = requests.post(f"{os.environ.get('AUTH_SERVICE_URL')}/login", auth=basicAuth)

    if response.status_code == 200:
        return response.text, None
    return None, (response.text, response.status_code)