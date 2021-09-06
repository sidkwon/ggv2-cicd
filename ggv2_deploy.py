import boto3
import os
import json

with open('./config.json', 'r') as f:
    configs = json.load(f)

###### Variables
component_name = configs['Component']['ComponentName']
component_version = configs['Component']['ComponentVersion']
deployment_name = configs['Deployment']['DeploymentName']

account_number = boto3.client('sts').get_caller_identity().get('Account')
region_name = boto3.Session().region_name

artifact_root_dir = './artifacts'
recipe_root_dir = './recipes'

bucket_name = 'sinjoonk-demo-bucket'

###### Create Boto3 clients
ggv2_client = boto3.client('greengrassv2')
s3_client = boto3.client('s3')

######  TODO: Upload artifacts to S3
artifact_dir = os.path.join(artifact_root_dir, component_name, component_version)
artifacts = os.listdir(artifact_dir) # list

for artifact in artifacts:
    response = s3_client.upload_file(os.path.join(artifact_dir, artifact),
                                     bucket_name,
                                     os.path.join('artifacts', component_name, component_version, artifact)
                                     )

# TODO: Create component version
recipe_file = os.path.join('recipes', component_name + '-' + component_version + '.json')

with open(recipe_file, 'r') as recipe:
    recipe_bytes = recipe.read().encode()

response = ggv2_client.create_component_version(
    inlineRecipe=recipe_bytes
)

print(response)

# TODO: Get deployment
deployments_response = ggv2_client.list_deployments(
    historyFilter='LATEST_ONLY'
)
# print(deployments_response['deployments'])

for deployment in deployments_response['deployments']:
    if deployment['deploymentName'] == deployment_name:
        target_arn = deployment['targetArn']

        response = ggv2_client.get_deployment(
            deploymentId = deployment['deploymentId']
        )
        
        components = response['components']
        components[component_name]['componentVersion'] = component_version
        deploymentPolicies = response['deploymentPolicies']
        iotJobConfiguration = response['iotJobConfiguration']
        
        response = ggv2_client.create_deployment(
            deploymentName = deployment_name,
            targetArn = target_arn,
            components = components,
            deploymentPolicies = deploymentPolicies,
            iotJobConfiguration = iotJobConfiguration
        )
        
        print(response)