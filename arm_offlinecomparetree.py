import json
import os

# Set the paths to the old and new ARM templates
old_template_path = 'old/arm_template.json'
new_template_path = 'new/arm_template.json'

# Load the old and new ARM templates
with open(old_template_path, 'r') as f:
    old_template = json.load(f)

with open(new_template_path, 'r') as f:
    new_template = json.load(f)

# Function to recursively find the top-level dependencies
def find_top_level_dependencies(resource_name, dependencies, top_level_dependencies):
    for dependency in dependencies:
        if dependency not in top_level_dependencies:
            top_level_dependencies.append(dependency)
            if dependency in deleted_objects:
                for dependency_type, dependency_list in deleted_objects[dependency].items():
                    find_top_level_dependencies(dependency, dependency_list, top_level_dependencies)

# Identify the resources that were deleted
deleted_objects = {}
for resource_id in old_template['resources']:
    resource = old_template['resources'][resource_id]
    resource_type = resource['type']
    if resource_type not in ['Microsoft.DataFactory/factories/pipelines', 'Microsoft.DataFactory/factories/datasets', 'Microsoft.DataFactory/factories/linkedServices', 'Microsoft.DataFactory/factories/triggers']:
        continue
    if resource_id not in new_template['resources']:
        # Check if the deleted resource has dependencies
        dependencies = resource.get('dependsOn', [])
        if dependencies:
            # Retrieve the names of top-level dependent resources
            top_level_dependencies = {dependency.split('/')[-1]: {} for dependency in dependencies}
            deleted_objects[resource['name']] = {resource_type: top_level_dependencies}
        else:
            deleted_objects[resource['name']] = {resource_type: {}}

# Find all the top-level dependencies
top_level_dependencies = []
for deleted_object in deleted_objects:
    for resource_type, dependencies in deleted_objects[deleted_object].items():
        find_top_level_dependencies(deleted_object, dependencies, top_level_dependencies)

# Function to recursively print the dependency tree
def print_dependency_tree(dependency_name, dependencies, indent=0):
    print(' ' * indent + '- ' + dependency_name)
    for dependency_type, dependency_list in dependencies.items():
        for dependency in dependency_list:
            print_dependency_tree(dependency, dependencies[dependency_type], indent + 2)

# Print the dependency tree for each top-level dependency
for dependency in top_level_dependencies:
    print_dependency_tree(dependency, deleted_objects[dependency])
