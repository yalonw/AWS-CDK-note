# How tos
## Check the drift/diff status of configuration in the stack
1. Actual Resources configuration (Actual)
1. CloudFormation Console - Template configuration (CF)
1. AWS-CDK - Template configuration (CDK)

### **Lambda**
- 「＊」表示執行動作
- 「異動」包含新增、修改、刪除等

| CDK -deploy＊       | CF -deploy＊        | Actual＊ | CF -drift  | CDK -diff  | Actual |
| :------------------ |:--------------------| :------: | :--------: | :--------: | :----: |
| Template 中無此設定   | Template 中無此設定   | 有異動    | 檢測不到(X) | 檢測不到(X) |        |
| Template 中有此設定   | Template 中有此設定   | 新增      | 檢測不到(X) | 檢測不到(X) |        |
| Template 中有此設定   | Template 中有此設定   | 修改、刪除 | 發現異動(O) | 檢測不到(X) |        |
|
| 更改 Template 設定   |                      | 有異動    | 同步 Template |          | 覆蓋異動 |
| 沒更改 Template 設定 |                      | 有異動    | 同步 Template |          | 保留異動 |
|
|                     | 更改 Template 設定    | 有異動    |           | 不同步 有差異(O) | 覆蓋異動 |
|                     | 沒更改 Template 設定  | 有異動    |           | 不同步 有差異(O) | 保留異動 |

<br>

### **s3 Bucket - event notification**
| CDK -deploy＊                    | CF -deploy＊                     | Actual＊ | CF -drift  | CDK -diff  | Actual |
| :------------------------------- | :------------------------------ | :------: | :--------: | :--------: | :----: |
| Template 中有設定<br>notification | Template 中有設定<br>notification | 有異動    | 檢測不到(X) | 檢測不到(X) |         |
| 修改或刪除部分<br>notification     |                                  |         | 同步 Template |          | 覆蓋且<br>**全部重新創建** |
| 刪除所有 notification             |                                  |         | 同步 Template |          | [清空所有<br>包含手動新增的](https://github.com/aws/aws-cdk/issues/13797) |

<br>
<br>


## Importing Existing AWS Resources into AWS-CDK Stack
### NOTE:
- [AWS CloudFormation Console](https://console.aws.amazon.com/cloudformation/) support for importing existing resources into stack, but it is not yet supported in the AWS-CDK.
*[(Reference - 2020/03/09)](https://github.com/aws/aws-cdk/issues/6548#issuecomment-596223217)*

- A template that describes the entire stack, including both the resources that are already part of the stack and the resources to import.

- Each resource to import must have a [DeletionPolicy attribute](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html) in the template.
    + json code: `"DeletionPolicy": "Delete"`
    + python code: `construct.apply_removal_policy(cdk.RemovalPolicy.DESTROY)`

### STEP:
1. Use AWS-CDK to generate the CloudFormation resources configuration.

1. Run `cdk synth` to get the CloudFormation templates.
   - file path: `cdk.out/xxxStack.template.json`

1. Then use [AWS CloudFormation Console](https://console.aws.amazon.com/cloudformation/) to import it.
   - *Reference: [AWS Documentation1](https://aws.amazon.com/tw/blogs/aws/new-import-existing-resources-into-a-cloudformation-stack/)*
   - *Reference: [AWS Documentation2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import-existing-stack.html#resource-import-existing-stack-console)*
   - *Reference: [How to import existing AWS resources into CDK stack | by Maria Verbenko | Medium](https://medium.com/@visya/how-to-import-existing-aws-resources-into-cdk-stack-f1cea491e9)*

1. When it's done, run `drift` detection and go back to AWS-CDK run `cdk diff`, check the status is "There were no differences".

<br>
<br>


## Limitations of s3 event notification(s3 trigger)
- On the same s3 bucket, the event notification cannot share a common event type.
  (同一個 Bucket，不同 notification 的 event type 不能重複)

- AWS-CDK 底層[只能吃一個 event type](https://github.com/aws/aws-cdk/blob/c5a2addcd87ebb810dcac54c659fa60786f9d345/packages/%40aws-cdk/aws-s3/lib/notifications-resource/notifications-resource.ts#L55) ，但 CloudFormation Template 可以吃 list(event type).
  + 建議作法：對每個 event type 建立一個對應的 notification

- CloudFormation Template cannot assign id(event name).
  + ex: [AWS::S3::Bucket LambdaConfiguration](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html) doesn't have properties of id(event name).

    ```json
    {
    "Event" : String,
    "Filter" : NotificationFilter,
    "Function" : String
    }
    ```

- 其他相關討論：
  + *Reference: [How to add an event notification to an existing S3 Bucket | Stack Overflow](https://stackoverflow.com/questions/58087772/aws-cdk-how-to-add-an-event-notification-to-an-existing-s3-bucket/62247029#62247029)*
  + *Reference: [s3: allow defining bucket notifications for unowned buckets · Issue #2004 · aws/aws-cdk](https://github.com/aws/aws-cdk/issues/2004#issuecomment-702496473)*
  + *Reference: [feat(aws-s3): Add notifications to existing buckets by michaelbrewer · Pull Request #11773 · aws/aws-cdk](https://github.com/aws/aws-cdk/pull/11773)*
  + *Reference: [AWS Documentation: Event message structure - AWS s3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html)*
  + *Reference: [AWS Documentation: Configuring Amazon S3 event notifications - AWS s3](https://docs.aws.amazon.com/AmazonS3/latest/dev-retired/NotificationHowTo.html#how-to-enable-disable-notification-intro)*
  + *Reference: [AWS Documentation: AWS::S3::Bucket NotificationConfiguration - AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig.html#aws-properties-s3-bucket-notificationconfig-properties)*

<br>
<br>


## Importing an AWS CloudFormation template
```python
from aws_cdk import core
from aws_cdk import cloudformation_include as cfn_inc

class MyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        template = cfn_inc.CfnInclude(self, "Template",
            template_file="my-template.json")
```
> *Reference: [AWS Documentation](https://docs.aws.amazon.com/cdk/latest/guide/use_cfn_template.html)*

<br>
<br>


## Get access to the CFN Resource class
- Use `construct.node.default_child`
```python
# Get the AWS CloudFormation resource
cfn_bucket = bucket.node.default_child

# Change its properties
cfn_bucket.analytics_configuration = [
    {
        "id": "Config",
        # ...
    }
]
```
> *Reference: [AWS Documentation](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html#cfn_layer_resource)*

<br>
<br>


## Rename or Override Logical IDs
### **Override Logical ID**
```python
# python
construct.node.default_child.override_logical_id('new_id')
```
```js
// JavaScript
import * as cdk from '@aws-cdk/core';
import s3 = require('@aws-cdk/aws-s3');

export class MyStack extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const bucket = new s3.Bucket(this, 'MyBucket');
        const cfnBucket = bucket.node.defaultChild as cdk.CfnResource;
        cfnBucket.overrideLogicalId('MyBucket');
    }
}
```
> *Reference: [Thoughts about resource IDs · Issue #1424 · aws/aws-cdk](https://github.com/aws/aws-cdk/issues/1424#issuecomment-621307020)*

<br>

### **Rename Logical ID**
```python
# python
old_id = self.get_logical_id(construct.node.default_child)
self.rename_logical_id(old_id, 'new_id')
```
```js
// JavaScript
class MyStack extends Stack {
      constructor(parent: App, name: string, props: StackProps) {
        super(parent, name);

        // note that `renameLogical` must be called /before/ defining the construct.
        // a good practice would be to always put these at the top of your stack initializer.
        this.renameLogical('MyTableCD117FA1', 'MyTable');
        this.renameLogical('MyQueueAB4432A3', 'MyAwesomeQueue');

        new Table(this, 'MyTable');
        new Queue(this, 'MyQueue');
      }
 }
```
> *Reference: [Improve experience for renaming L1s · Issue #207 · aws/aws-cdk](https://github.com/aws/aws-cdk/issues/207#issuecomment-401510704)*

<br>
<br>


## About Logical Id of the resources
- *Reference: [Thoughts about resource IDs · Issue #1424 · aws/aws-cdk](https://github.com/aws/aws-cdk/issues/1424#issue-393751681)*
- *Reference: [Hash in the Logical Id of the resources in CDK/Cloudformation | Stack Overflow](https://stackoverflow.com/questions/56729322/hash-in-the-logical-id-of-the-resources-in-cdk-cloudformation)*

<br>

## Referencing? Importing?
- *Reference: [Support resource import · Issue #52 · aws/aws-cdk-rfcs](https://github.com/aws/aws-cdk-rfcs/issues/52#issuecomment-614178816)*