
import aws_cdk as cdk
from aws_cdk import Aws, aws_iam as iam
from cdk_stacksets import StackSetStack
from constructs import Construct

from common.cfn_helpers import apply_condition


class BaselineResources(StackSetStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Standard Engineer policy
        standard_eng_policy = iam.ManagedPolicy(
            self,
            "StandardEngineerPolicy",
            managed_policy_name='StandardEngineerPolicy',
            description="A standardized managed policy for engineers in the organization.",
            path="/engineer/",
            statements=[
                iam.PolicyStatement(
                    sid="AllowReadEcs",
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "ecs:Get",
                        "ecs:List",
                        "ecs:Describe"
                    ],
                    resources=[f"arn:{Aws.PARTITION}:ecs:{Aws.REGION}:{Aws.ACCOUNT_ID}"]
                )
            ]
        )

        # Elevated Engineer policy
        elevated_eng_policy = iam.ManagedPolicy(
            self,
            "ElevatedEngineerPolicy",
            managed_policy_name='ElevatedEngineerPolicy',
            description="A standardized elevated managed policy for engineers in the organization.",
            path="/engineer/",
            statements=[
                iam.PolicyStatement(
                    sid="AllowReadWriteEcs",
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "ecs:*"
                    ],
                    resources=[f"arn:{Aws.PARTITION}:ecs:{Aws.REGION}:{Aws.ACCOUNT_ID}"]
                )
            ],
        )

        # Global resources such as IAM Roles or Policies should be only deployed once
        is_ireland_region = cdk.CfnCondition(
            self,
            "isIrelandRegion",
            expression=cdk.Fn.condition_equals("eu-west-1", Aws.REGION)
        )

        apply_condition(standard_eng_policy, is_ireland_region)
        apply_condition(elevated_eng_policy, is_ireland_region)
