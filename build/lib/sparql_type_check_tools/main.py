import sys

from sparql_type_check_tools.functions.sparql_type_checker import type_check_sparql


def main():
    #sys.stderr = open('/dev/null', 'w')
    if len(sys.argv) < 4 or len(sys.argv) > 6:
        print("Usage: type_check_sparql <database_name> <query> <shex_path> <verbose(option)>")
        sys.exit(1)

    database_name = sys.argv[1]
    query = sys.argv[2]
    shex_path = sys.argv[3]
    verbose = sys.argv[4]

    # ここでtype_check_sparql関数を呼び出します
    result = type_check_sparql(database_name, query, shex_path, verbose)

    print(result)


if __name__ == "__main__":
    main()
