import lkml
import yaml

def get_column_description(docs_yaml, model_name, column_name):
    # this gives us back a list
    model_cols = []
    for model in docs_yaml['models']:
        if model['name'] == model_name:
            model_cols.extend(model['columns'])

    col_descriptions = [col.get('description') for col in model_cols if col['name'] == column_name]

    if col_descriptions:
        col_description = col_descriptions[0]
    else:
        col_description = None
    return col_description

# load the lookml into memeory
with open('inputs/orders.lkml', 'r') as file:
    lookml = lkml.load(file)

# lood the yaml into memory
with open('inputs/schema.yml', 'r') as file:
    dbtdocs = yaml.load(file)


for view in lookml['views']:
    view_name = view['name']
    for dimension in view['dimensions']:

        dimension_name = dimension['name']
        dimension_description = get_column_description(dbtdocs, view_name, dimension_name)
        if dimension_description:
            dimension['description'] = dimension_description


with open('target/new_orders.lkml', 'w+') as file:
    lkml.dump(lookml, file)


# how to handle:
# - what's a reasonable assumption for matching views to models? the view name?
# - yaml from multiple files
# - what happens if a model has definitions in multiple places?
