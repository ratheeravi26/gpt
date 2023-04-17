import os
import json
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient

# Set the credentials and subscription ID
tenant_id = os.environ.get('AZURE_TENANT_ID')
client_id = os.environ.get('AZURE_CLIENT_ID')
client_secret = os.environ.get('AZURE_CLIENT_SECRET')
subscription_id = os.environ.get`('AZURE_SUBSCRIPTION_ID')

# Set the resource group name and ADF instance name
resource_group_name = 'my_resource_group'
adf_name = 'my_adf_instance'

# Set the paths to the old and new ARM templates
old_template_path = 'old/arm_template.json'
new_template_path = 'new/arm_template.json'

# Set up the credentials and clients
credentials = ServicePrincipalCredentials(client_id=client_id, secret=client_secret, tenant=tenant_id)
resource_client = ResourceManagementClient(credentials, subscription_id)
adf_client = DataFactoryManagementClient(credentials, subscription_id)

# Get the list of objects in the ADF instance
objects = adf_client.factories.list_objects(resource_group_name, adf_name)

# Load the old and new ARM templates
with open(old_template_path, 'r') as f:
    old_template = json.load(f)

with open(new_template_path, 'r') as f:
    new_template = json.load(f)

# Identify the objects that were deleted
deleted_objects = []
for obj in objects:
    obj_id = obj.id
    obj_name = obj.name
    obj_type = obj.type
    if obj_type not in ['datasets', 'linkedServices', 'pipelines']:
        continue
    if obj_id not in new_template['resources']:
        deleted_objects.append(obj_name)

# Print the list of deleted objects
print(f"The following objects were deleted: {deleted_objects}")
