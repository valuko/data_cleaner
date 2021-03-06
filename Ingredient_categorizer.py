import csv
import math

ingredients = dict()
mode = 0
test = 0
cut_off_col = 6

if test == 1:
    dataset_file = 'test_ingredient_data.csv'
    out_data_file = 'test_new_ingredients.csv'
else:
    dataset_file = 'raw_ingredients_data.csv'
    out_data_file = 'new_ingredients_data.csv'

if mode == 1:
    col_num = 1
    output_cols = [1, 2, 3, 4, 5]
    out_data_file = "ratings_"+out_data_file
else:
    col_num = 2
    out_data_file = "calories_" + out_data_file
    output_cols = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800,
                   1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]


def read_csv_data(filename, run_mode):
    ingredients_dict = dict()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            idx = -1
            target_val = -1
            for val in row:
                idx += 1
                if col_num == idx:
                    if val == 'NA':
                        break

                    target_val = int(float(val) / 100.0) * 100
                    if run_mode == 1:
                        target_val = int(math.floor(float(val)))
                    continue
                if idx < cut_off_col:
                    continue
                if val == 'NA' or val.strip(' \t\n\r') == "":
                    break
                if not (val in ingredients_dict):
                    ingredients_dict[val] = dict()
                if not (target_val in ingredients_dict[val]):
                    ingredients_dict[val][target_val] = 0
                ingredients_dict[val][target_val] += 1
    return ingredients_dict


def write_ingredients_csv(filename, data):
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['ingredient'] + output_cols)
        for key in data:
            data_rec = data[key]
            out_list = [key]
            for i in output_cols:
                new_val = data_rec[i] if (i in data_rec) else 0
                out_list.append(new_val)
            # print(out_list)
            writer.writerow(out_list)


target_results = read_csv_data(dataset_file, mode)

# print(target_results)

write_ingredients_csv(out_data_file, target_results)
