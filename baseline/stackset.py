import aws_cdk as cdk
from cdk_stacksets import (Capability, DeploymentType, OperationPreferences,
                           RegionConcurrencyType, StackSet, StackSetTarget,
                           StackSetTemplate)
from constructs import Construct

from baseline.resources import BaselineResourcesStack


class BaselineStackSet(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        baseline_resources = BaselineResourcesStack(self, 'BaselineResourcesStack')

        StackSet(
            self,
            'BaselineStackSet',
            stack_set_name=props['stackset_name'],
            description='StackSet containing baseline configuration for accounts in AWS Organization.',
            deployment_type=DeploymentType.service_managed(),
            template=StackSetTemplate.from_stack_set_stack(baseline_resources),
            capabilities=[Capability.NAMED_IAM],
            target=props['target'],
            operation_preferences=OperationPreferences(
                region_concurrency_type=RegionConcurrencyType.PARALLEL
            )
        )
