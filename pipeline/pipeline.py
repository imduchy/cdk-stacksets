import aws_cdk as cdk
from aws_cdk import pipelines
from constructs import Construct

from pipeline.stage import BaselinePipelineStage


class BaselinePipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline_input = pipelines.CodePipelineSource.connection(
            repo_string=props['repo_url'],
            branch=props['repo_branch'],
            connection_arn=props['codestar_connection_arn']
        )

        synth_action = pipelines.ShellStep(
            'Synth',
            input=pipeline_input,
            commands=[
                f'pip install -r requirements.txt',
                f'npm install -g aws-cdk',
                f'cdk synth'
                f' -c codestar_connection_arn={props["codestar_connection_arn"]}'
                f' -c repo_url={props["repo_url"]}'
                f' -c repo_branch={props["repo_branch"]}'
                f' -c sandbox_ou_id={props["sandbox_ou_id"]}'
                f' -c prod_ou_id={props["prod_ou_id"]}'
            ]
        )

        pipeline = pipelines.CodePipeline(
            self,
            'BaselinePipelineStack',
            synth=synth_action,
            self_mutation=True
        )

        deployment_regions = ['eu-west-1', 'eu-central-1']

        # Before deploying to production OU, first deploy changes to the test OU
        pipeline.add_stage(
            BaselinePipelineStage(
                self,
                'BaselinePipelineStageTest',
                props={
                    'stackset_name': 'BaselineStackSetTestEnvironment',
                    'regions': deployment_regions,
                    'organizational_units': [props['sandbox_ou_id']],
                }
            )
        )

        pipeline.add_stage(
            BaselinePipelineStage(
                self,
                'BaselinePipelineStageProd',
                props={
                    'stackset_name': 'BaselineStackSetProdEnvironment',
                    'regions': deployment_regions,
                    'organizational_units': [props['prod_ou_id']],
                }
            )
        )
