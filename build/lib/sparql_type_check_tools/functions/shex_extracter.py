import re

from rdflib import BNode, URIRef


def extract_triples_from_shex(shex_text):
    """Extract triples from ShEx schema
    shex = ShExEvaluator(schema=ShEx_uniprot)
    # トリプルを抽出
    shex_triples = extract_triples_from_shex(shex.schema)

    Args:
        shex_text : shex.schema

    Returns:
        list of triples
    """
    triples = []
    # シェイプごとに分割
    shapes = re.split(r"<([^>]+)> {", shex_text)

    for i in range(1, len(shapes), 2):
        shape_name = f"<{shapes[i]}>"
        shape_body = shapes[i + 1].strip().rstrip("}")

        # 述語と目的語のペアを抽出
        pairs = re.findall(
            r"<([^>]+)> (\[[^]]+\]|BNODE|IRI|@<[^>]+>|<[^>]+>)", shape_body
        )

        for pred, obj in pairs:
            # BNODE, IRI, リテラルを適切に処理
            if obj == "BNODE":
                obj = BNode()
            elif obj == "IRI":
                obj = URIRef("IRI")
            elif obj.startswith("[") and obj.endswith("]"):
                obj = URIRef(obj[2:-2])
            elif obj.startswith("@<") and obj.endswith(">"):
                obj = URIRef(obj[1:])
            else:
                obj = URIRef(obj[1:-1])

            triples.append((URIRef(shape_name), URIRef(pred), obj))

    return triples
