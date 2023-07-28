from aws_cdk import CfnCondition, Resource


def apply_condition(resource: Resource, condition: CfnCondition):
    cfn_options = resource.node.default_child.cfn_options
    cfn_options.condition = condition
