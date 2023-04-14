import os
import json
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# set up Azure credentials
tenant_id = os.environ['tenant_id']
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
subscription_id = os.environ['subscription_id']
credentials = ServicePrincipalCredentials(
    client_id=client_id,
    secret=client_secret,
    tenant=tenant_id
)

# set up Azure DevOps connection
organization_url = os.environ['organization_url']
project_name = os.environ['project_name']
personal_access_token = os.environ['personal_access_token']
connection = Connection(
    base_url=organization_url,
    creds=BasicAuthentication('', personal_access_token)
)
client = connection.clients.get_data_client()

# set up ARM clients
resource_client = ResourceManagementClient(credentials, subscription_id)
adf_client = DataFactoryManagementClient(credentials, subscription_id)

# get old and new template files from Azure Repos Git repository
old_commit_id = os.environ['Build_SourceVersion']
new_commit_id = os.environ['System.PullRequest.SourceCommitId']
repository_id = os.environ['Build_Repository_ID']
repository_project_name = os.environ['Build_Repository_Name']
old_template_file_path = os.environ['old_template_file_path']
new_template_file_path = os.environ['new_template_file_path']
old_template_content = client.get_item_content(repository_id, old_template_file_path, old_commit_id).decode('utf-8')
new_template_content = client.get_item_content(repository_id, new_template_file_path, new_commit_id).decode('utf-8')
old_template = json.loads(old_template_content)
new_template = json.loads(new_template_content)

# compare objects in old and new templates
old_objects = old_template['resources']
new_objects = new_template['resources']

objects_to_delete = []

for old_object in old_objects:
    object_found = False
    for new_object in new_objects:
        if old_object['type'] == new_object['type'] and old_object['name'] == new_object['name']:
            object_found = True
            break
    if not object_found:
        objects_to_delete.append(old_object)

# delete unused objects from ADF
for object_to_delete in objects_to_delete:
    resource_client.resources.delete(
        resource_group_name=os.environ['resource_group_name'],
        resource_provider_namespace='Microsoft.DataFactory',
        parent_resource_path='',
        resource_type='dataFactories',
        resource_name=os.environ['data_factory_name'],
        api_version='2018-06-01',
        parameters={
            'factoryName': os.environ['data_factory_name'],
            'resourceName': object_to_delete['name'],
            'resourceType': object_to_delete['type']
        }
    )

# update pipeline run result in Azure DevOps
pipeline_run_id = int(os.environ['Build_TriggeredBy_BuildId'])
result = {'unused_objects_deleted': len(objects_to_delete)}
client.update_build_properties(
    project=project_name,
    build_id=pipeline_run_id,
    properties=result
)

print('Unused objects deleted from ADF:', len(objects_to_delete))
