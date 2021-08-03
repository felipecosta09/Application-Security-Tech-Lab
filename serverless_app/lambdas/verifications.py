from aws_cdk import aws_lambda as lambda_


def day_one_verification_code():
    code = """import os
import json
import urllib3

HTTP = urllib3.PoolManager()

def main_handler(event, context):
    web_app_url = os.environ['WEB_APP_URL']
    backend_url = f'{web_app_url}/backend/'
    resp = HTTP.request('GET', backend_url)
    message = json.loads(resp.data).get('message')

    if message == 'Internal server error' or 'welcome to our secure website' in message.lower():
        return True
    
    else:
        raise Exception("Either your app is insecure, or you've missed a step!")
    
"""

    verification_code = lambda_.Code.from_inline(code)

    return verification_code


def day_two_verification_code():
    code = """import os
import json
import urllib3

HTTP = urllib3.PoolManager()

def main_handler(event, context):
    web_app_url = os.environ['WEB_APP_URL']
    backend_url = f'{web_app_url}/backend/'
    resp = HTTP.request('GET', backend_url)
    message = json.loads(resp.data).get('message')

    if 'welcome to our secure website' in message.lower():
        return True
    
    else:
        raise Exception("Either your app is insecure, or you've missed a step!")

"""

    verification_code = lambda_.Code.from_inline(code)

    return verification_code
