import os
import json
#from azure.common.credentials import ServicePrincipalCredentials
#from azure.mgmt.resource import ResourceManagementClient
##from azure.mgmt.datafactory import DataFactoryManagementClient
#from azure.devops.connection import Connection
#from msrest.authentication import BasicAuthentication

# set up Azure credentials
'''
tenant_id = os.environ['tenant_id']
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
subscription_id = os.environ['subscription_id']
credentials = ServicePrincipalCredentials(
    client_id=client_id,
    secret=client_secret,
    tenant=tenant_id
)
'''

'''
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
'''

# set up template paths
new_template_path = r'C:\Users\Ravi\PycharmProjects\azure\ARMTemplate_old.json'
old_template_path = r'C:\Users\Ravi\PycharmProjects\azure\ARMTemplate_new.json'

# read in template files
with open(old_template_path, 'r') as old_template_file:
    old_template = json.load(old_template_file)

with open(new_template_path, 'r') as new_template_file:
    new_template = json.load(new_template_file)

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
'''
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
'''

print('Unused objects deleted from ADF:', len(objects_to_delete))
