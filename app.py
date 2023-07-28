#!/usr/bin/env python3

import aws_cdk as cdk

from pipeline.pipeline import BaselinePipelineStack

app = cdk.App()

# Required input parameters
context_keys = [
    'codestar_connection_arn',
    'repo_url',
    'repo_branch',
    'sandbox_ou_id',
    'prod_ou_id'
]

parameters = {}

for context_key in context_keys:
    parameters[context_key] = app.node.try_get_context(context_key)

    if parameters[context_key] is None:
        raise ValueError(f'Missing required input parameter: {context_key}')

BaselinePipelineStack(
    app,
    'BaselinePipelineStack',
    props={
        'codestar_connection_arn': parameters['codestar_connection_arn'],
        'repo_url': parameters['repo_url'],
        'repo_branch': parameters['repo_branch'],
        'sandbox_ou_id': parameters['sandbox_ou_id'],
        'prod_ou_id': parameters['prod_ou_id']
    }
)

app.synth()
