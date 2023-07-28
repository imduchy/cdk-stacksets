import aws_cdk as cdk
from cdk_stacksets import (Capability, DeploymentType, StackSet,
                           StackSetTarget, StackSetTemplate)
from constructs import Construct

from baseline.resources import BaselineResources


class BaselineStackSet(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        baseline_resources = BaselineResources(self, "BaselineResources")

        StackSet(
            self,
            'BaselineStackSet',
            deployment_type=DeploymentType.service_managed(),
            template=StackSetTemplate.from_stack_set_stack(baseline_resources),
            capabilities=[Capability.NAMED_IAM],
            target=StackSetTarget.from_organizational_units(
                regions=['eu-west-1', 'eu-central-1'],
                organizational_units=['ou-1c8h-oj29wirz']
            )
        )
