import os, requests

def token(request):

    if not "Authorization" in request.headers:
        return None, ("Unauthorized", 401)

    header_token = request.headers["Authorization"]

    response = requests.post(f"{os.environ.get('AUTH_SERVICE_URL')}/validate",headers={"Authorization":header_token})
    
    if response.status_code == 200:
        return response.text, None
    
    return None, (response.text, response.status_code)