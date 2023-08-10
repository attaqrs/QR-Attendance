import json

students = []
attendance = set()

def start_session(section):
    global students
    with open('data/students.json', 'r') as f:
        students = json.load(f)[section]

def mark_attendance(srn):
    if not get_name(srn):
        return False
    attendance.add(srn)
    return 'Attendance marked successfully'

def end_session():
    with open('data/attendance.json', 'w') as f:
        json.dump(list(attendance), f)

def get_name(srn):
    for student in students:
        if student[0] == srn:
            return student[1]
    return False

def get_cur_attendance():
    atts = ''
    for srn in attendance:
        atts += srn + '  ' + get_name(srn) + ';'
    return atts
