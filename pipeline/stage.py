import aws_cdk as cdk
from cdk_stacksets import StackSetTarget
from constructs import Construct

from baseline.stackset import BaselineStackSet


class BaselinePipelineStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        BaselineStackSet(
            self,
            'BaselineStackSetStack',
            props={
                'stackset_name': props['stackset_name'],
                'target': StackSetTarget.from_organizational_units(
                    regions=props['regions'],
                    organizational_units=props['organizational_units']
                )
            }
        )
