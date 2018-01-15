from tkinter import *
from os import path

root = None
csv_file_path = None

credentials_division = None
marks_division = None

credentials_fields = ['uid', 'name', 'grade', 'section']

exams_all = ['FA1', 'FA2', 'SA1', 'FA3', 'FA4', 'SA2']
exams = ['FA1', 'FA2', 'SA1', 'FA3', 'FA4', 'SA2']
subjects = ['subj_' + str(i) for i in range(1, 7)]
tests = ['_ppt', '_activity']
marks_fields = [subjects[i // 2] + tests[i % 2] for i in range(len(subjects) * 2)]

uid = None
curr_exam = 0
credentials_list = [credentials_fields]
marks_list = {'eid': marks_fields}


def main():
    render_application()


# ----- FORM RENDERING -----


def render_application():
    global root

    root = Tk()
    root.winfo_toplevel().title("SPM CSV Data Input GUI")
    render_form_file_path()
    root.mainloop()


def render_form_file_path():
    global root

    division = create_new_division(root)
    section = create_new_section(division)
    render_heading(section, 'File Path')
    status_label = render_status_label(section)
    entries = list()
    entries.append(render_entries_row(section, ['File Path']))
    entries.append(render_entries_row(section, ['Exam']))
    render_buttons_row(section, ['Submit'], [validate_file_path], entries, status_label)
    attach_return_event(validate_file_path, entries, status_label)
    entry_set_focus(entries, status_label)


def render_form_credentials(entries_values):
    global root, credentials_division, credentials_list

    if credentials_division:
        credentials_division.destroy()

    credentials_division = create_new_division(root)
    section = create_new_section(credentials_division)
    render_heading(section, 'Credentials')
    status_label = render_status_label(section)
    entries = []
    entries_text = ['Name', 'Grade', 'Section']
    for entry_text in entries_text:
        entries.append(render_entries_row(section, [entry_text]))

    entries_fill(entries, entries_values, status_label)

    buttons_list = ['<', '>', 'Set Marks']
    on_click_list = [prev_stud, next_stud, validate_credentials]

    if uid == 0:
        del buttons_list[0]
        del on_click_list[0]

    if uid == len(credentials_list) - 1 or len(credentials_list) == 0:
        index = buttons_list.index('>')
        del buttons_list[index]
        del on_click_list[index]

    render_buttons_row(section, buttons_list,
                       on_click_list, entries, status_label)
    attach_return_event(validate_credentials, entries, status_label)
    entry_set_focus(entries, status_label)


def render_form_marks(exam_no, entries_values):
    global root, marks_division, exams

    if marks_division:
        marks_division.destroy()

    marks_division = create_new_division(root)
    section = create_new_section(marks_division)
    render_heading(section, 'Marks')
    render_title(section, exams[exam_no - 1] + ' Marks')
    status_label = render_status_label(section)
    entries = []
    entries_text = ['I Language', 'II Language', 'III Language', 'Maths', 'Science', 'Social']
    for entry_text in entries_text:
        entries.append(render_entries_row(section, [entry_text + ' PPT', entry_text + ' Activity'], 18))

    entries_fill(entries, entries_values, status_label)

    render_buttons_row(section, ['Save Marks'],
                       [next_exam], entries, status_label)
    attach_return_event(next_exam, entries, status_label)
    entry_set_focus(entries, status_label)


# ----- FORM ELEMENTS RENDERING -----


def render_heading(section, text):
    row = create_new_row(section)
    heading = Label(row, text=text, font=('arial', 18),  anchor=CENTER)

    heading.pack()


def render_title(section, text):
    row = create_new_row(section)
    heading = Label(row, text=text, font=('arial', 14), anchor=CENTER)

    heading.pack()


def render_entries_row(section, text_list, width=9):
    entries = []

    row = create_new_row(section)
    for text in text_list:
        text += ': '
        label = Label(row, width=width, text=text, anchor=W)
        label.pack(side=LEFT, padx=5)

        entry = Entry(row)
        entry.pack(side=LEFT, expand=YES, fill=X, padx=5)
        entries.append(entry)

    return entries


def render_buttons_row(section, text_list, on_click_list, entries, status_label):
    row = create_new_row(section)
    for i in range(len(text_list)):
        render_button(row, text_list[i], on_click_list[i], entries, status_label)


def render_button(row, text, on_click, entries, status_label):
    button = Button(row, width=10, text=text, font=('arial', 10),
                    command=(lambda: on_click(entries, status_label)))
    button.pack(side=LEFT, padx=5)
    return button


def render_status_label(section):
    row = create_new_row(section)
    label = Label(row, anchor=W)
    label.pack_forget()
    return label


def create_new_row(section):
    row = Frame(section)
    row.pack(side=TOP, fill=X, pady=5)
    return row


def create_new_division(top):
    division = Frame(top)
    division.pack(side=LEFT, fill=Y)
    return division


def create_new_section(division):
    section = Frame(division)
    section.pack(side=TOP, fill=X, padx=5, pady=5)
    return section


# ----- FORM FUNCTIONS -----


def attach_return_event(on_click, entries, status_label):
    global root
    root.bind('<Return>', (lambda event: on_click(entries, status_label)))


def entry_set_focus(entries, status_label):
    try:
        entries[0].focus()
    except AttributeError:
        entries[0][0].focus()
    except Exception as e:
        display_status(status_label, e.__str__(), error=True)


def save_entries_input(entries, db, status_label):
    global credentials_list, marks_list, uid, curr_exam

    entries_values = entries_get_value(entries, status_label)

    if db == 'credentials':
        try:
            credentials_list[uid + 1] = [str(uid)] + entries_values
        except IndexError:
            credentials_list.append(([str(uid)] + entries_values))
    elif db == 'marks':
        try:
            marks_list[str(curr_exam) + str(uid).zfill(4)] = entries_values
        except IndexError:
            marks_list.update({str(curr_exam) + str(uid).zfill(4): entries_values})


def display_status(status_label, text, error=False):
    status_label.pack(side=LEFT)
    if error:
        status_label['text'] = 'Invalid Input: ' + text
    else:
        status_label['text'] = text


def entries_get_value(entries, status_label):
    try:
        return [entry.get() for entry in entries]
    except AttributeError:
        return [entry.get() for entry_row in entries for entry in entry_row]
    except Exception as e:
        display_status(status_label, e.__str__(), error=True)


def entries_fill(entries, values, status_label):
    try:
        for i in range(len(entries)):
            entries[i].delete(0, END)
            entries[i].insert(0, values[i])
    except AttributeError:
        for j in range(len(entries)):
            for i in range(len(entries[j])):
                entries[j][i].delete(0, END)
                entries[j][i].insert(0, values[j + i])
    except Exception as e:
        display_status(status_label, e.__str__(), error=True)


# ----- APPLICATION FUNCTIONS -----


def csv_read(file):
    lines = [line.rstrip() for line in file.readlines()]
    return [line.split(',') for line in lines]


def csv_open(file_path, status_label):
    global credentials_list, marks_list, uid

    try:
        with open(file_path + 'credentials.csv', 'r') as file:
            credentials_list = csv_read(file)

        with open(file_path + 'marks.csv', 'r') as file:
            marks_list = csv_read(file)
            marks_list = {row[0]: row[1:] for row in marks_list}

        uid = len(credentials_list) - 1
    except Exception as e:
        display_status(status_label, e.__str__(), error=True)


def csv_create(file_path, status_label):
    global credentials_list, marks_list, uid

    try:
        open(file_path + 'credentials.csv', 'x').close()
        open(file_path + 'marks.csv', 'x').close()
        uid = 0
    except Exception as e:
        display_status(status_label, e.__str__(), error=True)


def write_to_file():
    global csv_file_path, credentials_list, marks_list

    with open(csv_file_path + 'credentials.csv', 'w') as file:
        for row in credentials_list:
            file.write(','.join(row) + '\n')

    with open(csv_file_path + 'marks.csv', 'w') as file:
        for key, value in marks_list.items():
            file.write(str(key) + ',' + ','.join(value) + '\n')


def get_where(db, condition):
    if db == 'credentials':
        for row in credentials_list:
            if row[0] == condition:
                return row[1:]
    elif db == 'marks':
        try:
            return marks_list[condition]
        except KeyError:
            pass


def set_stud(uid_l):
    global uid, credentials_fields

    uid = uid_l

    entries_values = get_where('credentials', str(uid))

    if not entries_values:
        entries_values = [''] * (len(credentials_fields))

    render_form_credentials(entries_values)


def set_exam():
    global curr_exam, subjects, uid, marks_list, marks_fields

    entries_values = get_where('marks', str(curr_exam) + str(uid).zfill(4))

    if not entries_values:
        entries_values = [''] * (len(marks_fields))

    render_form_marks(0, entries_values)


# ----- ON CLICK FUNCTIONS -----


def validate_file_path(entries, status_label):
    global csv_file_path, exams_all, exams, curr_exam, marks_division, credentials_division

    if marks_division:
        marks_division.destroy()

    if credentials_division:
        credentials_division.destroy()

    values = entries_get_value(entries, status_label)
    file_path = values[0]
    exam = str(values[1]).upper()

    if not exam:
        display_status(status_label, 'Must provide current exam', error=True)
        return

    if exam not in exams_all:
        display_status(status_label, 'Exam not in exams list', error=True)
        return
    else:
        exams = [exam]
        curr_exam = exams_all.index(exam) + 1

    if not file_path:
        display_status(status_label, 'Please input a directory to which you want to save the file', error=True)
        return
    if file_path[-1] != '\\':
        file_path += '\\'
    elif file_path[-2:] == '\\\\':
        file_path = file_path[:-1]

    if not path.isdir(file_path):
        display_status(status_label, 'Invalid Directory Path. Please input valid directory path', error=True)
    elif path.isfile(file_path + 'credentials.csv') and path.isfile(file_path + 'marks.csv'):
        csv_open(file_path, status_label)
        display_status(status_label, 'CSV File Opened')
        csv_file_path = file_path
        set_stud(uid)
    else:
        csv_create(file_path, status_label)
        display_status(status_label, 'CSV File Created')
        csv_file_path = file_path
        set_stud(uid)


def validate_credentials(entries, status_label):

    entries_values = entries_get_value(entries, status_label)

    grade = entries_values[1]
    section = entries_values[2]

    try:
        grade = int(grade)
    except ValueError:
        display_status(status_label, 'Grade must be a positive integer between 1 and 10', error=True)
        return

    if grade > 10 or grade < 1:
        display_status(status_label, 'Grade must be between 1 and 10', error=True)
        return
    elif section.upper() not in ['A', 'B', 'C']:
        display_status(status_label, "Section must be 'A', 'B' or 'C'", error=True)
        return

    save_entries_input(entries, 'credentials', status_label)
    display_status(status_label, 'Credentials Saved')
    set_exam()


def prev_stud(_, __):
    global uid, marks_division

    set_stud(uid - 1)
    if marks_division:
        marks_division.destroy()


def next_stud(_, __):
    global uid, marks_division

    set_stud(uid + 1)
    if marks_division:
        marks_division.destroy()


def next_exam(entries, status_label):
    global curr_exam, marks_division, exams, uid

    save_entries_input(entries, 'marks', status_label)
    write_to_file()
    marks_division.destroy()
    uid += 1
    set_stud(uid)


# ----- QUIT PROTOCOL -----


def quit_application(_, __):
    write_to_file()
    root.quit()
    root.destroy()
    sys.exit(0)


# ----- START PROTOCOL -----


if __name__ == '__main__':
    main()
