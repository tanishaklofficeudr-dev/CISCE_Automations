import openpyxl


class ExcelReader:
    def __init__(self, file_path):
        self.workbook = openpyxl.load_workbook(file_path)

    def get_sheet_data(self, sheet_name):
        sheet = self.workbook[sheet_name]

        headers = [cell.value for cell in sheet[1]]
        data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = dict(zip(headers, row))
            data.append(row_data)

        return data

    def get_school_ids_to_execute(self):
        master_data = self.get_sheet_data("Master")

        return [
            row["school_id"]
            for row in master_data
            if str(row["execute"]).lower() == "yes"
        ]

    def get_row_by_school_id(self, sheet_name, school_id):
        data = self.get_sheet_data(sheet_name)

        for row in data:
            if row["school_id"] == school_id:
                return row

        return None