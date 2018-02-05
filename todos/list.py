import json

from todos.todo_model import TodoModel


def todo_list(event, context):
    # fetch all todos from the database
    results = TodoModel.scan()

    # create a response
    return {'statusCode': 200,
'headers': {
    "Access-Control-Allow-Origin" : "*", 
    "Access-Control-Allow-Credentials" : True                       
  },

            'body': json.dumps({'items': [dict(result) for result in results]})}
