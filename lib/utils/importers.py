import csv

def fill_from_csv(file_path, to_be_filled, mapper):
    data_list = []
    try:
        with open(file_path) as file_data:
            reader = csv.reader(file_data)
            isHeader = True
            for line in reader:
                if not isHeader:
                    instance = to_be_filled()
                    mapper.map_properties(line, instance)
                    data_list.append(instance)
                isHeader = False

    except FileNotFoundError:
        print(f'File: {file_path} not found!')
    
    return data_list
