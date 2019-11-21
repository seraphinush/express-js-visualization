import main
import re
from collections import defaultdict
import file_finder

regex = {}
# example key value pair
# '/database': ['get', 'post']
endpoints = defaultdict(list)

def get_routes(file_paths):
    build_regex()
    for file_path in file_paths:
        parse_file(file_path)
                
def build_regex():
    app_var = list(main.symbol_table.keys())[list(main.symbol_table.values()).index('express()')]

    regex['app_get'] = re.compile(r'' + re.escape(app_var) + r'\.get\((?:\'|\")(?P<endpoint_get>.+)(?:\'|\"),(.?)')
    regex['app_put'] = re.compile(r'' + re.escape(app_var) + r'\.put\((?:\'|\")(?P<endpoint_put>.+)(?:\'|\"),(.?)')
    regex['app_post'] = re.compile(r'' + re.escape(app_var) + r'\.post\((?:\'|\")(?P<endpoint_post>.+)(?:\'|\"),(.?)')
    regex['app_delete'] = re.compile(r'' + re.escape(app_var) + r'\.delete\((?:\'|\")(?P<endpoint_delete>.+)(?:\'|\"),(.?)')
    regex['app_patch'] = re.compile(r'' + re.escape(app_var) + r'\.patch\((?:\'|\")(?P<endpoint_patch>.+)(?:\'|\"),(.?)')

def parse_line(line):
  for key, rx in regex.items():
    match = rx.search(line)
    if match:
      return key, match
  return None, None

def parse_file(file_path):
  with open(file_path, 'r') as file:
    for line in file:
      
      file_finder.router_files(file, file_path, line)

      key, match = parse_line(line)
      # extract endpoint string and respective HTTP method
      if key == 'app_get':
        endpoints[match.group('endpoint_get')].append('get')
      if key == 'app_put':
        endpoints[match.group('endpoint_put')].append('put')
      if key == 'app_post':
        endpoints[match.group('endpoint_post')].append('post')
      if key == 'app_delete':
        endpoints[match.group('endpoint_delete')].append('delete')
      if key == 'app_patch':
        endpoints[match.group('endpoint_delete')].append('delete')