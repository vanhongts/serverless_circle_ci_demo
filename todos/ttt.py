import json
import random
import logging



def get(event, context):
    # create a responsei
    params = event['queryStringParameters']

    try:
        gid = params['g']
        pid = params['p']
    except KeyError:
        return {'statusCode': 422
                , 'headers': {
                        "Access-Control-Allow-Origin" : "*", 
                        "Access-Control-Allow-Credentials" : True 
                },
                'body': json.dumps({'error_message': 'Params is not valid'})}
    

    with open('todos/entry.json', 'r', encoding='utf-8') as f:
        entry = json.load(f, object_hook=from_json)

    result = None
    for item in entry:
        if (item['guest']['customer_id'] == int(gid) and item['property']['property_id'] == int(pid)):
            result = item
            break;
    if result is None:
        return {'statusCode': 422,
'headers': {
    "Access-Control-Allow-Origin" : "*",
    "Access-Control-Allow-Credentials" : True
  },'body': 'Data does not exist'}

    return {'statusCode': 201,
'headers': {
    "Access-Control-Allow-Origin" : "*",
    "Access-Control-Allow-Credentials" : True
  },'body': json.dumps(result)}



def check_pass(event, context):
    logging.error("Event: {0}".format(event))
    params = event['queryStringParameters']

    try:
        login = params['txtUserName']
        password = params['txtPassword']
    except KeyError:
        return {'statusCode': 422
                , 'headers': {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                },
                'body': json.dumps({'error_message': 'Params is not valid'})}


    with open('todos/data.json', 'r', encoding='utf-8') as f:
        entry = json.load(f, object_hook=from_json)

    cookie_string = "TTT%5FUType={0}; Max-Age=0".format('empty')
    for item in entry:
        if (item['usr'] == str(login) and item['pwd'] == str(password)):
            cookie_string = "TTT%5FUType={0};".format(item['type'])
            break;
    return {'statusCode': 201,
		'headers': {
			    "Access-Control-Allow-Origin" : "*",
			    "Access-Control-Allow-Credentials" : True,
                            "Set-Cookie": cookie_string,
		  }}
def from_json(json_object):
    if '__class__' in json_object:
        if json_object['__class__'] == 'time.asctime':
            return time.strptime(json_object['__value__'])
        if json_object['__class__'] == 'bytes':
            return bytes(json_object['__value__'])
    return json_object
