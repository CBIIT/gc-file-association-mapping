import csv

import yaml

import file_extensions as extensions
from FileMetadata import FileMetadata
#this script generates a YAML file that maps associated files based on their extensions

def generate_mappings():
    input_file = "file.tsv"
    name_col = "file_name"
    id_col = "file_id"
    
    file_map = parse_files(input_file, name_col, id_col)
    mapping = create_mapping(file_map)
    print_to_yaml(mapping)


def parse_files(file, name_col, id_col):
    id_col_index = None
    name_col_index = None
    file_map = {}
    with open(file, encoding='utf-8-sig') as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for i, row in enumerate(rd):
            if i == 0:
                for j, col in enumerate(row):
                    string_col = str(col)
                    if string_col == name_col:
                        name_col_index = j
                        continue
                    if string_col == id_col:
                        id_col_index = j
                        continue
            else:
                if id_col_index is None:
                    raise Exception("ID column not found")
                if name_col_index is None:
                    raise Exception("Name column not found")
                file = FileMetadata(row[name_col_index], row[id_col_index])
                file_map[file.file_name] = file
    return file_map


def create_mapping(file_map):
    mapping = {}
    for name in file_map:
        file = file_map[name]
        associated_file_name = determine_associated_file_name(file)
        if associated_file_name is None:
            continue
        associated_file = file_map.get(associated_file_name)
        if associated_file is None:
            continue
        mapping[file.id] = associated_file.id
    return mapping


def determine_associated_file_name(file):
    ext = file.get_extension()
    if ext == extensions.BAM:
        return file.get_file_basename() + extensions.BAI
    if ext == extensions.CRAM:
        return file.get_file_basename() + extensions.CRAM + extensions.CRAI
    return None


def print_to_yaml(mapping):
    with open('associations.yaml', 'w') as file:
        data = {"file_associations": mapping}
        yaml.dump(data, file)


if __name__ == '__main__':
    generate_mappings()
