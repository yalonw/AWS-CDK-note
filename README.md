# AWS CDK

- [AWS Cloud Development Kit (AWS CDK)](https://aws.amazon.com/tw/cdk/)
- [Working with the AWS CDK in Python](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-python.html)
- [AWS official of CDK example code](https://github.com/aws-samples/aws-cdk-examples/tree/master/python)


## **Prerequisites**
### Install
- Python 3.6 or later
- Node.js 10.13 or later
- AWS CDK Toolkit（the cdk command)
  ```
  yarn global add aws-cdk
  ```

### Initial Settings
- [Setting AWS configure](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_prerequisites):
  provide AWS access key ID, secret access key, and default region
  1. In `~/.aws/config` or `%USERPROFILE%\.aws\config`
        ```
      [default]
      region=ap-northeast-1
      ```
  2. In `~/.aws/credentials` or `%USERPROFILE%\.aws\credentials`
      ```
      [default]
      aws_access_key_id=
      aws_secret_access_key=
      ```

- [Bootstrapping](https://aws-ci-cd.workshop.aws/20-infrastructure/200-cdk-bootstrap.html):
  bootstrap the CDK into your account and region. This is a one-time operation that creates the resources necessary to allow CDK deployments in your AWS account to a given region.
  ```
  cdk bootstrap aws://{account}/{region}
  ```
<br>

## **Creat Project**

```
mkdir my-project
cd my-project
cdk init app --language python

python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt
```
> It is best to edit requirements.txt  manually rather than using `pip3 freeze > requirements.txt`. The requirements.txt should list only top-level dependencies (modules that app depends on directly) and not the dependencies of those modules. This strategy makes updating the dependencies simpler. The requirements.txt file might look like [this](requirements.txt).

<br>

## **Deploy Project**
```
cdk deploy
```


<br>
<br>

## **How tos**
- [Check the drift/diff status of configuration in the stack](HOWTOs.md#Check-the-drift/diff-status-of-configuration-in-the-stack)
- [Importing Existing AWS Resources into AWS-CDK Stack](HOWTOs.md#Importing-Existing-AWS-Resources-into-AWS-CDK-Stack)

<br>

## Reference
### [AWS CDK API Reference - Python](https://docs.aws.amazon.com/cdk/api/latest/python/modules.html)
### [AWS CloudFormation Template Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)

### [AWS CDK CLI](https://aws.amazon.com/cdk/features/?nc1=h_ls)
- **`cdk init`**:
   Initialize a new, default application in the language of your choice.
- **`cdk synth`**:
   Compile your AWS CDK application into an AWS CloudFormation template.
- **`cdk diff`**:
   See a “diff” between your local AWS CDK code and the running application in AWS.
- **`cdk deploy`**:
   Deploy your AWS CDK application into testing or production via AWS CloudFormation.
- **`cdk destroy`**:
   Destroying the app's(stack) resources.