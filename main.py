from nav_parser import Parser


def main():
    parser = Parser()

    navmeshs = {}
    for map_name in parser.raw_files.keys():
        navmeshs[map_name] = parser.parse(map_name)

    return navmeshs


if __name__ == '__main__':
    main()
