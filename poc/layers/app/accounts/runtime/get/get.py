from shared import endpoint, response

@endpoint
def handler(event, context):
    data = {
        'test': 'data'
    }

    return response(201, context, data)
