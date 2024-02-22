import time
from datetime import datetime
import sqlite3
import requests
import random



class User:
    def __init__(self, username, name, email, password, user_type, logged_in):
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.logged_in = logged_in
        
    @classmethod
    def delete_user(cls, username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
            Clinic_database.commit()
            print(f"User with username {username} deleted successfully")

        
    @classmethod
    def register_account(cls):
        username = input("Enter username: ")
        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        user_type = input("Enter user type: ")
        new_account = cls(username, name, email, password, user_type, logged_in=False) #create and return a User object
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
                        User_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(255) UNIQUE,
                        name VARCHAR(255),
                        Email VARCHAR(255),
                        Password VARCHAR(255),
                        User_type VARCHAR(255),
                        Logged_in BOOLEAN)
                    ''')
        cursor.execute("SELECT * FROM Users WHERE email = ? OR username = ?", (email, username))
        existing_user = cursor.fetchone()
        if existing_user is not None:
            print("User with this email or username already exists.")
            return False
        else:

            cursor.execute('''INSERT INTO Users (username, name, email, password, user_type, logged_in)
                            VALUES (?, ?, ?, ?, ?, ?)
                           ''', (new_account.username, new_account.name, new_account.email,new_account.password, new_account.user_type, new_account.logged_in))
        Clinic_database.commit()
        print("registered successfully")
        return True
    
    
    @classmethod
    def login(cls, username, password):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
            existing_user = cursor.fetchone()
            
            if existing_user is not None:
                if existing_user[6] == 1:
                    print("You  have been logged in before")
                    return True
                else:
                    cursor.execute("UPDATE Users SET logged_in = 1 WHERE username = ?", (username,))
                    Clinic_database.commit()
                    print("logged in successfully")
                    return True
            else:
                print("invalid username or password")
                return False
            
            
    @classmethod
    def logout(cls, username, password):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("You are currently logged out")
                    return True
                else:
                    cursor.execute('''UPDATE Users SET logged_in = 0 WHERE username = ?''', (username,))
                    Clinic_database.commit()
                    print("logged out successfully")
                    return True
            else:
                print("invalid username or password")
                return False
            
    @classmethod
    def Update_profile(cls, username, password):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("please log in at first")
                    return True
                else:
                    new_name = input("Enter new name: ")
                    new_email = input("Enter new email: ")
                    new_password = input("Enter new password: ")
                    cursor.execute('''UPDATE Users SET name = ?, email = ?, password = ? WHERE username = ?''', (new_name, new_email, new_password, username))
                    Clinic_database.commit()
                    print("update profile successfully")
                    return True
            else:
                print("invalid username or password")
                return False
    @classmethod
    def view_appoinment(cls, username, password):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT ClinicID, DateTime, Status FROM Appointments JOIN Users ON Appointments.UserID = Users.User_id 
                           WHERE username = ? AND password = ?''', (username, password))
            result = cursor.fetchall()
            return result
        
        



class Clinic:
    def __init__(self, clinic_id, name, address, phone_number, services, capacity, availablity):
        self.clinic_id = clinic_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.services = services
        self.capacity = capacity
        self.availablity = availablity

    @classmethod
    def AddClinic(cls):
        response = requests.get('http://127.0.0.1:5000/slots')
        if response.status_code == 200:
            id_and_cap = response.json()  # converted response to json
            with sqlite3.connect("Clinic Database.sql") as Clinic_database:
                cursor = Clinic_database.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS Clinics (
                            Clinic_id INTEGER PRIMARY KEY,
                            name TEXT NULLABLE,
                            address TEXT NULLABLE,
                            phone_number TEXT NULLABLE,
                            services TEXT NULLABLE,
                            capacity INTEGER,
                            availability BOOLEAN NULLABLE
                            )
                        ''')
                for clinic_id, capacity in id_and_cap.items():
                # Check if Clinic_id already exists
                    cursor.execute("SELECT * FROM Clinics WHERE Clinic_id = ?", (clinic_id,))
                    existing_clinic = cursor.fetchone()

                if existing_clinic is not None:
                    # Update existing record instead of inserting
                    cursor.execute('''UPDATE Clinics SET capacity = ? WHERE Clinic_id = ?''', (capacity, clinic_id))
                else:
                    # Insert new record
                    cursor.execute('''INSERT INTO Clinics (Clinic_id, capacity) VALUES(?, ?)''', (clinic_id, capacity))

                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Yas', 'Tehran, Ekbatan', '09122121021', 'Dental clinic', 1, 1))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Arya', 'shahrak gharb', '09230991250', 'Eye clinic', 1, 2))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Afra', 'Tajrish', '09230991163', 'Heart clinic', 0, 3))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Samarghand', 'Saadatabad', '09122064051', 'nouro clinic', 1, 4))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Shafa', 'Eslamshahr', '09128964951', 'orthopedia clinic', 0, 5))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Noor', 'Motehari street', '09216489632', 'Eye clinic', 1, 6))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Farda', 'Argentina square', '09337369788', 'Heart clinic', 0, 7))
                
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}")
          
    @classmethod
    def UpdateClinicInfo(cls, username, password):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("Please login first")
                    return True
                else:
                    if existing_user[5] == 'p':
                        print("you don,t have access to this part")
                        return True
                    else:
                        new_clinic_name = input("Enter new clinic name: ")
                        new_address = input("Entern new address: ")
                        new_phone_number = input('Enter new phone number: ')
                        new_services = input("Enter all of your services that you have now: ")
                        cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone number = ?, services = ? 
                                       WHERE Clinics.User_id = (SELECT Users.User_id FROM Users WHERE Users.username = ? AND Users.password = ?)
                                       ''', (new_clinic_name, new_address, new_phone_number, new_services, username, password))
                        Clinic_database.commit()
                        print("Update Clinic info successfully")
                        return True
            else:
                print("invalid username or password")
                return False
'''       
    @classmethod
    def set_availability(cls):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            if 
'''            

'''
    @classmethod
    def view_appointment():
'''        
                    
class Appoinment(Clinic, User):
    def __init__(self, Appoinment_id, clinic_id, User_id, DateTime, Status):
        super().__init__(clinic_id, User_id)
        self.Appoinment_id = Appoinment_id
        self.DateTime = DateTime
        self.Status = Status
        
    def check_clinic_capacity(self, clinic_id):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT capacity FROM Clinics WHERE Clinic_id = ?''', (clinic_id,))
            capacity = cursor.fetchone()
            if capacity and capacity[0] > 0:
                return True
            else:
                print("This clinic is full")
                return False
        
        
    @classmethod
    def make_appoinment(cls, username, password):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Appointments (
                            AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                            ClinicID INTEGER,
                            UserID INTEGER ,
                            DateTime DATETIME,
                            Status VARCHAR(255))
                        ''')
            cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[5] == 'c':
                    print("you don,t have access to this part")
                    return True
                else:
                    cursor.execute('''SELECT User_id FROM Users WHERE username = ? AND password = ?''', (username,password))
                    user_id_tuple = cursor.fetchone()
                    User_id = user_id_tuple[0]
                    Clinic_id = input("Enter your intended clinic id: ")
                    date_time_str = input("Enter date and time (YYYY-MM-DD HH:MM): ")
                    try:
                        DateTime = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
                        if cls.check_clinic_capacity(cls, Clinic_id) == True:
                            
                            cursor.execute('''INSERT INTO Appointments (ClinicID, UserID, DateTime, Status)
                                               VALUES (?, ?, ?, ?)''', (Clinic_id, User_id, DateTime, "Scheduled"))
                            cursor.execute('''UPDATE Clinics SET Capacity = Capacity - 1 WHERE Clinic_id = ?''', (Clinic_id,))
                        Clinic_database.commit()
                        
                        print("Appoinment scheduled successfully")
                        return True
                    except ValueError:
                        print("invalid date and time")
                        
            else:
                print("invalid username or password")
                return False
            
            
            
    @classmethod
    def cancell_appoinment(cls, username, password):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("please login first")
                    return True
                if existing_user[5] != 'p':
                    print("You can,t cancell the appoinment ")
                    return True
                else:
                    cursor.execute('''SELECT User_id FROM Users WHERE username = ? AND password = ?''', (username, password))
                    user_id_tuple = cursor.fetchone()
                    
                    if user_id_tuple is not None:
                        user_id = user_id_tuple[0]
                        cursor.execute('''UPDATE Appointments SET Status = ? WHERE UserID = ?''', ("cancelled", user_id))
                        Clinic_database.commit()
                        cursor.execute('''SELECT ClinicID FROM Appointments WHERE UserID = ?''', (user_id))
                        clinic_id_tuple = cursor.fetchone()
                        cursor.execute('''UPDATE Clinics SET Capacity = Capacity + 1 WHERE Clinic_id = ?''',(clinic_id_tuple[0]))
                        Clinic_database.commit()
                        print("appoinment have cancelled successfully")
                        return True
            else:
                return False
            

       
    @classmethod
    def reschedule_appoinment(cls, username, password):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("please login first")
                    return True
                if existing_user[5] != 'p':
                    print("You can,t change the appointment ")
                    return True
                else:
                    AppoinmentID = input("Enter your Appointment ID that you want change: ") 
                    new_time_str = input("Enter New time you want your appointment (YYYY-MM-DD HH:MM):   ")
                    cursor.execute('''SELECT * FROM Appointments WHERE AppointmentID = ?''', (AppoinmentID,))
                    new_datetime = datetime.strptime(new_time_str,"%Y-%m-%d %H:%M")
                    cursor.execute('''UPDATE Appointments SET DateTime = ?''', (new_datetime,))
                    Clinic_database.commit()
                    return True
            else:
                return False                 


 

def main():
    while True:
        print("1. register account")
        print("2. login account")
        select_options = input("Select option:  ")
        if select_options == '1':
            User.register_account()
        if select_options == '2':
            print("1. login with your username and password")
            print("2. login with one time password")
            login_method = input("select an option From above: ")
            if login_method == '1':
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                User.login(username, password)
                with sqlite3.connect("Clinic Database.sql") as Clinic_database:
                    cursor =  Clinic_database.cursor()
                    cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
                    existing_user = cursor.fetchone()
                    if existing_user is not None:
                        if existing_user[5] == 'p':
                            print("1. make appoinment")
                            print("2. cancell appoinment")
                            print("3. view appoinment")
                            print("4. logout")
                            print("5. updaate inoformation")
                            patient_options  = input("select your option: ")
                            if patient_options == '1':
                                Appoinment.make_appoinment(username, password)
                            elif select_options == '2':
                                Appoinment.cancell_appoinment(username, password)  
                            elif select_options == '3':
                                User.view_appoinment(username, password)
                            elif select_options == '4':
                                User.logout(username, password)
                            elif select_options == '5' :
                                if existing_user[5] == 'p':
                                    User.Update_profile(username, password)
                                    '''
        elif login_method == '2':
            generated_password = 
            
            
                
                                
main()
'''


def show_users():
    # Connect to the database
    with sqlite3.connect("Clinic Database.sql") as clinic_database:
        # Create a cursor
        cursor = clinic_database.cursor()

        # Execute SELECT query to fetch data from the Users table
        cursor.execute("SELECT * FROM Users")

        # Fetch all rows from the result set
        users = cursor.fetchall()

        # Print or process the retrieved data
        for user in users:
            print(user)
show_users()


def show_clinics():
    # Connect to the database
    with sqlite3.connect("Clinic Database.sql") as clinic_database:
        # Create a cursor
        cursor = clinic_database.cursor()

        # Execute SELECT query to fetch data from the Users table
        cursor.execute("SELECT * FROM Clinics")

        # Fetch all rows from the result set
        clinics = cursor.fetchall()

        # Print or process the retrieved data
        for clinic in clinics:
            print(clinic)
show_clinics()



# mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew mew



from sqlite3 import *

class AccessControl:
    def __init__(self, db_path):
        self.db_connection = self._connect_to_db(db_path)

    def _connect_to_db(self, db_path):
        try:
            connection = sqlite3.connect(db_path)
            print("اتصال به دیتابیس SQLite موفقیت‌آمیز بود")
            return connection
        except Error as e:
            print(f"خطا در اتصال به دیتابیس SQLite: {e}")
            return None

    def login(self, username, password, user_type):
        try:
            cur = self.db_connection.cursor()
            cur.execute(
                "SELECT * FROM users WHERE username=? AND password=? AND user_type=?",
                (username, password, user_type,)
            )
            record = cur.fetchone()
            if record:
                user = User(username, user_type)
                print(f"{username} به عنوان {user_type} وارد شد")
                return user
            else:
                print("اطلاعات وارد شده صحیح نیست یا کاربری با این مشخصات وجود ندارد.")
                return None
        except Error as e:
            print(f"خطا در هنگام تأیید اطلاعات کاربر: {e}")
            return None

    def get_access_level(self, user):
        access_levels = {
            'patient': ['book_appointment'],
            'doctor': ['view_schedule', 'manage_appointments'],
            'secretary': ['manage_all_appointments', 'interact_with_patients']
        }
        return access_levels.get(user.user_type, [])

db_path = 'Clinic Database.sql'

access_control = AccessControl(db_path)

user = access_control.login('johndoe', 'password123', 'doctor')

if user:
    access_rights = access_control.get_access_level(user)
    print(f"حقوق دسترسی برای {user.username}: {access_rights}")




class Doctor:
    def __init__(self, doctor_id, name, specialty, clinic_id):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty
        self.clinic_id = clinic_id

    def get_schedule(self, date):
        cur = access_control.db_connection.cursor()
        cur.execute(
            "SELECT time_slot FROM appointments WHERE doctor_id=? AND date=?",
            (self.doctor_id, date,)
        )
        schedule = cur.fetchall()
        return schedule

    def add_appointment(self, patient_id, date, time_slot):
        try:
            cur = access_control.db_connection.cursor()
            cur.execute(
                "INSERT INTO appointments (doctor_id, patient_id, date, time_slot) VALUES (?, ?, ?, ?)",
                (self.doctor_id, patient_id, date, time_slot,)
            )
            access_control.db_connection.commit()
            print(f"وقت ملاقات جدید برای {date} در {time_slot} اضافه شد.")
        except Error as e:
            print(f"خطا در هنگام اضافه کردن وقت ملاقات: {e}")

    def cancel_appointment(self, appointment_id):
        try:
            cur = access_control.db_connection.cursor()
            cur.execute(
                "DELETE FROM appointments WHERE id=?",
                (appointment_id,)
            )
            access_control.db_connection.commit()
            print(f"وقت ملاقات با شناسه {appointment_id} لغو شد.")
        except Error as e:
            print(f"خطا در هنگام لغو وقت ملاقات: {e}")


class Insurance:
    def __init__(self, db_connection, user_id, company_name, insurance_type):
        self.db_connection = db_connection
        self.user_id = user_id
        self.company_name = company_name
        self.insurance_type = insurance_type

    def register_insurance(self):
        try:
            cur = self.db_connection.cursor()
            cur.execute(
                "INSERT INTO insurance (user_id, company_name, insurance_type) VALUES (?, ?, ?)",
                (self.user_id, self.company_name, self.insurance_type,)
            )
            self.db_connection.commit()
            print(f"بیمه با موفقیت برای کاربر {self.user_id} ثبت شد.")
        except Error as e:
            print(f"خطا در هنگام ثبت بیمه: {e}")

    def update_insurance(self, company_name=None, insurance_type=None):
        try:
            cur = self.db_connection.cursor()
            if company_name:
                cur.execute(
                    "UPDATE insurance SET company_name = ? WHERE user_id = ?",
                    (company_name, self.user_id,)
                )
            if insurance_type:
                cur.execute(
                    "UPDATE insurance SET insurance_type = ? WHERE user_id = ?",
                    (insurance_type, self.user_id,)
                )
            self.db_connection.commit()
            print(f"اطلاعات بیمه برای کاربر {self.user_id} به‌روزرسانی شد.")
        except Error as e:
            print(f"خطا در هنگام به‌روزرسانی بیمه: {e}")

    def get_insurance_details(self):
        try:
            cur = self.db_connection.cursor()
            cur.execute(
                "SELECT company_name, insurance_type FROM insurance WHERE user_id = ?",
                (self.user_id,)
            )
            insurance_details = cur.fetchone()
            if insurance_details:
                return insurance_details
            else:
                print("اطلاعات بیمه برای این کاربر یافت نشد.")
                return None
        except Error as e:
            print(f"خطا در هنگام دریافت جزئیات بیمه: {e}")
            return None


        
###