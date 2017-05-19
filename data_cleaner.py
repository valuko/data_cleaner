import csv

columns_dict = dict()
# Test data
# columns_file = 'sample_colname.csv'
# dataset_file = 'dataset_sample.csv'
# output_file = 'output_data_test.csv'
# categorized_data_file = 'output_data_categorized_test.csv'
# Live data
columns_file = 'column_dataset.csv'
dataset_file = 'epi_r.csv'
output_file = 'output_data.csv'
categorized_data_file = 'categorized_output_data.csv'


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
            cl_heading = heading.strip(' \t\n\r')
            if cl_heading in col_hash:
                col_hash[heading] = i
            i += 1
    return col_hash


def clean_up_data(filename, cleaned_data):
    response_data = []
    with open(filename, encoding="utf8", newline='') as csvfile:
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
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(data_list)


def categorize_data(data_list):
    columns_list = data_list.pop(0)
    response_data = []
    for data in data_list:
        idx = 0
        sanitized = []
        for val in data:
            stripped_val = val.strip(' \t\n\r')
            if idx < 6:
                val = "NA" if stripped_val == "" else stripped_val
                sanitized.append(val)
                idx += 1
                continue

            try:
                float_val = float(stripped_val)
                if float_val > 0.0:
                    cat = float_val if float_val > 1 else columns_list[idx]
                    sanitized.append(cat)
            except ValueError:
                if stripped_val != "":
                    sanitized.append(stripped_val)
            idx += 1
        response_data.append(sanitized)
    #return [columns_list] + response_data
    return response_data

columns_hash = gen_column_names_dict(columns_file)

#print(', '.join(columns_hash))
#exit(1)

cleaned_dict = read_csv_cols(dataset_file, columns_hash)

#for key in cleaned_dict:
#    print (key, cleaned_dict[key])

refined_list = clean_up_data(dataset_file, cleaned_dict)

#for key in refined_list:
#    print(key)

write_list_to_file(output_file, refined_list)

# Categorize the data
data_categorized = categorize_data(refined_list)
#for key in data_categorized:
#    print(key)

write_list_to_file(categorized_data_file, data_categorized)
