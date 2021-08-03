from aws_cdk import aws_lambda as lambda_


def get_backend_page_code():
    code = """import json
vars_file_path = '../../proc/self/environ'

def main_handler(event, context):
    message = {"message": "Welcome to our secure website"}
    f = open(vars_file_path, "r"); f.readline(); f.close(); message = {"message": "Welcome to our website"}
    
    return {
        "statusCode": 200,
        "body": json.dumps(message),
    }
    
"""

    web_app = lambda_.Code.from_inline(code)

    return web_app
