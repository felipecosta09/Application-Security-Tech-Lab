from aws_cdk.core import Tags
from aws_cdk import (
    core as cdk,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
)


from lambdas.frontend import get_frontend_page_code
from lambdas.backend import get_backend_page_code
from lambdas.verifications import day_one_verification_code, day_two_verification_code


class ServerlessAppStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # get API GW
        web_app_api_gw = self.get_web_app_api_gw()
        self.api_url = web_app_api_gw.url

        # Add API gateway resources
        self.add_frontend_page(web_app_api_gw)
        self.add_backend_page(web_app_api_gw)

        # Add verificaiton Lambdas
        self.add_day_one_verification_lambda()
        self.add_day_two_verification_lambda()

    def get_web_app_api_gw(self):
        web_app_api_gw = apigateway.RestApi(
            self,
            "application-security-web-app",
            rest_api_name="Application Secuirty - Serverless Web App",
            description="Our very first serverless app!",
        )

        Tags.of(web_app_api_gw).add("Name", "ApplicationSecurityVulnerableWebApp")

        cdk.CfnOutput(
            self,
            "ApplicationSecurityWebAppUrl",
            value=web_app_api_gw.url,
            description="Application Security Web app URL",
            export_name="ApplicationSecurityWebAppUrl",
        )

        return web_app_api_gw

    def add_frontend_page(self, web_app_api_gw):
        web_app_code = get_frontend_page_code()

        web_app_handler = lambda_.Function(
            self,
            "ApplicationSecurityFrontendPage",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=web_app_code,
            handler="index.main_handler",
            function_name="ApplicationSecurityFrontendPage",
            description="Application Security Web GUI",
        )

        Tags.of(web_app_handler).add("Name", "ApplicationSecurityFrontendPage")

        app_integration = apigateway.LambdaIntegration(
            web_app_handler,
            # request_templates={"application/json": '{ "statusCode": "200" }'},
            request_templates={"text/html": '{ "statusCode": "200" }'},
        )

        web_app_api_gw.root.add_method("GET", app_integration)

    def add_backend_page(self, web_app_api_gw):
        web_app_code = get_backend_page_code()
        backend_lambda_name = "ApplicationSecurityBackendPage"

        web_app_handler = lambda_.Function(
            self,
            backend_lambda_name,
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=web_app_code,
            handler="index.main_handler",
            function_name=backend_lambda_name,
            description="Application Security Vulnerable app - PLEASE SECURE ME!",
            memory_size=512,
            timeout=cdk.Duration.seconds(10),
        )

        Tags.of(web_app_handler).add("Name", backend_lambda_name)

        app_integration = apigateway.LambdaIntegration(
            web_app_handler,
            # request_templates={"application/json": '{ "statusCode": "200" }'},
            request_templates={"text/html": '{ "statusCode": "200" }'},
        )

        backend = web_app_api_gw.root.add_resource("backend")
        backend.add_method("GET", app_integration)

        Tags.of(backend).add("Name", "ApplicationSecurityBackend")

        backend_lambda_code = f"https://{self.region}.console.aws.amazon.com/lambda/home?region={self.region}#/functions/{backend_lambda_name}?tab=code"
        cdk.CfnOutput(
            self,
            "ApplicationSecurityBackendLambdaCode",
            value=backend_lambda_code,
            description="Application Security Backend Lambda code",
            export_name="ApplicationSecurityBackendLambdaCode",
        )

        cdk.CfnOutput(
            self,
            "ApplicationSecurityBackendLambdaFunctionArn",
            value=web_app_handler.function_arn,
            description="Application Security Backend Lambda function ARN",
            export_name="ApplicationSecurityBackendLambdaFunctionArn",
        )

    def add_day_one_verification_lambda(self):
        verification_code = day_one_verification_code()

        day_one_lambda = lambda_.Function(
            self,
            "ApplicationSecurityDayOneVerificationLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=verification_code,
            handler="index.main_handler",
            function_name="ApplicationSecurityDayOneVerificationLambda",
            description="Application Security Day One verificaiton",
            timeout=cdk.Duration.seconds(10),
            environment={"WEB_APP_URL": self.api_url,},
        )

        Tags.of(day_one_lambda).add(
            "Name", "ApplicationSecurityDayOneVerificationLambda"
        )

    def add_day_two_verification_lambda(self):
        verification_code = day_two_verification_code()

        day_two_lambda = lambda_.Function(
            self,
            "ApplicationSecurityDayTwoVerificationLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=verification_code,
            handler="index.main_handler",
            function_name="ApplicationSecurityDayTwoVerificationLambda",
            description="Application Security Day Two verificaiton",
            timeout=cdk.Duration.seconds(10),
            environment={"WEB_APP_URL": self.api_url,},
        )

        Tags.of(day_two_lambda).add(
            "Name", "ApplicationSecurityDayTwoVerificationLambda"
        )
