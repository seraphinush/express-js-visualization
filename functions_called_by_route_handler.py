import re

reserved = ['forEach', 'then', 'push', 'toJSON', 'log', 'on']


def is_reserved(word):
    word = word.replace('(', '')
    word = word.replace(')', '')
    return word in reserved


def get_sub_handler(found, file_paths, parent_handler):
    functions = {}

    parts = map(str.strip, list(filter(None, [e+';' for e in parent_handler.split(';') if e])))
    parts = [part for part in parts if not part.startswith('res.') and not part.startswith('req.')]

    for part in parts:
        part = '.' + part + ';'
        try:
            function_names = re.findall("\.[^().;]+\(.*\)\s*[.;]", part)

            for function_name in function_names:

                function_name = function_name[1:]

                if function_name.find('(') > 0:
                    function_name = function_name[:function_name.find('(')]

                if function_name in found:
                    break

                if is_reserved(function_name):
                    break

                for file in file_paths:
                    f = open(file, "r")
                    file_text = f.read()

                    if function_name not in file_text:
                        continue

                    if re.search(function_name + '\s*\([^();:\'"]*\)\s*{', file_text):
                        file_text = file_text[file_text.index(function_name):]
                        open_brackets = 0
                        closing_brackets = 0
                        end_index = 0
                        for i in range(0, len(file_text)):
                            char = file_text[i]
                            if char == '{':
                                open_brackets += 1
                            elif char == '}':
                                closing_brackets += 1

                            if open_brackets == closing_brackets and open_brackets != 0:
                                end_index = i + 1
                                break

                        file_text = file_text[:end_index]
                        file_text = file_text[file_text.index('{') + 1: file_text.rindex('}')]
                        found.append(function_name)
                        functions[function_name] = file_text

                        sub_functions = get_sub_handler(found, file_paths, file_text)
                        functions = merge_two_dicts(functions, sub_functions)
        except:
            pass

    return functions


def merge_two_dicts(dict1, dict2):
    merged = dict1.copy()
    merged.update(dict2)
    return merged
