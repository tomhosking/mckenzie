

def application(environ, start_response):
    output = 'Welcome to mckenze proxy!'

    response_headers = [
        ('Content-Length', str(len(output))),
        ('Content-Type', 'text/plain'),
    ]

    start_response('200 OK', response_headers)

    return [bytes(output, 'utf-8')]