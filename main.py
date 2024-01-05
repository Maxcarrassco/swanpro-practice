import openpyxl


wb = openpyxl.load_workbook("grades.xlsx")
ws = wb.active 

data = ws.iter_rows(values_only=True)
field = str(data.__next__()[0]).replace(")", "").split("(")
subject = field[0]
className = field[1]
students = []

for row in data:
    if row[0] == None or str(row[0]).strip() == "Name":
        continue
    student = {}
    student["name"] = row[0]
    student["email"] = row[1]
    student["gender"] = row[2]
    student["age"] = row[3]
    student["grade"] = row[4]
    students.append(student)
