import lkml
import yaml

import os
import json

PATH_TO_DBT_PROJECT = "/Users/claire/clrcrl/jaffle_shop"

MANIFEST_FILE = "target/manifest.json"
COMPILATION_MESSAGE = "You may need to run dbt compile first."


def _get_manifest(path_to_project):
    """
    This subcommand uses the manifest file, whereas other subcommands import
    the manifest object from dbt (which requires the project to be parsed).
    Using the manifest file is significantly faster, so is preferred in this
    case.
    """
    manifest_path = os.path.join(path_to_project, MANIFEST_FILE)
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
        return manifest
    except IOError:
        raise Exception(
            "Could not find {} file. {}".format(MANIFEST_FILE, COMPILATION_MESSAGE)
        )

def get_column_description(manifest, model_name, column_name):
    matching_models = []
    for fqn, node in manifest['nodes'].items():
        if node['name'] == model_name and node['resource_type'] == 'model':
            matching_models.append(node)
    import ipdb; ipdb.set_trace()

    model = matching_models[0]

    try:
        column = model['columns'].get(column_name)
        col_description = column.get('description')
        return col_description
    except:
        return None


# load the lookml
with open('test_lookml_project/orders.lkml', 'r') as file:
    lookml = lkml.load(file)

# load the manifest.json file

manifest = _get_manifest(PATH_TO_DBT_PROJECT)

for view in lookml['views']:
    view_name = view['name']
    for dimension in view['dimensions']:

        dimension_name = dimension['name']
        dimension_description = get_column_description(manifest, view_name, dimension_name)
        if dimension_description:
            dimension['description'] = dimension_description


with open('target/new_orders.lkml', 'w+') as file:
    lkml.dump(lookml, file)



# To-do:
# - multiple lkml files
# - parameterize the paths / add a cli
# - Consider what is a reasonable assumption for matching views to models? the view name?
