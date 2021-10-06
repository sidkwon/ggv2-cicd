# ggv2-cicd

Greengrass V2 CI/CD samples
- Flow: Github -> Codebuild -> Create ggv2 component version & Create ggv2 deployment
- CodePipeline: sinjoonk-ggv2-basic
- CodeBuild project: sinjoonk-ggv2-basic

## How to deploy new components

### Step1- Modify config.json
    {
        "Component": {
            "ComponentName": "com.annakie.Publisher",
            "ComponentVersion": "1.0.0"
        },
        "Deployment": {
            "DeploymentName": "sinjoonk-ggv2"
        },
        "Bucket": {
            "BucketName": "sinjoonk-demo-bucket"
        }
    }
- ComponentName: ggv2 component name
- ComponentVersion": New component version
- DeploymentName: ggv2 deployment name
- BucketName: S3 bucket that stores artifacts

### Step2 - Local test
Example: `com.annakie.Publisher`, when upgrading ggv2 component version from 1.0.0 to 1.0.1
1. Test new code (e.g., `python publisher.py`)
2. Deploy new local ggv2 component by using 

### Step3 - Deployment from cloud
1. Create new folder under `artifacts/com.annakie.Publisher` (e.g., 1.0.1)
2. Create new python code `publisher.py` in the folder
3. Create new recipe under `recipes` (e.g., `com.annakie.Publisher-1.0.1.json`)
4. Source code commit to Github
5. Monitor CodePipeline/Codebuild