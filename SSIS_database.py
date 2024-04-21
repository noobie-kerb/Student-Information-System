from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.simpledialog import askstring
import csv
import os
import sqlite3

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

#Databases

#connect to a database
conn = sqlite3.connect('student.db')

cursor = conn.cursor()

#table
create_student_table = """
        CREATE TABLE IF NOT EXISTS student (
        ID_Number TEXT,
        Name TEXT,
        Year_Level INTEGER,
        Gender TEXT,
        Course_Code TEXT,
        Status TEXT
    )

"""
create_course_table = """
    CREATE TABLE IF NOT EXISTS course (
        Course_Code TEXT,
        Course_Name TEXT
    )

"""

cursor.execute(create_student_table)
cursor.execute(create_course_table)

#commit changes
conn.commit()

#close connection
conn.close()


#CRUDL

def validate_id(input_text):
    # Check if the input matches the format "xxxx-xxxx"
    if len(input_text) == 9 and input_text[4] == '-':
        if input_text[:4].isdigit() and input_text[5:].isdigit():
            return True
    return False

def add_student():
    # Create a popup window for adding a student
    popup_window = Toplevel(root)
    popup_window.geometry("300x250")
    popup_window.title("Add Student")

    # Labels and entry fields for student information
    id_label = Label(popup_window, text="ID Number:")
    id_label.grid(row=0, column=0, padx=5, pady=5)
    id_entry = Entry(popup_window)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    name_label = Label(popup_window, text="Name:")
    name_label.grid(row=1, column=0, padx=5, pady=5)
    name_entry = Entry(popup_window)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    year_label = Label(popup_window, text="Year Level:")
    year_label.grid(row=2, column=0, padx=5, pady=5)
    year_entry = Entry(popup_window)
    year_entry.grid(row=2, column=1, padx=5, pady=5)

    gender_label = Label(popup_window, text="Gender:")
    gender_label.grid(row=3, column=0, padx=5, pady=5)
    gender_entry = Entry(popup_window)
    gender_entry.grid(row=3, column=1, padx=5, pady=5)

    # Fetch course codes from the database
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Course_Code FROM course")
    course_codes = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Dropdown for course selection
    course_code_var = StringVar()
    course_code_var.set(course_codes[0] if course_codes else "NONE")
    course_combobox = ttk.Combobox(popup_window, textvariable=course_code_var, values=course_codes, state="readonly")
    course_combobox.grid(row=4, column=1, padx=5, pady=5)

    # Function to submit the student details
    def submit_student():
        id_number = id_entry.get().strip()
        name = name_entry.get().strip().title()
        year_level = year_entry.get().strip()
        gender = gender_entry.get().strip().title()
        course_code = course_code_var.get()

        # Connect to the database
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()
        if(validate_id(id_number)):
            # Insert the student into the database
            cursor.execute("INSERT INTO student (ID_Number, Name, Year_Level, Gender, Course_Code, Status) VALUES (?, ?, ?, ?, ?, ?)",
                           (id_number, name, year_level, gender, course_code, "ENROLLED" if course_code in course_codes else "NOT ENROLLED"))

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Update the student table GUI
            student_table.insert("", "end", values=(id_number, name, year_level, gender, course_code, "ENROLLED" if course_code in course_codes else "NOT ENROLLED"))

            # Close the popup window
            popup_window.destroy()

            messagebox.showinfo("Success", "Student added successfully.")
        else:
            messagebox.showerror("ERROR", "Please follow ID_Number format")

    # Button to submit the student details
    submit_button = Button(popup_window, text="Submit", command=submit_student)
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Keep the popup window running
    popup_window.mainloop()

def edit_student():
    # Get the selected student's ID
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a student to edit.")
        return

    student_id = student_table.item(selected_item, "values")[0]

    # Fetch the current information of the selected student from the database
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE ID_Number=?", (student_id,))
    student_data = cursor.fetchone()
    conn.close()

    if not student_data:
        messagebox.showerror("Error", "Student data not found.")
        return

    # Create a popup window for editing student information
    popup_window = Toplevel(root)
    popup_window.geometry("300x250")
    popup_window.title("Edit Student")

    # Labels and entry fields for student information
    id_label = Label(popup_window, text="ID Number:")
    id_label.grid(row=0, column=0, padx=5, pady=5)
    id_entry = Entry(popup_window)
    id_entry.grid(row=0, column=1, padx=5, pady=5)
    id_entry.insert(0, student_data[0])

    name_label = Label(popup_window, text="Name:")
    name_label.grid(row=1, column=0, padx=5, pady=5)
    name_entry = Entry(popup_window)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    name_entry.insert(0, student_data[1])

    year_label = Label(popup_window, text="Year Level:")
    year_label.grid(row=2, column=0, padx=5, pady=5)
    year_entry = Entry(popup_window)
    year_entry.grid(row=2, column=1, padx=5, pady=5)
    year_entry.insert(0, student_data[2])

    gender_label = Label(popup_window, text="Gender:")
    gender_label.grid(row=3, column=0, padx=5, pady=5)
    gender_entry = Entry(popup_window)
    gender_entry.grid(row=3, column=1, padx=5, pady=5)
    gender_entry.insert(0, student_data[3])

    # Fetch course codes from the database
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Course_Code FROM course")
    course_codes = [row[0] for row in cursor.fetchall()]
    conn.close()

    course_label = Label(popup_window, text="Course Code:")
    course_label.grid(row=4, column=0, padx=5, pady=5)
    course_code_var = StringVar()
    course_dropdown = ttk.Combobox(popup_window, textvariable=course_code_var, values=course_codes, state="readonly")
    course_dropdown.grid(row=4, column=1, padx=5, pady=5)
    course_dropdown.set(student_data[4])

    # Function to update the student information
    def update_student():
        new_id = id_entry.get().strip()  # Modified to get the new ID number
        new_name = name_entry.get().strip().title()
        new_year = year_entry.get().strip()
        new_gender = gender_entry.get().strip().title()
        new_course_code = course_code_var.get().strip().upper()

        # Check if all fields are provided
        if new_id and new_name and new_year and new_gender and new_course_code:
            # Connect to the database
            conn = sqlite3.connect('student.db')
            cursor = conn.cursor()

            # Check if the new ID number already exists in the database
            cursor.execute("SELECT COUNT(*) FROM student WHERE ID_Number=?", (new_id,))
            existing_id = cursor.fetchone()[0]

            if existing_id > 0 and new_id != student_id:  # Check if the ID is not the current student's ID
                messagebox.showerror("Error", f"ID number '{new_id}' already exists.")
            else:
                # Check if the course exists in the course table
                cursor.execute("SELECT COUNT(*) FROM course WHERE Course_Code=?", (new_course_code,))
                existing_course = cursor.fetchone()[0]

                if existing_course > 0:
                    status = "ENROLLED"
                else:
                    status = "NOT ENROLLED"

                # Update the student information in the database
                cursor.execute("UPDATE student SET ID_Number=?, Name=?, Year_Level=?, Gender=?, Course_Code=?, Status=? WHERE ID_Number=?",
                               (new_id, new_name, new_year, new_gender, new_course_code, status, student_id))
                conn.commit()
                conn.close()

                # Update the displayed student information in the GUI
                student_table.item(selected_item, values=(new_id, new_name, new_year, new_gender, new_course_code, status))
                popup_window.destroy()

                messagebox.showinfo("Success", "Student information updated successfully.")
        else:
            messagebox.showerror("Error", "All fields are required.")



    # Button to update student information
    update_button = Button(popup_window, text="Update", command=update_student)
    update_button.grid(row=5, column=0, columnspan=2, pady=10)



def delete_student():
    # Get the currently selected item in the student table
    selected_item = student_table.focus()

    # If no item is selected, show an error message
    if not selected_item:
        messagebox.showerror("Error", "Please select a student to delete.")
        return

    # Get the ID number of the selected student
    student_id = student_table.item(selected_item, 'values')[0]

    # Ask for confirmation
    confirm_delete = messagebox.askyesno("Confirm", f"Are you sure you want to delete the student with ID {student_id}?")

    # If confirmed, delete the student from the database
    if confirm_delete:
        # Connect to the SQLite database
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()

        # Execute the delete query
        cursor.execute("DELETE FROM student WHERE ID_Number=?", (student_id,))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Remove the student from the table
        student_table.delete(selected_item)

        # Show success message
        messagebox.showinfo("Success", f"Student with ID {student_id} deleted successfully.")

def add_course():
    # Create a popup window for adding a course
    popup_window = Toplevel(root)
    popup_window.geometry("300x150")
    popup_window.title("Add Course")

    # Labels and entry fields for course code and name
    course_code_label = Label(popup_window, text="Course Code:")
    course_code_label.grid(row=0, column=0, padx=5, pady=5)
    course_code_entry = Entry(popup_window)
    course_code_entry.grid(row=0, column=1, padx=5, pady=5)

    course_name_label = Label(popup_window, text="Course Name:")
    course_name_label.grid(row=1, column=0, padx=5, pady=5)
    course_name_entry = Entry(popup_window)
    course_name_entry.grid(row=1, column=1, padx=5, pady=5)

    # Function to submit the course details
    def submit_course():
        # Retrieve the course code and name from the entry fields
        course_code = course_code_entry.get().strip().upper()
        course_name = course_name_entry.get().strip().title()

        # Check if both course code and name are provided
        if course_code and course_name:
            # Connect to the SQLite database
            conn = sqlite3.connect('student.db')
            cursor = conn.cursor()
        else:
            # Show error message if course code or name is missing
            messagebox.showerror("Error", "Both Course Code and Course Name are required.")
        
        cursor.execute("SELECT COUNT(*) FROM course WHERE Course_Code = ?", (course_code,))
        existing_course = cursor.fetchone()[0]

        if existing_course > 0:
            messagebox.showerror("Error", f"Course with code '{course_code}' already exists.")
        else:
            # Insert the course into the database
            cursor.execute("INSERT INTO course (Course_Code, Course_Name) VALUES (?, ?)", (course_code, course_name))

            # Insert the new course into the course table GUI
            course_table.insert("", "end", values=(course_name,))

            # Close the popup window
            popup_window.destroy()

            # Show success message
            messagebox.showinfo("Success", "Course added successfully.")
        conn.commit()
        conn.close()
        

    # Button to submit the course details
    submit_button = Button(popup_window, text="Submit", command=submit_course)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)


def delete_course():
    # Get the selected course from the course table
    selected_item = course_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a course to delete.")
        return

    # Get the course name from the selected item
    course_name = course_table.item(selected_item, "values")[0]

    # Confirm deletion
    confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the course '{course_name}'?")

    if confirmation:
        # Connect to the database
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()

        # Fetch the course code corresponding to the selected course name
        cursor.execute("SELECT Course_Code FROM course WHERE Course_Name=?", (course_name,))
        course_code = cursor.fetchone()[0]  # Fetch the first column of the first row

        # Delete the course from the database
        cursor.execute("DELETE FROM course WHERE Course_Name=?", (course_name,))

        # Update the students' course codes and statuses in the database
        cursor.execute("UPDATE student SET Course_Code=?, Status=? WHERE Course_Code=?", ("NONE", "NOT ENROLLED", course_code))

        # Commit changes
        conn.commit()

        # Close connection
        conn.close()

        # Remove the course from the course table GUI
        course_table.delete(selected_item)

        # Update the affected student rows in the GUI table
        for row_id in student_table.get_children():
            row_data = student_table.item(row_id, "values")
            if row_data[4] == course_code:  # Check if the student is enrolled in the deleted course
                student_table.item(row_id, values=(row_data[0], row_data[1], row_data[2], row_data[3], "NONE", "NOT ENROLLED"))

        # Show success message
        messagebox.showinfo("Success", f"Course '{course_name}' deleted successfully.")

def search_student():
    search_text = search_entry.get().strip().lower()
    
    # Clear selections
    student_table.selection_remove(student_table.selection())
    
    if search_text:
        # Search in student table
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()

        # Search for students
        cursor.execute("""
            SELECT * FROM student 
            WHERE ID_Number LIKE ? 
            OR Name LIKE ? 
            OR Year_Level LIKE ? 
            OR Gender LIKE ? 
            OR Course_Code LIKE ? 
            OR Status LIKE ?""",
            ('%' + search_text + '%', '%' + search_text + '%', 
            '%' + search_text + '%', '%' + search_text + '%',
            '%' + search_text + '%', search_text))
        student_data = cursor.fetchall()

        for student in student_data:
            # Get the row ID of the student in the GUI table
            row_id = None
            for row in student_table.get_children():
                if student_table.item(row, 'values')[0] == student[0]:
                    row_id = row
                    break
            if row_id:
                student_table.selection_add(row_id)

        # Close connection
        conn.close()

def search_course():
    search_text = search_entry.get().strip().lower()
    
    # Clear selections
    course_table.selection_remove(course_table.selection())
    
    if search_text:
        # Search in course table
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM course 
            WHERE Course_Code LIKE ? 
            OR Course_Name LIKE ?""",
            ('%' + search_text + '%', '%' + search_text + '%'))
        course_data = cursor.fetchall()

        for course in course_data:
            # Search for matching rows in the GUI table
            for row_id in course_table.get_children():
                values = course_table.item(row_id, 'values')
                if search_text in str(values).lower():
                    course_table.selection_add(row_id)

        # Close connection
        conn.close()

def search():
    search_student()
    search_course()






def display_student_data():
    # Clear existing data from the student table
    for row in student_table.get_children():
        student_table.delete(row)

    # Connect to the database
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    # Fetch student data from the database
    cursor.execute("SELECT * FROM student")
    student_data = cursor.fetchall()

    # Insert fetched data into the student table
    for student in student_data:
        student_table.insert("", "end", values=student)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def display_course_data():
    # Clear existing data from the course table
    for row in course_table.get_children():
        course_table.delete(row)

    # Connect to the database
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    # Fetch course data from the database
    cursor.execute("SELECT Course_Name FROM course")
    course_data = cursor.fetchall()

    # Insert fetched data into the course table
    for course in course_data:
        course_table.insert("", "end", values=course)

    # Commit changes and close connection
    conn.commit()
    conn.close()

frame = LabelFrame(root, borderwidth = 1, bg = "#272829", pady = 50)

# create a search bar
search_bar = Frame(frame, bg="#ffffff", padx=10, pady=10)
search_bar.grid(row=6, column=0, sticky="n", pady = (20, 0))

search_label = Label(search_bar, text="Search:", bg="#ffffff")
search_label.grid(row=0, column=0)

search_entry = Entry(search_bar, width=10)
search_entry.grid(row=0, column=1)

search_button = Button(search_bar, text="Search", command = search)
search_button.grid(row=0, column=2)

#buttons
add_student_button = Button(frame, text = "Add Student", width = 10,  fg = "black",command = add_student, bg= "#FFF6E0", font=("David", 14, "bold"))
update_student_button = Button(frame, text = "Edit", width = 10, command = edit_student, bg= "#FFF6E0", font=("David", 14, "bold"))
delete_student_button = Button(frame, text = "Delete", width = 10, command = delete_student,  fg = "black", bg= "#FFF6E0", font=("David", 14, "bold"))

add_course_button = Button(frame, text = "Add Course", width = 10, command = add_course, fg = "black", bg= "#FFF6E0", font=("David", 14, "bold"))
delete_course_button =  Button(frame, text = "Delete Course", width = 10, command = delete_course, fg = "black", bg= "#FFF6E0", font=("David", 14, "bold"))
format_label = Label(frame, text = "FORMAT \n ID_Number: xxxx_xxxx", bg = "#FFF6E0")

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
add_student_button.grid(row = 0, column = 0, pady = (80, 0))
update_student_button.grid(row = 1, column = 0 )
delete_student_button.grid(row = 2, column = 0 )

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
add_course_button.grid(row = 4, column = 0, pady = (20,0))
delete_course_button.grid(row = 5, column = 0)
format_label.grid(row = 8, column = 0 , pady = 20)
display_student_data()
display_course_data()


root.mainloop()
