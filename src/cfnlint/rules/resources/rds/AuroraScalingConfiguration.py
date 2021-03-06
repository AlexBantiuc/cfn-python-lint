"""
Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""
from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch


class AttributeMismatch(CloudFormationLintRule):
    """ScalingConfiguration only set for Aurora Serverless"""
    id = 'E3028'
    shortdesc = 'ScalingConfiguration only set for Aurora Serverless'
    description = 'You cannot specify ScalingConfiguration for non Aurora Serverless AWS::RDS::DBCluster'
    source_url = 'https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-scalingconfiguration'
    tags = ['resources', 'rds']

    def __init__(self):
        """Init"""
        super(AttributeMismatch, self).__init__()
        self.resource_property_types = ['AWS::RDS::DBCluster']

    def check(self, properties, path, cfn):
        """Check itself"""
        matches = []
        property_sets = cfn.get_object_without_conditions(
            properties, ['EngineMode', 'ScalingConfiguration'])
        for property_set in property_sets:
            properties = property_set.get('Object')
            if properties.get('EngineMode') != 'serverless':
                if properties.get('ScalingConfiguration'):
                    message = 'You cannot specify ScalingConfiguration for non Aurora Serverless AWS::RDS::DBCluster: {}'
                    matches.append(RuleMatch(
                        path,
                        message.format('/'.join(map(str, path)))
                    ))
        return matches

    def match_resource_properties(self, properties, _, path, cfn):
        """Match for sub properties"""
        matches = []
        matches.extend(self.check(properties, path, cfn))
        return matches
