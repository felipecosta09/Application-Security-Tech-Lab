# Application Security - Tech lab

Participants must first secure their vulnerable Lambda function using Application Security. 

Next, they must use Application Security's stack trace to identify & remove the vulnerbale line of code.

## Game steps
### Setup

Deploy the `cfn.yaml` CloudFormation template.

### Challenge #1

1. Obtain the web app's API Gateway URL from the CloudFormation output 
2. Browse to web app to confirm it's vulnerable
   
    The website will have a red background and a message informing you that the page is insecure

3. Add Application Security layer ARN to Lambda. Use Python 3.8 & the [custom runtime](https://cloudone.trendmicro.com/docs/application-security/aws-lambda-with-custom-runtimes/) method
4. Create an Application Security group
5. Set the group's "Illegal File Access" module to mitigate
6. Pass in Application Security group's keys to the Lambda via [environment variables](https://cloudone.trendmicro.com/docs/application-security/environment-variables/)
7. Browse to the web app to confirm it's secure 

   The website will now have a green background and a message informing you that the page has been secured

### Challenge #2

1. Use Application Security stack trace to identify the vulnerable line of code. It will be this one:
   ```
   f = open(vars_file_path, "r"); f.readline(); f.close(); message = {"message": "Welcome to our website"}
   ```
2. Remove the vulnerable line
3. Deploy the updated Lambda
4. Browse to the wep app to confirm it's secure

    The website will now have a yellow background and a message informing you that the vulnerability has been removed

## Developer notes
### Generate CloduFormation

```
cdk synth --version-reporting=false --path-metadata=false --asset-metadata=false > cfn.yaml
```