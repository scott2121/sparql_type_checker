# My SPARQL Checker

This is a Python package for checking SPARQL queries against ShEx schemas. It provides a command-line tool named `type_check_sparql` to perform the checks.

## Installation

1. First, build the package using `setup.py`:

    ```bash
    python setup.py sdist bdist_wheel
    ```

2. After building, you can install the package locally using:

    ```bash
    pip install .
    ```

## Usage

Once installed, you can use the `type_check_sparql` command to check SPARQL queries. The command requires the following arguments:

- `SELECT * WHERE { ?s ?p ?o }`: The SPARQL query you want to check.
- `path_to_shex/uniprot_rdf-config.shex`: The path to the ShEx schema file.
- `False`: A boolean flag (in this case, "False").

### Example

To execute the command:

```bash
type_check_sparql 'SELECT * WHERE { ?s ?p ?o }' path_to_shex/uniprot_rdf-config.shex False
