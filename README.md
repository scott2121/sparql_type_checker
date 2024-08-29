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
```

In python:

```Python
from sparql_type_check_tools import type_check_sparql

import sys

# Suppress error output for clarity
sys.stderr = open('/dev/null', 'w')

# Example of an invalid SPARQL query
test_query_false = """
PREFIX core: <http://purl.uniprot.org/core/>
PREFIX chembl: <http://rdf.ebi.ac.uk/terms/chembl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?uniprot_pdb 
WHERE {
    VALUES ?UniProt__class { core:Protein chembl:UniprotRef }
    ?UniProt a ?UniProt__class ;
        rdfs:seeAlsooooooooo 1 .
    ?uniprot_pdb a core:Structure_Resource .
    ?uniprot_pdb ?x ?y.
}
LIMIT 100
"""

# Example of a valid SPARQL query
test_query_true = """
PREFIX core: <http://purl.uniprot.org/core/>
PREFIX chembl: <http://rdf.ebi.ac.uk/terms/chembl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?uniprot_orf_name ?uniprot_gene_name
WHERE {
    VALUES ?uniprot_gene_name { "ACE2" }
    VALUES ?UniProt__class { core:Protein chembl:UniprotRef }
    ?UniProt a ?UniProt__class ;
        core:encodedBy / core:orfName ?uniprot_orf_name ;
        core:encodedBy / skos:prefLabel ?uniprot_gene_name .
}
LIMIT 100
"""

# Path to the ShEx schema
path_to_shex = "path_to_your/uniprot_rdf-config.shex"

# Running the false query test
result = type_check_sparql(test_query_false, path_to_shex, False)
print("test_query_false:\n", result)
print("----------" * 10)

# Running the true query test
result = type_check_sparql(test_query_true, path_to_shex, False)
print("test_query_true:\n", result)
```