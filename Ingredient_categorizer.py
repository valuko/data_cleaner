import csv
import math

ingredients = dict()
# col_num = 2
col_num = 1
cut_off_col = 6
dataset_file = 'test_ingredient_date.csv'
out_data_file = 'new_ingredients.csv'
output_cols = [1, 2, 3, 4, 5, 6]
# output_cols = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700]


def read_csv_data(filename):
    ingredients_dict = dict()
    with open(filename, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            idx = -1
            target_val = -1
            for val in row:
                idx += 1
                if col_num == idx:
                    if val == 'NA':
                        break
                    target_val = int(math.floor(float(val)))
                    # convert to nearest hundred
                    # target_val = int(float(val) / 100.0) * 100
                    continue
                if idx < cut_off_col:
                    continue
                #print('val: ', val)
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
            print(out_list)
            writer.writerow(out_list)


target_results = read_csv_data(dataset_file)

#print(target_results)

write_ingredients_csv(out_data_file, target_results)
