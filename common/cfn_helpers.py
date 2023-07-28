from aws_cdk import CfnCondition, CfnResource, Resource


def apply_condition(resource: Resource, condition: CfnCondition):
    # A condition must be assigned to the resource's level-1-equivalent
    l1_construct: CfnResource = resource.node.default_child
    l1_construct.cfn_options.condition = condition
