# ***Archival Notice***
This repository has been archived.

As a result all of its historical issues and PRs have been closed.

Please *do not clone* this repo without understanding the risk in doing so:
- It may have unaddressed security vulnerabilities
- It may have unaddressed bugs

<details>
   <summary>Click for historical readme</summary>

# [WIP] dbtdocs-to-lookml
A tool to persist descriptions from your dbt project your lookml project.

## Running this proof of concept locally:
1. `cd` into the `test_dbt_project` directory
2. Run `dbt compile`. Note, you may need to set up a new dbt target to compile
this correctly.
3. `cd` back into main directory
4. Run `python dbtdocs_to_lookml.py`
5. Check the `target` directory: you should have new lookml files with dbt
descriptions

## To-dos:
For beta release:
- [ ] Make this handle multiple lookml files
- [ ] Parameterize the paths / add a CLI
- [ ] Consider reasonable assumptions around matching a dbt model to a view

Future considerations:
- Should this overwrite files, or just diff them?
- What other command line arguments should it have?
- What about long descriptions?

