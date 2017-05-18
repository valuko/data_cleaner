import csv

columns_file = 'sample_colname.csv'
dataset_file = 'dataset_sample.csv'
output_file = 'output_data.csv'
columns_dict = dict()


def gen_column_names_dict(colnames_file):
    cleaned = dict()
    with open(colnames_file, newline='') as csvfile:
        column_names = csv.reader(csvfile, delimiter=',')
        for row in column_names:
            col = row[0].strip(' \t\n\r')
            cleaned[col] = None
    return cleaned


def read_csv_cols(filename, col_hash):
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        csv_headings = next(csv_reader)
        i = 0
        for heading in csv_headings:
            if heading in col_hash:
                col_hash[heading] = i
            i += 1
    return col_hash


def clean_up_data(filename, cleaned_data):
    response_data = []
    with open(filename, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            sanitized = []
            idx = 0
            for val in row:
                if idx in cleaned_data.values():
                    sanitized.append(val)
                idx += 1
            response_data.append(sanitized)
    return response_data


def write_list_to_file(filename, data_list):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(data_list)

columns_hash = gen_column_names_dict(columns_file)

#print(', '.join(columns_hash))
#exit(1)

cleaned_dict = read_csv_cols(dataset_file, columns_hash)

#for key in cleaned_dict:
#    print (key, cleaned_dict[key])

refined_dict = clean_up_data(dataset_file, cleaned_dict)

#for key in refined_dict:
#    print(key)

write_list_to_file(output_file, refined_dict)
