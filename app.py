#!/usr/bin/env python3

import aws_cdk as cdk

from baseline.stackset import BaselineStackSet

app = cdk.App()

# One of the requirements of the cdk_stacksets package is that the
# application is environment agnostic.
BaselineStackSet(app, "OrganizationAccountBaseline")

app.synth()
