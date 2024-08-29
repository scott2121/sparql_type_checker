import os

from dotenv import load_dotenv
from pyshex import ShExEvaluator
from rdflib import BNode, Literal, URIRef
from rdflib.plugins.sparql import prepareQuery
from rdflib.term import Variable

from .shex_extracter import extract_triples_from_shex
from .sparql_extractor import extract_triples, extract_variables_from_query


def candiate_update(candidates, _candidates, verbose):
    if verbose:
        print("candidates", candidates, "\n_candidates", _candidates)
    if candidates != [-1]:
        # get & of candidates and _candidates
        candidates = list(set(candidates) & set(_candidates))
    else:
        candidates = _candidates

    # print("retuern", candidates)
    return candidates


def find_matching_classes(var, sparql_triples, shex_triples, verbose=False):
    """
    Given a SPARQL variable, find matching classes in the ShEx triples.
    """
    if verbose:
        print("var", var)
    rdflb_var = Variable(var)
    candidate_classes = [-1]

    for sparql_triple in sparql_triples:
        if rdflb_var not in sparql_triple:
            continue

        s, p, o = sparql_triple
        # print("s", s, "p", p, "o", o)

        # Check subject (s) matches
        if s == rdflb_var:
            if isinstance(p, URIRef):
                if verbose:
                    print("Pos 1")
                candidate_classes = candiate_update(
                    candidate_classes,
                    [
                        shex_triple[0]
                        for shex_triple in shex_triples
                        if URIRef(shex_triple[1]) == p
                    ],
                    verbose,
                )
            if isinstance(o, URIRef):
                if verbose:
                    print("Pos 2")
                candidate_classes = candiate_update(
                    candidate_classes,
                    [
                        shex_triple[0]
                        for shex_triple in shex_triples
                        if URIRef(shex_triple[2]) == o
                    ],
                    verbose,
                )
            if isinstance(o, Literal):
                if verbose:
                    print("Pos 3")
                candidate_classes = candiate_update(
                    candidate_classes,
                    [
                        shex_triple[0]
                        for shex_triple in shex_triples
                        if URIRef(shex_triple[2]) == o.datatype
                    ],
                    verbose,
                )
            if isinstance(o, BNode):
                candidate_classes = candiate_update(
                    candidate_classes,
                    [
                        shex_triple[0]
                        for shex_triple in shex_triples
                        if BNode == type(o)
                    ],
                    verbose,
                )

        # Check object (o) matches
        if o == rdflb_var:
            if isinstance(s, BNode):
                continue
            if isinstance(p, URIRef):
                if verbose:
                    print("Pos 4")
                candidate_classes = candiate_update(
                    candidate_classes,
                    [
                        shex_triple[2]
                        for shex_triple in shex_triples
                        if URIRef(shex_triple[1]) == p
                    ],
                    verbose,
                )
            if isinstance(s, URIRef):
                if verbose:
                    print("Pos 5")
                candidate_classes = candiate_update(
                    candidate_classes,
                    [
                        shex_triple[2]
                        for shex_triple in shex_triples
                        if URIRef(shex_triple[0]) == s
                    ],
                    verbose,
                )
    return candidate_classes


def validate_sparql(variables, sparql_triples, shex_triples, verbose):
    """
    Validate each SPARQL variable against ShEx triples.
    """
    candidate_shex_save = {}

    for var in variables:
        candidate_classes = find_matching_classes(
            var, sparql_triples, shex_triples, verbose
        )
        candidate_shex_save[var] = candidate_classes

        if candidate_classes == []:
            print(
                f"Error: No matching class found for variable {var}. This might indicate an issue with the SPARQL query."
            )

    return candidate_shex_save


def type_check_sparql(database_name, query, path_to_shex, verbose=False):
    """
    Type check a SPARQL query against a ShEx schema.
    """
    with open(path_to_shex, "r") as f:
        shex = f.read()

    shex_fromated = ShExEvaluator(schema=shex)
    # トリプルを抽出
    shex_triples = extract_triples_from_shex(shex_fromated.schema)

    # Extract triples from SPARQL query
    q = prepareQuery(query)
    sparql_triples = extract_triples(q.algebra)

    # Extract variables from SPARQL query
    all_vars, projected_vars, internal_vars = extract_variables_from_query(q)

    # Validate SPARQL query against ShEx schema
    candidate_shex_save = validate_sparql(all_vars, sparql_triples, shex_triples, verbose)

    result = {
        "correct_query": None,
        "error_variables": [],
        "all_vars": all_vars,
    }

    for variable in candidate_shex_save.keys():
        if candidate_shex_save[variable] == []:
            result["error_variables"].append(variable)
            result["correct_query"] = False

    if result["error_variables"] == []:
        result["correct_query"] = True

    return result
