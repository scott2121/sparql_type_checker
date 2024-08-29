import sys

from sparql_type_check_tools.functions.sparql_type_checker import type_check_sparql


def main():
    # sys.stderr = open('/dev/null', 'w')
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print(
            "Usage: type_check_sparql <database_name> <query> <shex_path> <verbose(option)>"
        )
        sys.exit(1)

    query = sys.argv[1]
    shex_path = sys.argv[2]
    verbose = sys.argv[3]

    # ここでtype_check_sparql関数を呼び出します
    result = type_check_sparql(query, shex_path, verbose)

    print(result)


if __name__ == "__main__":
    main()
