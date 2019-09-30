import lkml
import yaml

import os
import json

# Hardcoded paths that should be parameteized later
PATH_TO_DBT_PROJECT = "test_dbt_project"
PATH_TO_LOOKML_PROJECT = "test_lookml_project"
PATH_TO_TARGET_LOOKML_PROJECT = "target"

MANIFEST_FILE = "target/manifest.json"
COMPILATION_MESSAGE = "You may need to run dbt compile first."


def get_manifest(path_to_project):
    """
    Parse the manifest file as this is faster than importing the manifest object
    from dbt.
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
    for fqn, node in manifest["nodes"].items():
        if node["name"] == model_name and node["resource_type"] == "model":
            matching_models.append(node)

    model = matching_models[0]

    try:
        column = model["columns"].get(column_name)
        col_description = column.get("description")
        return col_description
    except:
        return None


# load the manifest.json file -- just do this once
manifest = get_manifest(PATH_TO_DBT_PROJECT)

# For each file in the lookml project
for file_name in os.listdir(PATH_TO_LOOKML_PROJECT):
    path_to_lookml_file = os.path.join(PATH_TO_LOOKML_PROJECT, file_name)

    # load the lookml
    with open(path_to_lookml_file, "r") as file:
        lookml = lkml.load(file)

    # for each view in the lookml
    for view in lookml["views"]:
        view_name = view["name"]

        # for each dimension in the view
        for dimension in view["dimensions"]:
            dimension_name = dimension["name"]
            dimension_description = get_column_description(
                manifest, view_name, dimension_name
            )
            if dimension_description:
                # update the description based on the project's description
                dimension["description"] = dimension_description

    # dump the lmkl to a target directory
    os.makedirs(PATH_TO_TARGET_LOOKML_PROJECT, exist_ok=True)
    target_lookml_file = os.path.join(PATH_TO_TARGET_LOOKML_PROJECT, file_name)
    with open(target_lookml_file, "w+") as file:
        lkml.dump(lookml, file)


# To-do:
# - multiple lkml files
# - parameterize the paths / add a cli
# - Consider what is a reasonable assumption for matching views to models? the view name?
# - error handling for unmatched view
