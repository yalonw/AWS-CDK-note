from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
    aws_s3_notifications,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_cloudwatch as cloudwatch,
    aws_iam as iam,
)

class BaseTemplateStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create Lambda-Role
        # doc: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_iam/Role.html
        base_lambda_role = iam.Role(
            self, 'base_lambda_service_role_lgcid',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            ],
        )

        # reference to already existing Lambda-Role
        existing_lambda_role = iam.Role.from_role_arn(
            self, 'existing_lambda_role_lgcid',
            role_arn='arn:aws:iam::ACCOUNTID:role/service-role/ROLENAME'
        )

        # create Lambda-Layer
        base_lambda_layer = _lambda.LayerVersion(
            self, 'base_lambdaLayer_lgcid',
            code=_lambda.AssetCode('./layer/example'),
            # code=_lambda.AssetCode('./layer/pandas.zip'),
            layer_version_name='example_phscid',
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_8,
            ],
        )

        # reference to already existing Lambda-Layer
        existing_lambda_layer = _lambda.LayerVersion.from_layer_version_arn(
            self, 'existing_lambda_layer_lgcid',
            layer_version_arn='arn:aws:lambda:REGION:ACCOUNTID:layer:LAYERNAME:VERSION',
        )

        # reference to already existing lambda code from s3 Bucket
        existing_lambda_code_bucket = s3.Bucket.from_bucket_attributes(
            self, 'existing_lambda_code_bucket_lgcid',
            bucket_name='existing_lambda_code_bucket_phscid',
        )

        # create Lambda function
        # doc: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Function.html
        base_lambda = _lambda.Function(
            self, 'base_lambda_lgcid',
            function_name='base_lambda_phscid',
            code=_lambda.AssetCode('./lambda'),
            # code=_lambda.S3Code(
            #     bucket=existing_lambda_code_bucket,
            #     key='lambda/lambda_function.py'
            # ),
            handler='lambda_function.lambda_handler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            role=base_lambda_role,
        )
        base_lambda.add_environment('kk', 'vv')
        base_lambda.add_layers(base_lambda_layer)
        # Each resource to import must have a DeletionPolicy attribute in the template.
        base_lambda.apply_removal_policy(cdk.RemovalPolicy.DESTROY)


        # create s3 Bucket
        # doc: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        base_s3 = s3.Bucket(
            self, "base_s3bucket_lgcid",
            bucket_name='base_s3bucket_phscid',
        )
        base_s3.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        # grant permission to lambda to access to s3 Bucket
        base_s3.grant_read_write(base_lambda)
        base_lambda.add_environment("BUCKET_NAME", base_s3.bucket_name)

        # create s3 notification for Lambda Function
        base_s3.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            aws_s3_notifications.LambdaDestination(base_lambda)
        )


        # create Lambda-Apigetway
        base_lambda_api = apigw.LambdaRestApi(
            self, 'base_lambda_api_lgcid',
            handler=base_lambda,
        )


        # create dynamo table
        base_dynamotable = dynamodb.Table(
            self, "base_dynamotable_lgcid",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
        )
        # grant permission to lambda to access to dynamo table
        base_dynamotable.grant_read_write_data(base_lambda)
        base_lambda.add_environment("TABLE_NAME", base_dynamotable.table_name)


        # create cloudwatch



        # override all constructs Logical id
        self.override_all_lgcid()

    def override_all_lgcid(self):
        for c in self.node.children:
            return c.node.default_child.override_logical_id(c.node.id)

    def override_lgcid(self, constructs):
        return constructs.node.default_child.override_logical_id(constructs.node.id)
