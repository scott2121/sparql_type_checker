def extract_triples(node):
    """
    Extract triples from SPARQL query
    q = prepareQuery(sparql_text)
    triples = extract_triples(q.algebra)

    Args:
        nodes : q.algebra
    Returns:
        list of triples
    """
    triples = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "triples":
                triples.extend(value)
            else:
                triples.extend(extract_triples(value))
    elif isinstance(node, list):
        for item in node:
            triples.extend(extract_triples(item))
    return triples


# クエリ内の変数を抽出
def extract_variables_from_query(query):
    """Extract varibles like ?Protein

    Args:
        nodes : q.algebra

    Returns:
        some list of varibles
    """
    # Projection variables
    projected_vars = {str(var) for var in query.algebra["PV"]}

    # Internal variables in query body
    internal_vars = {str(var) for var in query.algebra["_vars"]}

    # Combine both sets
    all_vars = projected_vars.union(internal_vars)

    return all_vars, projected_vars, internal_vars
