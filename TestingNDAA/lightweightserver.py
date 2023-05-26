from wsgiref.simple_server import make_server
import requests

def application(environ, start_response):
    path = environ['PATH_INFO']
    if path == '/':
        placeOrder_response = requests.post('http://localhost:8000/placeOrder')
        response = placeOrder_response
    elif path == '/logs':
        response = 'Logs'
    elif path == '/placeOrder':
        if environ['REQUEST_METHOD'] == 'GET':
            response = 'here are those logs you requested!'
        elif environ['REQUEST_METHOD'] == 'POST':
            pay_response = requests.get('http://localhost:8000/pay')
            response = pay_response
        else:
            response = 'Invalid request method'
    elif path == '/gatherLogs':
        # Make a GET request to /placeOrder
        placeOrder_response = requests.get('http://localhost:8000/placeOrder')
        response = placeOrder_response
    elif path == '/pay':
        response = 'payment pushed!'
    else:
        response = 'Invalid path'
    
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [response.encode()]

if __name__ == '__main__':
    with make_server('', 8000, application) as server:
        print('Server started on http://localhost:8000')
        server.serve_forever()