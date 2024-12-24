import requests

def query(text,server='http://192.168.10.4:8080/completion'):
    headers = {'Content-Type':'application/json'}
    data = {
        "prompt":text,
        "n_predict":16
    }
    
    response = requests.post(
        url=server,
        headers=headers,
        json=data
    )
    return response.json()['content']
    pass

print(query(text="hello,i'm gin")) 