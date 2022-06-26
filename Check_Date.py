import os

def check(dt):
    lst = os.listdir('Attendance')
    for i in lst:
        date = i.split('_')
        if dt == date[1]:
            return True
    return False

# print(check("2022-06-23"))