from aws_cdk import aws_lambda as lambda_


def get_frontend_page_code():
    code = """import json
import urllib3
import boto3

HTTP = urllib3.PoolManager()

REQUIRED_ENV_VARS = ['TREND_AP_SECRET', 'TREND_AP_KEY']
REQUIRED_LAYER_ARN = 'arn:aws:lambda:us-east-1:800880067056:layer:CloudOne-ApplicationSecurity-runtime-python3_8:1'.lower()


INSECURE_HTML = '''
<!DOCTYPE html>
<html>
<title>ACME App</title>
<body style="background-color:red;">

<h1>Oh no!</h1>
<p>Either your app is insecure, or you've missed a step!</p>
</body>
</html>
'''

SECURE_HTML_DAY_ONE = '''
<!DOCTYPE html>
<html>
<title>ACME App</title>
<body style="background-color:lightgreen;">

<h1>Congratulations!</h1>
<p>It looks like you've enabled Application Security!</p>
<p>Just to be sure though, <b>check the Application Security dashboard</b>. If you don't see attacks being blocked, 
you might have missed a step!</p>
</body>
</html>
'''

SECURE_HTML_DAY_TWO = '''
<!DOCTYPE html>
<html>
<title>ACME App</title>
<body style="background-color:yellow;">

<h1>Congratulations!</h1>
<p>You've removed the bug from your code!</p>
</body>
</html>
'''

SECURE_DAY_ONE_PAYLOAD = {
            "statusCode": 200,
            "body": SECURE_HTML_DAY_ONE,
            "headers": {
            'Content-Type': 'text/html',
            }
        }

SECURE_DAY_TWO_PAYLOAD = {
            "statusCode": 200,
            "body": SECURE_HTML_DAY_TWO,
            "headers": {
            'Content-Type': 'text/html',
            }
        }
        
INSECURE_PAYLOAD = {
            "statusCode": 200,
            "body": INSECURE_HTML,
            "headers": {
            'Content-Type': 'text/html',
            }
        }
    

def _get_lambda_config(function_name='ApplicationSecurityBackendPage'):
    client = boto3.client('lambda')
    response = client.get_function_configuration(
        FunctionName=function_name,
    )

    return response


def _get_backend_url(event):
    domain_name = event['requestContext']['domainName']
    stage_name = event['requestContext']['stage']
    backend_url = f'https://{domain_name}/{stage_name}/backend'
    
    return backend_url

def check_required_env_vars():
    lambda_config = _get_lambda_config()
    env_vars = lambda_config['Environment']['Variables'].keys()
    print(f'Env vars: {env_vars}')
    required_env_vars_set = all(var in env_vars for var in REQUIRED_ENV_VARS)
    
    return required_env_vars_set

def check_required_layer():
    lambda_config = _get_lambda_config()

    try:
        configured_layer = lambda_config['Layers'][0]['Arn']
        print(f'Configured layer: {configured_layer}')
        return configured_layer

    except KeyError:
        print('No layers configured')
        return ''
    

def main_handler(event, context):
    backend_url = _get_backend_url(event)
    resp = HTTP.request('GET', backend_url)
    print(f'Status: {resp.status}')
    message = json.loads(resp.data).get('message')
    print(f'Message: {message}')
    
    required_env_vars = check_required_env_vars()
    required_layer = check_required_layer()

    if not required_env_vars:
        print('Required environment variables are not set')
        return INSECURE_PAYLOAD
        
    elif required_layer.lower() != REQUIRED_LAYER_ARN:
        print('Required layer is not set')
        return INSECURE_PAYLOAD

    elif resp.status == 502:
        print('Received 502 - Day 1 task is complete')
        return SECURE_DAY_ONE_PAYLOAD

    elif resp.status == 200 and 'welcome to our secure website' in message.lower():
        print('Received 200 & correct welcome message - Day 2 task is complete')
        return SECURE_DAY_TWO_PAYLOAD

    else:
        return INSECURE_PAYLOAD


    return resp

"""

    web_app = lambda_.Code.from_inline(code)

    return web_app
