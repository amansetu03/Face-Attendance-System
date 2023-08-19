import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import os
import tkinter as tk
from PIL import Image
from tkinter import filedialog
ref = None
from AutoEncoding import AutoEncoading

def firstStape():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "database url",
        'storageBucket': "storage url"
    })
    return ref

# to ensure that id is unoique
def loadId():
    c = AutoEncoading()
    id = input("enter 6 disit ID: ")
    for i in c.studentIds:
        if i == str(id):
            print("this user id is abailable plz enter again ")
            loadId()
    return id

def uploadImage(id):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    # Open a file dialog for the user to select a PNG image
    path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png;*.jpg;*.jpeg")])
    # Check if the user selected a file
    if path:
        # Get the Firebase storage bucket
        bucket = storage.bucket()

        # Get the base name of the file
        file_name = os.path.basename(path)
        renamed_file = f'{id}.png'
        file_path = f'Images/{renamed_file}'

        # Open the image using PIL
        image = Image.open(path)
        # resized_image = image.resize((216, 216))
        temp_path = "resized_image.png"
        image.save(temp_path)
        image.save(file_path)
        blob = bucket.blob(file_path)
        blob.upload_from_filename(temp_path)
        os.remove(temp_path)
        # Print the uploaded image URL
        print("Image uploaded successfully. URL:", blob.public_url)
    else:
        print("No file selected.")


# main function for adding data
def add_new_data():
    global ref
    if not ref:
        ref = firstStape()
    name = input("Enter student's name: ")
    id = loadId()
    branch = input("Enter student's branch: ").upper()
    section = input("Enter student's section: ").upper()
    starting_year = int(input("Enter student's starting year: "))
    year = int(input("enter current year: "))
    # Create a dictionary to store the student's information
    ref = db.reference('Students')
    data = {
        f"{id}":
        {
            "name": name,
            "Branch": branch,
            "starting_year": starting_year,
            "total_attendance": 0,
            "Section": section,
            "year": year,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
    }
    print("plz Upload Image.")
    uploadImage(id)
    print("Image is uploaded")
    for key, value in data.items():
        ref.child(key).set(value)
    print("Basic Details is uploaded")


if __name__ == "__main__":
    print("enter 1 to add new student data")
    print("enter Q to exit")
    while True:
        n = input("enter choice: ")
        if n == "1":
            add_new_data()
        elif n in "Qq":
            Au = AutoEncoading()
            Au.getEncoading()
            print("program end")
            break
