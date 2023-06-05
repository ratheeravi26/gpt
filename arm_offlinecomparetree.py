import json
import re

# Load the old and new ARM templates
with open('old/arm_template.json', 'r') as f:
    old_template = json.load(f)

with open('new/arm_template.json', 'r') as f:
    new_template = json.load(f)

# Identify the resources that were deleted
deleted_objects = {}
for resource in old_template['resources']:
    resource_type = resource['type']
    if resource_type not in ['Microsoft.DataFactory/factories/pipelines', 'Microsoft.DataFactory/factories/datasets', 'Microsoft.DataFactory/factories/linkedServices', 'Microsoft.DataFactory/factories/triggers']:
        continue
    resource_name = resource['name']
    if resource_name not in [r['name'] for r in new_template['resources']]:
        cleaned_resource_name = re.sub(r"[/\'\)\],]+", "", resource_name)
        deleted_objects[cleaned_resource_name] = resource_type

# Function to find the top-level dependencies recursively
def find_top_level_dependencies(resource_name, dependencies):
    top_level_dependencies = []
    for dependency in dependencies:
        if dependency in deleted_objects:
            top_level_dependencies.append(dependency)
            top_level_dependencies.extend(find_top_level_dependencies(dependency, []))
    return top_level_dependencies

# Find all the top-level dependencies for deletion
top_level_dependencies = []
for deleted_object in deleted_objects:
    top_level_dependencies.extend(find_top_level_dependencies(deleted_object, []))

# Print the dependency tree
def print_dependency_tree(dependency_name, indent=0):
    print(' ' * indent + '- ' + dependency_name)
    if dependency_name in deleted_objects:
        for dependency in top_level_dependencies:
            if dependency != dependency_name and dependency in deleted_objects[dependency_name]:
                print_dependency_tree(dependency, indent + 2)

# Print the top-level dependencies for deletion
for dependency in top_level_dependencies:
    print_dependency_tree(dependency)
