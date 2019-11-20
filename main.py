import router_finder
import endpoint_finder

symbol_table = dict([('app', 'express()'), ('router', 'express.Router()')])


def main():
    directory = input("Please enter the path to the directory to scan:\n").strip()
    file_paths = router_finder.get_js_files(directory)
    endpoint_finder.get_routes(file_paths)
    print(endpoint_finder.endpoints)


if __name__ == "__main__":
    main()