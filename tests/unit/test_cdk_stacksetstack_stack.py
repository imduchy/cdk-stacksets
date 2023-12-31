import aws_cdk as core
import aws_cdk.assertions as assertions

from stackset.stack import BaselineConfigStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_stacksetstack/cdk_stacksetstack_stack.py


def test_sqs_queue_created():
    app = core.App()
    stack = BaselineConfigStack(app, "cdk-stacksetstack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
