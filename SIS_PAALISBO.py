from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.simpledialog import askstring
import csv
import os

#main window
root = Tk()
root.geometry("1750x600")
root.title("Student Information System")

#student table(table to display student info)
student_table = ttk.Treeview(root , columns = ("column1", "column2", "column3", "column4", "column5", "column6"), show = "headings", selectmode = "browse")
student_table.column("column2", width=200)  
student_table.column("column3", width=100)

#course table(table to display courses)
course_table = ttk.Treeview(root, columns = "column1", show = "headings")

#CSV file
my_csv = "D:/student.csv"
course_code_csv = "D:/course_code.csv"
try:
    with open(my_csv, 'r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader, None)
except FileNotFoundError:
    pass

def create_csv():
    headers = ['ID_Number', 'Name', 'Year_Level', 'Gender', 'Course_Code']
    # make sure the csv and its headers exist, if not create one
    if not os.path.exists(my_csv):
        with open(my_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
    try:  # put csv file into a list of row
        with open(my_csv, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
    except csv.Error as e:
        print("Error reading CSV file:", e)
        return headers, []
    if not rows:
        return headers, []
    else:
        return headers, rows[1:]
        
def create_course_csv():
    if not os.path.exists(course_code_csv):
        with open(course_code_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Course Code", "Course Name"])  # Include both headers

    try:
        with open(course_code_csv, 'r', newline='') as file:
            reader = csv.reader(file)
            # skip reading the row of headers
            next(reader)
            for row in reader:
                # Insert each row into the course table
                course_table.insert("", "end", values=(row[1],))
    except Exception as e:
        print("An error occurred while reading course data:", e)


headers, student_data = create_csv()
# load data if available
if headers and student_data:  # check if both headers and data exist
    for student in student_data:
        student_table.insert("", "end", values=student)

create_course_csv()

#CRUDL
def addStudent():
    # popup window for filling of information
    popup_window = Toplevel(root) 
    popup_window.geometry ("400x250")
    popup_window.title("Student Information")

    # labels and entry bars
    id_label = Label(popup_window, text = "ID_Number:")
    id_label.pack()
    id_entry = Entry(popup_window)
    id_entry.pack()

    name_label = Label(popup_window, text = "Name:")
    name_label.pack()
    name_entry = Entry(popup_window)
    name_entry.pack()

    year_label = Label(popup_window, text = "Year_Level:(1 - 4)")
    year_label.pack()
    year_entry = Entry(popup_window)
    year_entry.pack()

    gender_label = Label(popup_window, text = "Gender: (M or F(etc))")
    gender_label.pack()
    gender_entry = Entry(popup_window)
    gender_entry.pack()

    course_label = Label(popup_window, text = "Course_Code:")
    course_label.pack()
    course_entry = Entry(popup_window)
    course_entry.pack()

    submit_button = Button(popup_window, text="Submit", command=lambda: submitStudent(id_entry.get(), name_entry.get(), year_entry.get(), gender_entry.get(), course_entry.get()))
    submit_button.pack()

    # Wait for the pop-up window to close
    popup_window.mainloop()

def updateStudent(ID_Number):
    # find the id number
    for row_id in student_table.get_children():
        if student_table.item(row_id, 'values')[0] == ID_Number:
            # get the values of the selected row
            selected_values = student_table.item(row_id, 'values')

            # pop-up window for editing
            popup_window = Toplevel(root)
            popup_window.geometry("400x250")
            popup_window.title("Update Student Information")

            id_label = Label(popup_window, text="ID_Number:")
            id_label.grid(row=0, column=0, padx=10, pady=10)
            id_entry = Entry(popup_window)
            id_entry.grid(row=0, column=1, padx=10, pady=10)
            id_entry.insert(0, selected_values[0])  

            name_label = Label(popup_window, text="Name:")
            name_label.grid(row=1, column=0, padx=10, pady=10)
            name_entry = Entry(popup_window)
            name_entry.grid(row=1, column=1, padx=10, pady=10)
            name_entry.insert(0, selected_values[1]) 

            year_label = Label(popup_window, text="Year_Level:")
            year_label.grid(row=2, column=0, padx=10, pady=10)
            year_entry = Entry(popup_window)
            year_entry.grid(row=2, column=1, padx=10, pady=10)
            year_entry.insert(0, selected_values[2])  

            gender_label = Label(popup_window, text="Gender:")
            gender_label.grid(row=3, column=0, padx=10, pady=10)
            gender_entry = Entry(popup_window)
            gender_entry.grid(row=3, column=1, padx=10, pady=10)
            gender_entry.insert(0, selected_values[3])  

            course_label = Label(popup_window, text="Course_Code:")
            course_label.grid(row=4, column=0, padx=10, pady=10)
            course_entry = Entry(popup_window)
            course_entry.grid(row=4, column=1, padx=10, pady=10)
            course_entry.insert(0, selected_values[4])  

            # update the student information
            def submit_update():
                # Get the updated values from the entries
                updated_id = id_entry.get().strip()
                updated_name = name_entry.get().strip()
                updated_year = year_entry.get().strip()
                updated_gender = gender_entry.get().strip().upper()
                updated_course_code = course_entry.get().strip().upper()

                # check if the new ID number already exists 
                if updated_id != ID_Number:  # check if the ID number has been changed
                    for row_id_check in student_table.get_children():
                        if student_table.item(row_id_check, 'values')[0] == updated_id:
                            messagebox.showerror("Error", f"ID number '{updated_id}' already exists.")
                            return

                # check if the course code exists in the course CSV file
                course_exists = False
                with open(course_code_csv, 'r', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0].strip().upper() == updated_course_code:
                            course_exists = True
                            break

                # update the status of the student
                if course_exists:
                    updated_status = "ENROLLED"
                    status_color = "black"
                else:
                    updated_status = "NOT ENROLLED"
                    status_color = "red"

                # update the student information
                updated_info = (
                    updated_id,
                    updated_name,
                    updated_year,
                    updated_gender,
                    updated_course_code,
                    updated_status
                )
                student_table.item(row_id, values=updated_info)
                save_to_csv()
                popup_window.destroy()

            # add a button to submit the update
            submit_button = Button(popup_window, text="Submit Update", command=submit_update)
            submit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

            return

    # if id number doesn't exist , display error message
    messagebox.showerror("Error", f"Student with ID_Number {ID_Number} not found")




def search():
    search_text = search_entry.get().strip().lower()
    
    # clear
    student_table.selection_remove(student_table.selection())
    course_table.selection_remove(course_table.selection())
    
    if search_text:
        # search in student table
        for row_id in student_table.get_children():
            values = student_table.item(row_id, 'values')
            if search_text in str(values).lower():
                student_table.selection_add(row_id)
        
        # search in course table
        for row_id in course_table.get_children():
            values = course_table.item(row_id, 'values')
            if search_text in str(values).lower():
                course_table.selection_add(row_id)

#this function is going to be used for our updatestudent function
def findIDNumber():
     # ask for id number
    ID_Number = askstring("Enter ID Number", "Please enter the ID Number of the student you want to edit:")
    
    # if the user cancels or inputs nothing, return
    if ID_Number is None or ID_Number.strip() == "":
        return
    
    # find the row with the id number
    found = False
    for row_id in student_table.get_children():
        values = student_table.item(row_id, 'values')
        if values[0] == ID_Number:
            found = True
            break
    
    # If the id number doesn't exist , display error message
    if not found:
        messagebox.showerror("Error", f"Student with ID_Number {ID_Number} not found")
        return
    
    # edit that student's info
    updateStudent(ID_Number)

def deleteStudent():
    # choose the row to be deleted
    rows_selected = student_table.selection()

    # display error if there's no row selected
    if not rows_selected:
        messagebox.showerror("Error", "Please select a row to be deleted")
        return

    confirm_deletion = messagebox.askyesno("Confirm", "Are you sure you want to delete the selected row(s)?")

    # if yes, delete from table and from CSV
    if confirm_deletion:
        for row in rows_selected:
            # delete from the table
            student_table.delete(row)

        # save the remaining data to the CSV file
        save_to_csv()

        messagebox.showinfo("Success", "Selected row(s) deleted successfully")



def save_to_csv():
    # get all the data from the table
    all_rows = student_table.get_children()
    with open(my_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        # write headers
        writer.writerow(["ID_Number", "Name", "Year_Level", "Gender", "Course_Code"])
        # write each row of data
        for row in all_rows:
            values = student_table.item(row, 'values')
            writer.writerow(values)


def submitStudent(id_number, name, year, gender, course):
    id_number = id_number.strip()
    name = name.strip().title()
    year = year.strip()
    gender = gender.strip().upper()
    course = course.strip().upper()

    # check if the ID number already exists
    for row_id in student_table.get_children():
        if student_table.item(row_id, 'values')[0] == id_number:
            messagebox.showerror("Error", f"ID number '{id_number}' already exists.")
            return

    # check if the course exists in the course CSV file
    course_exists = False
    with open(course_code_csv, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].strip().upper() == course:
                course_exists = True
                break

    # update the status of the student
    if course_exists:
        status = "ENROLLED"
        status_color = "black"
    else:
        status = "NOT ENROLLED"
        status_color = "red"

    student_info = (id_number, name, year, gender, course, status)
    student_table.insert("", "end", values=student_info, tags="new_row")

    # Apply font color to the status column
    student_table.tag_configure("new_row", font=("David", 10, "normal"), foreground=status_color)
    save_to_csv()



def addCourse():
    #window to ask the user for the course code and name.
    popup_window = Toplevel(root)
    popup_window.geometry("300x150")
    popup_window.title("Add Course")

    course_code_label = Label(popup_window, text="Course Code:")
    course_code_label.grid(row=0, column=0, padx=5, pady=5)
    course_code_entry = Entry(popup_window)
    course_code_entry.grid(row=0, column=1, padx=5, pady=5)

    course_name_label = Label(popup_window, text="Course Name:")
    course_name_label.grid(row=1, column=0, padx=5, pady=5)
    course_name_entry = Entry(popup_window)
    course_name_entry.grid(row=1, column=1, padx=5, pady=5)

    #another function to finalize the submission
    def submit_course():
        course_code = course_code_entry.get().strip().upper()
        course_name = course_name_entry.get().strip()

        course_name_titlecase = course_name.title()

        # check if the course name exists
        for row_id in course_table.get_children():
            if course_table.item(row_id, 'values')[0] == course_name_titlecase:
                messagebox.showerror("Error", f"Course '{course_name_titlecase}' already exists.")
                return

        # check for duplicates of course codes.
        with open(course_code_csv, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].strip().upper() == course_code:
                    messagebox.showerror("Error", f"Course code '{course_code}' already exists for a different course name.")
                    return

        # if the course doesn't already exist, add it to the table and CSV
        if course_code and course_name:
            course_table.insert("", "end", values=(course_name_titlecase,))
            with open(course_code_csv, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([course_code, course_name_titlecase])
            update_status(course_code)
            popup_window.destroy()  
        else:
            messagebox.showerror("Error", "Both Course Code and Course Name are required.")

    submit_button = Button(popup_window, text="Submit", command=submit_course)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)

def update_status(course_code): #update student status in case there's a new course code added
    # loop thru all rows of the table
    for row_id in student_table.get_children():
        values = student_table.item(row_id, 'values')
        # check if the student's course code matches the newly added course code
        if values[4] == course_code:
            # update the status to "ENROLLED"
            student_table.item(row_id, values=(values[0], values[1], values[2], values[3], values[4], "ENROLLED"))
    # save the updated statuses to the CSV file
    save_to_csv()




def deleteCourse():
    # ask user for input
    course_name = simpledialog.askstring("Input", "Enter Course Name to Delete:")
    if course_name:  # check course name
        course_name_lowercase = course_name.lower() # convert to lowercase for comparison later
        # find the course name to be deleted
        for row in course_table.get_children():
            current_course_name = course_table.item(row, "values")[0]
            if current_course_name.lower() == course_name_lowercase:
                course_table.delete(row)
                delete_course_from_csv(course_name)
                messagebox.showinfo("Success", f"Course with name '{course_name}' deleted successfully.")
                return

        messagebox.showerror("Error", f"Course with name '{course_name}' not found.")

def delete_course_from_csv(course_name):
    # read all data from the CSV file
    all_rows = []
    with open(course_code_csv, 'r', newline='') as file:
        reader = csv.reader(file)
        all_rows = list(reader)

    # write data back to the CSV file without the deleted course
    with open(course_code_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in all_rows:
            # Check if the course name matches, and skip it if it does
            if row[1].strip().lower() != course_name.strip().lower():
                writer.writerow(row)
    
    # update the status of students enrolled in the deleted course
    course_code = None
    for row in all_rows:
        if row[1].strip().lower() == course_name.strip().lower():
            course_code = row[0].strip().upper()
            break
    
    if course_code:
        # go thru all the rows
        for row_id in student_table.get_children():
            values = student_table.item(row_id, 'values')
            # check if the student's course code matches the deleted course code
            if values[4] == course_code:
                # update to not enrolled
                student_table.item(row_id, values=(values[0], values[1], values[2], values[3], values[4], "NOT ENROLLED"))
    # save
    save_to_csv()






frame = LabelFrame(root, borderwidth = 1, bg = "#272829", pady = 50)

# create a search bar
search_bar = Frame(frame, bg="#ffffff", padx=10, pady=10)
search_bar.grid(row=6, column=0, sticky="n", pady = (20, 0))

search_label = Label(search_bar, text="Search:", bg="#ffffff")
search_label.grid(row=0, column=0)

search_entry = Entry(search_bar, width=10)
search_entry.grid(row=0, column=1)

search_button = Button(search_bar, text="Search", command=search)
search_button.grid(row=0, column=2)

#buttons
add_student = Button(frame, text = "Add Student", width = 10, command = addStudent, fg = "black", bg= "#FFF6E0", font=("David", 14, "bold"))
update_student = Button(frame, text = "Edit", width = 10, command = lambda: findIDNumber(), fg = "black", bg= "#FFF6E0", font=("David", 14, "bold"))
delete_student = Button(frame, text = "Delete", width = 10, command = deleteStudent, fg = "black", bg= "#FFF6E0", font=("David", 14, "bold"))

add_course = Button(frame, text = "Add Course", width = 10, command = addCourse, fg = "black", bg= "#FFF6E0", font=("David", 14, "bold"))
delete_course =  Button(frame, text = "Delete Course", width = 10, command = deleteCourse, fg = "black", bg= "#FFF6E0", font=("David", 14, "bold"))

#table
style = ttk.Style(root)
style.configure("Treeview.Heading", font=("David", 10, "bold"))

#set column titles
student_table.heading("column1", text = "ID_Number")
student_table.heading("column2", text="Name", anchor = "center")
student_table.heading("column3", text="Year_Level")
student_table.heading("column4", text="Gender")
student_table.heading("column5", text="Course_Code")
student_table.heading("column6", text="Status")
student_table.tag_configure("new_row", font=("David", 10, "bold"))

course_table.heading("column1", text = "Course_Name")

#printing
add_student.grid(row = 0, column = 0, pady = (80, 0))
update_student.grid(row = 1, column = 0 )
delete_student.grid(row = 2, column = 0 )

frame.grid(row = 0, column = 0, rowspan = 1, sticky = "ns")
root.grid_rowconfigure(0, weight=1)


student_table.grid(row = 0, column = 1, columnspan = 1, rowspan = 3,  sticky = "nsew")
#set weight to fill screen
student_table.grid_columnconfigure(1, weight = 1)

course_table.grid(row=0, column=2, columnspan=3, sticky="nsew", padx = (5,0))
# extend to the right
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
add_course.grid(row = 4, column = 0, pady = (20,0))
delete_course.grid(row = 5, column = 0)



root.mainloop()
