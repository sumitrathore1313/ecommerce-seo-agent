import os
import openpyxl

def get_files(dir_name):
    # get all files in the directory
    files = os.listdir(dir_name)
    return files

def get_xlsx_data(file_name, skip_header=False):
    # get the data from the xlsx file
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    data = []
    for i, row in enumerate(sheet.rows):
        # Skip the first row (header) if skip_header is True
        if skip_header and i == 0:
            continue
        data.append([cell.value for cell in row])
    return data

def get_xlsx_data_from_dir(dir_name):
    # get the data from the xlsx files in the directory
    files = get_files(dir_name)
    data = []
    is_first_file = True
    
    for file in files:
        if file.endswith('.xlsx'):  # only process xlsx files
            # Don't skip header for first file, skip for rest
            file_data = get_xlsx_data(os.path.join(dir_name, file), skip_header=not is_first_file)
            data.extend(file_data)
            is_first_file = False
    return data


if __name__ == "__main__":
    DIR_LOC = "./data"
    print(get_xlsx_data_from_dir(DIR_LOC))
