# Import the time module.
import time
# Impost the os module.
import os
# Import the pymysql module.
import pymysql
# Import the flask module.
from flask import Flask, render_template, request, redirect
# Import the wtfroms module.
from wtforms import Form, StringField, PasswordField, SubmitField, SelectMultipleField, validators
# Import the flask login module.
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user

# Create the application.
app = Flask(__name__)
# Create the login manager and initial the login manager.
login_manager = LoginManager()
login_manager.init_app(app)
# Create the secret key.
app.secret_key = os.urandom(16)
# Create global values.
level = ''
user_admin = ''
logintime = ''
logouttime = ''
order = ''
training = ''

# Create a class for login.
class UserLogin(UserMixin):
    # Initialize the user login class.
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Create a class of the database connection.
class DatabaseOperations():
    # The attributes to store the host, username, password and database.
    __db_url = '172.16.199.106'
    __db_username = '1730026042'
    __db_password = '88888888'
    __db_name = '1730026042'
    __db = ''
    # The constructor.
    def __init__(self):
        # Connect the database.
        self.__db = self.db_connect()
    # Make the connection.
    def db_connect(self):
        self.__db = pymysql.connect(self.__db_url, self.__db_username, self.__db_password, self.__db_name)
        return self.__db
    # Delete the connection.
    def __del__(self):
        self.__db.close()
    # Registration.
    def Registration(self, username, password, email, gender, address, phonenumber):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        registration = "INSERT INTO user_info VALUES (null,'%s', '%s', '%s', '%c', '%s', '%s')" % (username, password, email, gender, address, phonenumber)
        # Execute the sql.
        try:
            # Execute the sql.
            cursor.execute(registration)
            # Make change to the database.
            self.__db.commit()
            # Return the registrate successful message.
            return "Registrate Successful"
        except:
            # If update fail, then rollback the database.
            self.__db.rollback()
            # Return the fail message.
            return "Registrate Fail"
    # User exists testing.
    def UserExistTest(self, username):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT USERNAME FROM user_info WHERE USERNAME = '%s'" % (username)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        if result:
            return True
        else:
            return False
    # User exists testing.
    def AdminExistTest(self, username):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT USERNAME FROM admin_info WHERE USERNAME = '%s'" % (username)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        if result:
            return True
        else:
            return False
    # Login as a user identify.
    def LoginAsUser(self, username, password):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT USERNAME FROM user_info WHERE USERNAME = '%s' AND PASSWORD = '%s'" % (username, password)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Login as an admin identify.
    def LoginAsAdmin(self, username, password):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT LEVEL FROM admin_info WHERE USERNAME = '%s' AND PASSWORD = '%s'" % (username, password)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Update the users access time.
    def UpdateAccessTime(self, username, logintime, logouttime, accesstime):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test1 = "INSERT INTO accesstime VALUES (null,'%s','%s','%s','%s')" % (username, logintime, logouttime, accesstime)
        # Execute the sql.
        try:
            cursor.execute(test1)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
        # Create the sql.
        test2 = "SELECT ACCESSID FROM accesstime WHERE LOGINTIME = '%s'" % (logintime)
        # Execute the sql.
        cursor.execute(test2)
        # Get the value.
        accessid = cursor.fetchall()
        # Create the sql.
        test3 = "INSERT INTO have VALUES (%d, %d)" % (accessid[0][0], user_admin.id[0][0])
        # Execute the sql.
        try:
            cursor.execute(test3)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
        # Create the sql.
    # Test whether the user is a admin.
    def IsAdmin(self, username):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT USERNAME FROM admin_info WHERE USERNAME = '%s'" % (username)
        # Execute the sql.
        cursor.execute(test)
        # Fetch the result.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Get the applicant.
    def UpdateApplicant(self, username, phonenumber, job):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test1 = "SELECT USERNAME FROM applicant WHERE APPLICANTID = (SELECT APPLICANTID FROM applicate WHERE USERID = %d)" % (user_admin.id[0][0])
        # Execute the sql.
        cursor.execute(test1)
        # Get the result.
        result = cursor.fetchall()
        # Indicate use update or insert.
        if result:
            # Create the sql.
            test2 = "UPDATE applicant SET job = '%s' WHERE APPLICANTID = (SELECT APPLICANTID FROM applicate WHERE USERID = %d)" % (job, user_admin.id[0][0])
            # Execute the sql.
            try:
                cursor.execute(test2)
                # Change the table.
                self.__db.commit()
            except:
                # If the change is not legal, rollback to the original page.
                self.__db.rollback()
        else:
            # Create the sql.
            test3 = "INSERT INTO applicant VALUES (null, '%s', '%s', '%s')" % (username, phonenumber, job)
            # Execute the sql.
            try:
                cursor.execute(test3)
                # Change the table.
                self.__db.commit()
            except:
                # If the change is not legal, rollback to the original page.
                self.__db.rollback()
            # Create the sql.
            test4 = "SELECT APPLICANTID FROM applicant WHERE USERNAME = '%s'" % (username)
            # Execute the sql.
            cursor.execute(test4)
            # Get the value.
            applicantid = cursor.fetchall()
            # Create the sql.
            test5 = "SELECT USERID FROM user_info WHERE USERNAME = '%s'" % (username)
            # Execute the sql.
            cursor.execute(test5)
            # Get the value.
            userid = cursor.fetchall()
            # Create the sql.
            test6 = "INSERT INTO applicate VALUES (%d, %d)" % (userid[0][0], applicantid[0][0])
            # Execute the sql.
            try:
                cursor.execute(test6)
                # Change the table.
                self.__db.commit()
            except:
                # If the change is not legal, rollback to the original page.
                self.__db.rollback()
        return result
    # Get the training.
    def UpdateTraining(self, username, phonenumber, training_time):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test1 = "SELECT USERNAME FROM training WHERE TRAININGID = (SELECT TRAININGID FROM booking WHERE USERID = %d)" % (user_admin.id[0][0])
        # Execute the sql.
        cursor.execute(test1)
        # Get the result.
        result = cursor.fetchall()
        # Indicate use update or insert.
        if result:
            # Create the sql.
            test2 = "UPDATE training SET time = '%s' WHERE TRAININGID = (SELECT TRAININGID FROM booking WHERE USERID = %d)" % (training_time, user_admin.id[0][0])
            # Execute the sql.
            try:
                cursor.execute(test2)
                # Change the table.
                self.__db.commit()
            except:
                # If the change is not legal, rollback to the original page.
                self.__db.rollback()
        else:
            test3 = "INSERT INTO training VALUES (null, '%s', '%s', '%s', %d)" % (username, training_time, phonenumber, 0)
            # Execute the sql.
            try:
                cursor.execute(test3)
                # Change the table.
                self.__db.commit()
            except:
                # If the change is not legal, rollback to the original page.
                self.__db.rollback()
            # Create the sql.
            test4 = "SELECT TRAININGID FROM training WHERE USERNAME = '%s'" % (username)
            # Execute the sql.
            cursor.execute(test4)
            # Get the value.
            trainingid = cursor.fetchall()
            # Create the sql.
            test5 = "SELECT USERID FROM user_info WHERE USERNAME = '%s'" % (username)
            # Execute the sql.
            cursor.execute(test5)
            # Get the value.
            userid = cursor.fetchall()
            # Create the sql.
            test6 = "INSERT INTO booking VALUES (%d, %d)" % (userid[0][0], trainingid[0][0])
            # Execute the sql.
            try:
                cursor.execute(test6)
                # Change the table.
                self.__db.commit()
            except:
                # If the change is not legal, rollback to the original page.
                self.__db.rollback()
        return result
    # Change the training payment state.
    def ChangeTrainingPayment(self, username):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "UPDATE training SET PAYMENTSTATE = 1 WHERE TRAININGID = (SELECT TRAININGID FROM booking WHERE USERID = %d)" % (user_admin.id[0][0])
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
    # Get the info for the admin.
    def GetAdminInfo(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT * FROM admin_info WHERE USERID = %d" % (user_admin.id[0][0])
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Get the info for the admin.
    def GetUserInfo(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT * FROM user_info WHERE USERID = %d" % (user_admin.id[0][0])
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the result.
        return result
    # Update the user info.
    def UpdateUserAdminInfo(self, username, address, email, phone, gender):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Get the level of the user.
        test1 = "SELECT LEVEL FROM admin_info WHERE USERID = '%d'" % (user_admin.id[0][0])
        # Execute the sql.
        cursor.execute(test1)
        # Get the result.
        result = cursor.fetchall()
        # If the user is an admin.
        if result:
            # Create the sql.
            test2 = "UPDATE admin_info SET USERNAME = '%s', ADDRESS = '%s', EMAIL = '%s', PHONENUMBER = '%s', GENDER = '%c' WHERE USERID = %d" % (username, address, email, phone, gender, user_admin.id[0][0])
            # Execute the sql.
            try:
                cursor.execute(test2)
                # Change the table.
                self.__db.commit()
            except:
                # If the change is not legal, rollback to the original page.
                self.__db.rollback()
        # Create the sql.
        test3 = "UPDATE user_info SET USERNAME = '%s', ADDRESS = '%s', EMAIL = '%s', PHONENUMBER = '%s', GENDER = '%c' WHERE USERID = %d" % (username, address, email, phone, gender, user_admin.id[0][0])
        # Execute the sql.
        try:
            cursor.execute(test3)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
    # Get the id of the user.
    def GetUserId(self, username):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT USERID FROM user_info WHERE USERNAME = '%s'" % (username)
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Get the access time.
    def GetAccessTime(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT * FROM accesstime"
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Delete the access time.
    def DeleteAccessTime(self, ID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "DELETE FROM accesstime WHERE ACCESSID = %d" % (ID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
    # Get the applicant.
    def GetApplicant(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        if level == 0:
            test = "SELECT * FROM applicant WHERE APPLICANTID = (SELECT APPLICANTID FROM applicate WHERE USERID = %d)" % (user_admin.id[0][0])
        else:
            test = "SELECT * FROM applicant"
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Delete the applicant.
    def DeleteApplicant(self, ID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "DELETE FROM applicant WHERE APPLICANTID = %d" % (ID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
    # Get the training.
    def GetTraining(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        if level == 0:
            test = "SELECT * FROM training WHERE TRAININGID = (SELECT TRAININGID FROM booking WHERE USERID = %d)" % (user_admin.id[0][0])
        else:
            test = "SELECT * FROM training"
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Delete the applicant.
    def DeleteTraining(self, ID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "DELETE FROM training WHERE TRAININGID = %d" % (ID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
    # Get About Us Info.
    def GetAboutUs(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT * FROM admin_info"
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Get hot flower.
    def GetHotFlower(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT * FROM flowers_info WHERE HOT = 1"
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Get all the flower.
    def GetAllFlower(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT * FROM flowers_info"
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Get each flower details
    def GetEachFlower(self, ID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT * FROM flowers_info WHERE FLOWERID = %d" % (ID)
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Search the flower.
    def SearchFlower(self, flowername):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT * FROM flowers_info WHERE FLOWERNAME = '%s'" % (flowername)
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Leave the comments.
    def LeaveComments(self, username, flowername, comments):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Get the time.
        leaveTime = time.time()
        # Create the sql.
        test1 = "INSERT INTO comment VALUES (null, '%s', '%s', '%s', '%s')" % (username, comments, flowername, str(leaveTime))
        # Execute the sql.
        try:
            cursor.execute(test1)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
        # Create the sql.
        test2 = "SELECT COMMENTID FROM comment WHERE LEAVETIME = '%s'" % (str(leaveTime))
        # Execute the sql.
        cursor.execute(test2)
        # Get the value.
        commentid = cursor.fetchall()
        # Create the sql.
        test3 = "INSERT INTO writtenby VALUES (%d, %d)" % (commentid[0][0], user_admin.id[0][0])
        # Execute the sql.
        try:
            cursor.execute(test3)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
        # Create the sql.
        test4 = "SELECT FLOWERID FROM flowers_info WHERE FLOWERNAME = '%s'" % (flowername)
        # Execute the sql.
        cursor.execute(test4)
        # Get the value.
        flowerid = cursor.fetchall()
        # Create the sql.
        test5 = "INSERT INTO belongto VALUES (%d, %d)" % (commentid[0][0], flowerid[0][0]) 
        # Execute the sql.
        try:
            cursor.execute(test5)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
    # Get the comments.
    def GetComments(self, flowername):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT USERNAME, COMMENT FROM comment WHERE FLOWERNAME = '%s'" % (flowername)
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Get the order.
    def GetOrder(self, username, flowername, flowerprice, quantity, totalprice):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Get the order time.
        orderTime = time.time()
        # Create the sql.
        test = "INSERT INTO cart VALUES (null, '%s', '%s', %d, %d, %d, '%s')" % (username, flowername, flowerprice, quantity, totalprice, str(orderTime))
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
        # Create the sql.
        test2 = "SELECT ORDERID FROM cart WHERE ORDERTIME = '%s'" % (str(orderTime))
        # Execute the sql.
        cursor.execute(test2)
        # Get the value.
        orderid = cursor.fetchall()
        # Create the sql.
        test3 = "INSERT INTO owner VALUES (%d, %d)" % (orderid[0][0], user_admin.id[0][0])
        # Execute the sql.
        try:
            cursor.execute(test3)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
        # Create the sql.
        test4 = "SELECT FLOWERID FROM flowers_info WHERE FLOWERNAME = '%s'" % (flowername)
        # Execute the sql.
        cursor.execute(test4)
        # Get the value.
        flowerid = cursor.fetchall()
        # Create the sql.
        test5 = "INSERT INTO stored VALUES (%d, %d)" % (flowerid[0][0], orderid[0][0]) 
        # Execute the sql.
        try:
            cursor.execute(test5)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
        # Create the sql.
        test6 = "INSERT INTO ordered VALUES (%d, %d)" % (user_admin.id[0][0], flowerid[0][0]) 
        # Execute the sql.
        try:
            cursor.execute(test6)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
    # Get the cart.
    def GetCart(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create a empty list.
        result = []
        # Create the sql.
        test = "SELECT ORDERID FROM owner WHERE USERID = %d" % (user_admin.id[0][0])
        # Execute the sql.
        cursor.execute(test)
        # Get the id.
        orderid = cursor.fetchall()
        # Get the payment order.
        for each in orderid:
            # Create the sql.
            test1 = "SELECT * FROM cart WHERE ORDERID = %d" % (each[0])
            # Execute the sql.
            cursor.execute(test1)
            # Insert into the list.
            result.append(cursor.fetchall()[0])
        # Return the value.
        return result
    # Get the total price.
    def GetTotalPrice(self, ID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "SELECT TOTALPRICE FROM cart WHERE ORDERID = %d" % (ID)
        # Execute the sql.
        cursor.execute(test)
        # Get the value.
        result = cursor.fetchall()
        # Return the value.
        return result
    # Delete the order.
    def DeleteOrder(self, ID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "DELETE FROM cart WHERE ORDERID = %d" % (ID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
    # Do the payment.
    def DoPaymentForOrder(self, ID, paymentTime):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test1 = "SELECT * FROM cart WHERE ORDERID = %d" % (ID)
        # Execute the sql.
        cursor.execute(test1)
        # Get the value.
        order = cursor.fetchall()
        # Create the sql.
        test2 = "INSERT INTO payment VALUES (null, '%s', '%s', %d, %d, %d, '%s')" % (order[0][1], order[0][2], order[0][3], order[0][4], order[0][5], paymentTime)
        # Execute the sql.
        try:
            cursor.execute(test2)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
        # Delete the order.
        self.DeleteOrder(ID)
        # Create the sql.
        test2 = "SELECT PAYMENTID FROM payment WHERE PAYTIME = '%s'" % (paymentTime)
        # Execute the sql.
        cursor.execute(test2)
        # Get the value.
        paymentid = cursor.fetchall()
        # Create the sql.
        test3 = "INSERT INTO paid VALUES (%d, %d)" % (paymentid[0][0], user_admin.id[0][0])
        # Execute the sql.
        try:
            cursor.execute(test3)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
        # Delete the order.
        self.DeleteOrder(ID)
    # Do the payment.
    def DoPaymentForTraining(self, ID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "UPDATE training SET PAYMENTSTATE = 1 WHERE TRAININGID = %d" % (ID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()
    # Get payment order.
    def GetPaymentOrder(self):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Indicate the privilege.
        if level == 1:
            test = "SELECT * FROM payment"
            # Execute the sql.
            cursor.execute(test)
            # Get the value.
            result = cursor.fetchall()
        if level == 0:
            # Create a empty list.
            result = []
            # Create the sql.
            test = "SELECT PAYMENTID FROM paid WHERE USERID = %d" % (user_admin.id[0][0])
            # Execute the sql.
            cursor.execute(test)
            # Get the id.
            paymentid = cursor.fetchall()
            # Get the payment order.
            for each in paymentid:
                # Create the sql.
                test1 = "SELECT * FROM payment WHERE PAYMENTID = %d" % (each[0])
                # Execute the sql.
                cursor.execute(test1)
                # Insert into the list.
                result.append(cursor.fetchall()[0])
        # Return the value.
        return result
    # Delete the order.
    def DeletePaymentOrder(self, ID):
        # Create a cursor to execute the sql.
        cursor = self.__db.cursor()
        # Create the sql.
        test = "DELETE FROM payment WHERE PAYMENTID = %d" % (ID)
        # Execute the sql.
        try:
            cursor.execute(test)
            # Change the table.
            self.__db.commit()
        except:
            # If the change is not legal, rollback to the original page.
            self.__db.rollback()

# Create a class for registration form.
class RegistrationForm(Form):
    # Get each of the value.
    Username = StringField('Username', [validators.DataRequired(), validators.Length(max = 25)])
    Password = PasswordField('Password', [validators.DataRequired(), validators.Length(min = 4, max = 25)])
    RePassword = PasswordField('RePassword', [validators.DataRequired(), validators.EqualTo('Password')])
    Email = StringField('Email', [validators.Length(max = 26)])
    Address = StringField('Address', [validators.DataRequired()])
    Phone = StringField('Phone', [validators.DataRequired(), validators.Length(max = 15)])
    Gender = StringField('Gender', [validators.DataRequired()])

# Create a class for users login form.
class UserLoginForm(Form):
    # Get each of the value.
    Username = StringField('Username', [validators.DataRequired(), validators.Length(max = 25)])
    Password = PasswordField('Password', [validators.DataRequired(), validators.Length(min = 4, max = 25)])
    User = SubmitField('User', [validators.DataRequired()])

# Create a class for admin login form.
class AdminLoginForm(Form):
    # Get each of the value.
    Username = StringField('Username', [validators.DataRequired(), validators.Length(max = 25)])
    Password = PasswordField('Password', [validators.DataRequired(), validators.Length(min = 4, max = 25)])
    Admin = SubmitField('Admin', [validators.DataRequired()])

# Create a class for applicant form.
class ApplicantForm(Form):
    # Get each of the value.
    username = StringField('username', [validators.DataRequired(), validators.Length(max = 25)])
    phonenumber = StringField('phonenumber', [validators.DataRequired(), validators.Length(min = 11, max = 15)])
    job = StringField('job', [validators.DataRequired()])

# Create a class for training form.
class TrainingForm(Form):
    # Get each of the value.
    username = StringField('username', [validators.DataRequired(), validators.Length(max = 25)])
    phonenumber = StringField('phonenumber', [validators.DataRequired(), validators.Length(min = 11, max = 25)])
    training_time = StringField('training_time', [validators.DataRequired()])

# Create a class for payment.
class PaymentForm(Form):
    # Get each of the value.
    payment = SubmitField('payment', [validators.DataRequired()])

# Create a class for update user or admin info.
class UpdateUserAdminInfoForm(Form):
    # Get each of the value.
    Username = StringField('Username', [validators.DataRequired(), validators.Length(max = 25)])
    Email = StringField('Email', [validators.Length(max = 26)])
    Address = StringField('Address', [validators.DataRequired()])
    Phone = StringField('Phone', [validators.DataRequired(), validators.Length(max = 15)])
    Gender = StringField('Gender', [validators.DataRequired(), validators.Length(max = 1)])

# Create a class for delete the access time information.
class DeleteAccessTimeForm(Form):
    # Get each of the value.
    Access = SelectMultipleField('Access')
    Delete_Access = SubmitField('Delete', [validators.DataRequired()])

# Create a class for delete the access time information.
class DeleteApplicantForm(Form):
    # Get each of the value.
    Applicant = SelectMultipleField('Applicant')
    Delete_Applicant = SubmitField('Delete', [validators.DataRequired()])

# Create a class for delete the access time information.
class DeleteTrainingForm(Form):
    # Get each of the value.
    Training = SelectMultipleField('Training')
    Delete_Train = SubmitField('Delete', [validators.DataRequired()])
    Pay_Train = SubmitField('Pay', [validators.DataRequired()])

# Create a class for delete the history order information.
class DeleteHistoryOrderForm(Form):
    # Get each of the value.
    History = SelectMultipleField('History')
    Delete_History = SubmitField('Delete', [validators.DataRequired()])

# Create a class for get flowers detail.
class GetFlowerForm(Form):
    # Get each of the value.
    GetInfo = StringField('GetInfo')

# Create a class for search the flower.
class SearchFlowerForm(Form):
    # Get each of the value.
    flower = StringField('flower')

# Create a class for leave comments.
class LeaveCommentsForm(Form):
    # Get each of the value.
    username = StringField('username')
    comments = StringField('comments', [validators.DataRequired()])
    leave_comments = StringField('leave_comments')

# Create a class for unique order.
class OrderUniqueFlowerForm(Form):
    # Get each of the value.
    UniqueOrder = StringField('UniqueOrder')

# Create a class for multi order.
class OrderMultiFlowerForm(Form):
    # Get each of the value.
    quantity = StringField('quantity')
    MultiOrder = StringField('MultiOrder')

# Create a class for the cart operation.
class CartOperationForm(Form):
    # Get each of the value.
    Order = SelectMultipleField('Order')
    Total = StringField('Total')
    Delete = StringField('Delete')
    Pay = StringField('Pay')

# Create a class for the payment.
class PaymentConfirmForm(Form):
    # Get each of the value.
    payment = StringField('payment')

# The function for load the user.
@login_manager.user_loader
def load_user(user_id):
    return UserLogin(user_id, user_admin.username, user_admin.password)

# The function for homepage.
@app.route('/')
def Homepage(message = ""):
    # Create the database.
    db = DatabaseOperations()
    # Get the value.
    result = db.GetHotFlower()
    # Close the database.
    db.__del__()
    # Return the value.
    return render_template('Homepage.html', level = level, admin = result, message = message)

# The function for about us.
@app.route('/About Us')
def About_Us():
    # Create the database.
    db = DatabaseOperations()
    # Get the value.
    result = db.GetAboutUs()
    # Close the database.
    db.__del__()
    # Return the value.
    return render_template('About Us.html', level = level, admin = result)

# Get the order.
@app.route('/Get Order', methods = ['GET', 'POST'])
@login_required
def Get_Order():
    # Create a variable to occupy the position of the parameter.
    occupy = ""
    # Create an instance of the form.
    uniqueOrderForm = OrderUniqueFlowerForm(request.form)
    multiOrderForm = OrderMultiFlowerForm(request.form)
    # Indicate the form.
    if uniqueOrderForm.UniqueOrder.data:
        # Create a database conection.
        db = DatabaseOperations()
        # Get the flower.
        flower = db.GetEachFlower(int(uniqueOrderForm.UniqueOrder.data))
        # Get the order.
        db.GetOrder(user_admin.username, flower[0][1], flower[0][4], 1, (flower[0][4]*1))
        # Close the cart.
        db.__del__()
        # Get the result.
        message = "Order successful"
    if multiOrderForm.MultiOrder.data:
        # Create a database conection.
        db = DatabaseOperations()
        # Get the flower.
        flower = db.GetEachFlower(int(multiOrderForm.MultiOrder.data))
        # Get the order.
        db.GetOrder(user_admin.username, flower[0][1], flower[0][4], int(multiOrderForm.quantity.data), (flower[0][4]*int(multiOrderForm.quantity.data)))
        # Close the cart.
        db.__del__()
        # Get the result.
        hints = "Order successful"
        # Return the value.
        return Flower_Details(hints, occupy, flower, int(multiOrderForm.quantity.data), flower[0][4]*int(multiOrderForm.quantity.data))
    # Return the value.
    return Homepage(message)

# The function for cart.
@app.route('/Cart')
@login_required
def Cart(price = ""):
    # Create the database connection.
    db = DatabaseOperations()
    # Get the value.
    result = db.GetCart()
    # Close the database connection.
    db.__del__()
    # Back to the page.
    return render_template('Cart.html', level = level, result = result, price = price)

# The function for cart operation.
@app.route('/Cart Operation', methods = ['GET', 'POST'])
@login_required
def Cart_Operation():
    # Get the order.
    global order
    # Create an instance of the form.
    cartOperation = CartOperationForm(request.form)
    # Indicate the form.
    if cartOperation.Total.data and cartOperation.Order.data:
        # Create a database connection.
        db = DatabaseOperations()
        # Initialize the price.
        price = 0
        # Get the total price.
        for each in cartOperation.Order.data:
            price = price + db.GetTotalPrice(int(each))[0][0]
        # Close the database connection.
        db.__del__()
        # Back to the page.
        return Cart(price)
    if cartOperation.Delete.data and cartOperation.Order.data:
        # Create a database connection.
        db = DatabaseOperations()
        # Delete the order.
        for each in cartOperation.Order.data:
            db.DeleteOrder(int(each))
        # Close the database connection.
        db.__del__()
    if cartOperation.Pay.data and cartOperation.Order.data:
        # Get the value.
        order = cartOperation.Order.data
        # Return to the page.
        return render_template('QR-Code.html', order = "order")
    # Back to the page.
    return Cart()

# The function for leave the comment.
@app.route('/Leave Comments', methods = ['GET', 'POST'])
@login_required
def Leave_Comments():
    # Create a variable to occupy the position of the parameter.
    occupy = "" 
    # Create an instance for the form.
    leaveCommentsForm = LeaveCommentsForm(request.form)
    # Create a database connection.
    db = DatabaseOperations()
    # Get the flower info.
    result = db.SearchFlower(leaveCommentsForm.leave_comments.data)
    # Validate the data.
    if leaveCommentsForm.validate():
        # Leave the comments.
        db.LeaveComments(user_admin.username, leaveCommentsForm.leave_comments.data, leaveCommentsForm.comments.data)
        # Close the database connection.
        db.__del__()
        # Back to the page.
        return Flower_Details(occupy, occupy, result)
    # Close the database connection.
    db.__del__()
    # If the comments are empty.
    return Flower_Details(occupy, occupy, result)

# The function for flower information.
@app.route('/Flower-Info')
def Flower_Info():
    # Create the database.
    db = DatabaseOperations()
    # Get the value.
    result = db.GetAllFlower()
    # Close the database.
    db.__del__()
    # Return the value.
    return render_template('Flower-Info.html', level = level, admin = result)

# The function for join us.
@app.route('/Join Us', methods = ['GET', 'POST'])
@login_required
def Join_Us():
    # Create a form of the appclicant.
    applicant = ApplicantForm(request.form)
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
         # Validate the input value.
        if applicant.validate():
            # Create an instance for the database.
            db = DatabaseOperations()
            # Indicate whether the username is exist or not.
            if db.UserExistTest(applicant.username.data):
                # Indicate whether the user is an admin.
                if db.IsAdmin(applicant.username.data):
                    username_error = "You are already the members of us, please focus on your work"
                    # Close the database connection.
                    db.__del__()
                    # Return to the page.
                    return render_template('Join Us.html', level = level, username_error = username_error)
                else:
                    # Indicate whether the username is the user hiself/herself.
                    if applicant.username.data != user_admin.username:
                        username_error = "Please type your own username"
                        # Close the database connection.
                        db.__del__()
                        # Return to the page.
                        return render_template('Join Us.html', level = level, username_error = username_error)
                    else:
                        # Insert the value into the table.
                        result = db.UpdateApplicant(applicant.username.data, applicant.phonenumber.data, applicant.job.data)
                        # Indicate the message.
                        if result:
                            message = "Because all the users can only apply one job, and you have applied before, therefore, we just update your work"
                        else:
                            message = "Applience Successful"
                        # Close the database connection.
                        db.__del__()
                        # Return to the page.
                        return render_template('Join Us.html', level = level, message = message)
            else:
                username_error = "This username not exists"
                # Close the database connection.
                db.__del__()
                # Return to the page.
                return render_template('Join Us.html', level = level, username_error = username_error)
        else:
            # Get the error message of the input value.
            if applicant.username.errors:
                username_error = applicant.username.errors[0]
            else:
                username_error = ""
            if applicant.phonenumber.errors:
                phonenumber_error = applicant.phonenumber.errors[0]
            else:
                phonenumber_error = ""
            if applicant.job.errors:
                job_error = applicant.job.errors[0]
            else:
                job_error = ""
            return render_template('Join Us.html', level = level, username_error = username_error, phonenumber_error = phonenumber_error, job_error = job_error)
    else:
        return render_template('Join Us.html', level = level)

# The function for login.
@app.route('/Login', methods = ['GET', 'POST'])
def Login():
    # Create a instance of login form.
    User = UserLoginForm(request.form)
    Admin = AdminLoginForm(request.form)
    # Create the login object.
    global user_admin
    # Change the level.
    global level
    # Get the users login time.
    global logintime
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if User.validate() and User.User.data:
            # Create an instance for database.
            db = DatabaseOperations()
            # Indicate whether the user is exist or not.
            if db.LoginAsUser(User.Username.data, User.Password.data):
                # Get the users' level.
                level = 0
                # Get the users login time.
                logintime = time.time()
                # Get the id of the user.
                ID = db.GetUserId(User.Username.data)
                # Make the login
                user_admin = UserLogin(ID, User.Username.data, User.Password.data)
                # Login.
                login_user(user_admin)
                # Close the database connection.
                db.__del__()
                # Return to the homepage.
                return redirect('.')
            else:
                # Close the database connection.
                db.__del__()
                # Give the error message.
                message = "Please input the correct username or password"
                # Return the error to the page.
                return render_template('Login.html', level = level, message = message)
        elif Admin.validate() and Admin.Admin.data:
             # Create an instance for database.
            db = DatabaseOperations()
            # Indicate whether the admin is exist or not.
            if db.LoginAsAdmin(Admin.Username.data, Admin.Password.data):
                # Change the level.
                level = 1
                # Get the users login time.
                logintime = time.time()
                # Get the id of the user.
                ID = db.GetUserId(User.Username.data)
                # Make the login
                user_admin = UserLogin(ID, Admin.Username.data, Admin.Password.data)
                # Login.
                login_user(user_admin)
                # Close the database connection.
                db.__del__()
                # Return to the homepage.
                return redirect('.')
            else:
                # Close the database connection.
                db.__del__()
                # Give the error message.
                message = "Please input the correct administrators name or password"
                # Return the error to the page.
                return render_template('Login.html', level = level, message = message)
        else:
            # Get the error message of the input value.
            if Admin.Username.errors:
                username_error = Admin.Username.errors[0]
            elif User.Username.errors:
                username_error = User.Username.errors[0]
            else:
                username_error = ''
            if Admin.Password.errors:
                password_error = Admin.Password.errors[0]
            elif User.Password.errors:
                password_error = Admin.Password.errors[0]
            else:
                password_error = ''
            # Return the error to the page.
            return render_template('Login.html', level = level, username_error = username_error, password_error = password_error)
    else:
        return render_template('Login.html', level = level)

# The function for QR-code.
@app.route('/QR-Code', methods = ['GET', 'POST'])
@login_required
def QR_Code():
    # Get the order and training.
    global order
    global training
    # Create an instance for the form.
    payment = PaymentConfirmForm(request.form)
    # Indicate the payment type.
    if payment.payment.data == "order":
        # Create the database connection.
        db = DatabaseOperations()
        # Do the payment.
        for each in order:
            # Get the time.
            paymentTime = time.time()
            # Insert the order.
            db.DoPaymentForOrder(int(each), str(paymentTime))
        # Kill the order.
        order = ''
        # Kill the training.
        training = ''
        # Close the database
        db.__del__()
        # Return to the page.
        return Homepage("Payment Successful")
    if payment.payment.data == "training":
        # Create the database connection.
        db = DatabaseOperations()
        # Do the payment.
        db.DoPaymentForTraining(int(training[0][0]))
        # Kill the training.
        training = ''
        # Kill the order.
        order = ''
        # Close the database
        db.__del__()
        # Return to the page.
        return Homepage("Payment Successful")

# The function for registration.
@app.route('/Registration', methods = ['GET', 'POST'])
def Registration():
    # Create an instance of registration form.
    register = RegistrationForm(request.form)
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if register.validate():
            # Create an instance for the database.
            db = DatabaseOperations()
            # Indicate whether the username has already exist.
            if db.UserExistTest(register.Username.data):
                # Get the error message.
                error = 'This username has existed'
                # Close the database connection.
                db.__del__()
                # Return the error to the templates.
                return render_template('Registration.html', error = error, level = level)
            else:
                # Get the information
                username = register.Username.data
                password = register.Password.data
                email = register.Email.data
                gender = register.Gender.data
                address = register.Address.data
                phone = register.Phone.data
                # Insert the information to the database and get the 
                db.Registration(username, password, email, gender, address, phone)
                # Close the database connection.
                db.__del__()
                # Get to the login page.
                return redirect('./Login')
        else:
            # Get the error message of the input value.
            if register.Phone.errors:
                phone_error = register.Phone.errors[0]
            else:
                phone_error = ''
            if register.Address.errors:
                address_error = register.Address.errors[0]
            else:
                address_error = ''
            if register.RePassword.errors:
                confirm_error = register.RePassword.errors[0]
            else:
                confirm_error = ''
            if register.Password.errors:
                password_error = register.Password.errors[0]
            else:
                password_error = ''
            if register.Username.errors:
                username_error = register.Username.errors[0]
            else:
                username_error = ''
            if register.Email.errors:
                email_error = register.Email.errors[0]
            else:
                email_error = ''
            # Return the error to the page.
            return render_template('Registration.html', level = level, username_error = username_error, password_error = password_error, confirm_error = confirm_error, email_error = email_error, address_error = address_error, phone_error = phone_error)
    else:
        return render_template('Registration.html', level = level)

# The function for training.
@app.route('/Training', methods = ['GET', 'POST'])
@login_required
def Training():
    # Get the training.
    global training
    # Create an instance of registration form.
    training = TrainingForm(request.form)
    # Indicate whether the form is posted or not.
    if request.method == 'POST':
        # Validate the input value.
        if training.validate():
            # Create an instance for the database.
            db = DatabaseOperations()
            # Indicate whether the username is exist or not.
            if db.UserExistTest(training.username.data):
                # Indicate whether the user is an admin.
                if db.IsAdmin(training.username.data):
                    username_error = "Administrator, please focus on your own work!!!"
                    # Close the database connection.
                    db.__del__()
                    # Return to the page.
                    return render_template('Training.html', level = level, username_error = username_error)
                else:
                    # Indicate whether the username is the user hiself/herself.
                    if training.username.data != user_admin.username:
                        username_error = "Please type your own username"
                        # Close the database connection.
                        db.__del__()
                        # Return to the page.
                        return render_template('Training.html', level = level, username_error = username_error)
                    else:
                        # Insert the value into the table.
                        result = db.UpdateTraining(training.username.data, training.phonenumber.data, training.training_time.data)
                        # Close the database connection.
                        db.__del__()
                        if result:
                            # Get the message.
                            message = "Because all users can only choose one time to take training lesson, and you had booked one before, therefore, we just update your time"
                            # Return to the page.
                            return render_template('Training.html', level = level, message = message)
                        else:
                            # Create the database connection.
                            db = DatabaseOperations()
                            # Get the training ID.
                            training = db.GetTraining()
                            # Close the database connection.
                            db.__del__()
                            # Return to the page.
                            return render_template('QR-Code.html', training = "training")
            else:
                username_error = "This username not exists"
                # Close the database connection.
                db.__del__()
                # Return to the page.
                return render_template('Training.html', level = level, username_error = username_error)
        else:
             # Get the error message of the input value.
            if training.username.errors:
                username_error = training.username.errors[0]
            else:
                username_error = ""
            if training.phonenumber.errors:
                phonenumber_error = training.phonenumber.errors[0]
            else:
                phonenumber_error = ""
            if training.training_time.errors:
                training_time_error = training.training_time.errors[0]
            else:
                training_time_error = ""
            return render_template('Training.html', level = level, username_error = username_error, phonenumber_error = phonenumber_error, training_time_error = training_time_error)      
    else:
        return render_template('Training.html', level = level)

# The function for each flower.
@app.route('/Flower-Details', methods = ['GET', 'POST'])
def Flower_Details(hints = "", message = "", flower = "", quantity = "", totalprice = ""):
    # Create an instance of the form.
    eachFlowerForm = GetFlowerForm(request.form)
    searchFlowerForm = SearchFlowerForm(request.form)
    # Indicate the form.
    if eachFlowerForm.GetInfo.data:
        # Create the database connection.
        db = DatabaseOperations()
        # Get the info of flower.
        flower = db.GetEachFlower(int(eachFlowerForm.GetInfo.data))
        # Close the database connection.
        db.__del__()
    if searchFlowerForm.flower.data != "":
        # Create the database connection.
        db = DatabaseOperations()
        # Get the info of flower.
        flower = db.SearchFlower(searchFlowerForm.flower.data)
        # Indicate whether the flower is exist.
        if flower:
            # Get the comment of the flower.
            comments = db.GetComments(flower[0][1])
            # Back to the page.
            return render_template('Flower-Details.html', level = level, flower = flower, message = message, comment = comments, quantity = quantity, hints = hints, totalprice = totalprice)
        else:
            # Back to the page.
            return Homepage("Sorry the flower you search doesn't exist")
        # Close the database connection.
        db.__del__()
    # Get the comments.
    if flower:
        # Create a database connection.
        db = DatabaseOperations()
        # Get the comment of the flower.
        comments = db.GetComments(flower[0][1])
        # Close the database connection.
        db.__del__()
        # Return the value.
        return render_template('Flower-Details.html', level = level, flower = flower, message = message, comment = comments, quantity = quantity, hints = hints, totalprice = totalprice)
    else:
        return Homepage()

# The function for user information.
@app.route('/User-Info')
@login_required
def User_Info(historyError = "", history = "", trainingError = "", training = "", applicantError = "", applicant = "", message = "", username_error = "", address_error = "", email_error = "", phone_error = "", gender_error = ""):
    # Create the database connection.
    db = DatabaseOperations()
    # Get the values of the admin.
    result = db.GetUserInfo()
    # Close the database.
    db.__del__()
    return render_template('User-Info.html', historyError = historyError, history = history, trainingError = trainingError, training = training, applicantError = applicantError, applicant = applicant, level = level, username = result[0][1], address = result[0][5], email = result[0][3], phone = result[0][6], gender = result[0][4], message = message, username_error = username_error, address_error = address_error, email_error = email_error, phone_error = phone_error, gender_error = gender_error)

# The function for admin information.
@app.route('/Admin-Info', methods = ['GET', 'POST'])
@login_required
def Admin_Info(historyError = "", history = "", trainingError = "", training = "", applicantError = "", applicant = "", accesstimeError = "", accesstime = "", message = "", username_error = "", address_error = "", email_error = "", phone_error = "", gender_error = ""):
    # Create the database connection.
    db = DatabaseOperations()
    # Get the values of the admin.
    result = db.GetAdminInfo()
    # Close the database.
    db.__del__()
    return render_template('Admin-Info.html', historyError = historyError, history = history, trainingError = trainingError, training = training, applicantError = applicantError, applicant = applicant, accesstimeError = accesstimeError, accesstime = accesstime, level = level, username = result[0][1], address = result[0][5], email = result[0][3], phone = result[0][6], gender = result[0][4], message = message, username_error = username_error, address_error = address_error, email_error = email_error, phone_error = phone_error, gender_error = gender_error)

# The function for access time information.
@app.route('/AccessTimeShowing', methods = ['GET', 'POST'])
@login_required
def AccessTimeShowing():
    # Create a variable to occupy the position of the parameter.
    occupy = ""
    # Create the database connection.
    db = DatabaseOperations()
    # Create an instance of the delete access form.
    deleteAccessForm = DeleteAccessTimeForm(request.form)
    # Indicate whether the delete button has pressed or not.
    if deleteAccessForm.Delete_Access.data:
        # Delete the access time.
        for each in deleteAccessForm.Access.data:
            db.DeleteAccessTime(int(each))
    # Get the accesstime.
    accesstime = db.GetAccessTime()
    # Close the database.
    db.__del__()
    # Return the accesstime.
    if accesstime:
        return Admin_Info(occupy, occupy, occupy, occupy, occupy, occupy, occupy, accesstime)
    else:
        accesstimeError = "There is no access time information"
        return Admin_Info(occupy, occupy, occupy, occupy, occupy, occupy, accesstimeError)

# The function for applicant information.
@app.route('/ApplicantShowing', methods = ['GET', 'POST'])
@login_required
def ApplicantShowing():
    # Create a variable to occupy the position of the parameter.
    occupy = ""
    # Create the database connection.
    db = DatabaseOperations()
    # Create an instance of the delete access form.
    deleteApplicantForm = DeleteApplicantForm(request.form)
    # Indicate whether the delete button has pressed or not.
    if deleteApplicantForm.Delete_Applicant.data:
        # Delete the access time.
        for each in deleteApplicantForm.Applicant.data:
            db.DeleteApplicant(int(each))
    # Get the accesstime.
    applicant = db.GetApplicant()
    # Close the database.
    db.__del__()
    # Return the accesstime.
    if level == 0:
        if applicant:
            return User_Info(occupy, occupy, occupy, occupy, occupy, applicant)
        else:
            applicantError = "You have no applicant information"
            return User_Info(occupy, occupy, occupy, occupy, applicantError)
    else:
        if applicant:
            return Admin_Info(occupy, occupy, occupy, occupy, occupy, applicant)
        else:
            applicantError = "There is no applicant information"
            return Admin_Info(occupy, occupy, occupy, occupy, applicantError)

# The function for training information.
@app.route('/TrainingShowing', methods = ['GET', 'POST'])
@login_required
def TrainingShowing():
    # Get training.
    global training
    # Create a variable to occupy the position of the parameter.
    occupy = ""
    # Create the database connection.
    db = DatabaseOperations()
    # Create an instance of the delete training form.
    deleteTrainingForm = DeleteTrainingForm(request.form)
    # Indicate whether the delete button has pressed or not.
    if deleteTrainingForm.Delete_Train.data:
        # Delete the training.
        for each in deleteTrainingForm.Training.data:
            db.DeleteTraining(int(each))
    if deleteTrainingForm.Pay_Train.data and deleteTrainingForm.Training.data:
        # Get the training.
        for each in deleteTrainingForm.Training.data:
            training = db.GetTraining()
        # Close the database connection.
        db.__del__()
        # Return to the page.
        return render_template('QR-Code.html', training = "training")
    # Get the training.
    trainingInfo = db.GetTraining()
    # Close the database.
    db.__del__()
    # Return the training.
    if level == 0:
        if trainingInfo:
            return User_Info(occupy, occupy, occupy, trainingInfo)
        else:
            trainingError = "You have no training has been booked"
            return User_Info(occupy, occupy, trainingError)
    else:
        if trainingInfo:
            return Admin_Info(occupy, occupy, occupy, trainingInfo)
        else:
            trainingError = "There is no training information"
            return Admin_Info(occupy, occupy, trainingError)

# The function for order information.
@app.route('/OrderShowing', methods = ['GET', 'POST'])
@login_required
def OrderShowing():
    # Create a variable to occupy the position of the parameter.
    occupy = ""
    # Create the database connection.
    db = DatabaseOperations()
    # Create an instance of the delete history form.
    deleteHistoryForm = DeleteHistoryOrderForm(request.form)
    # Indicate whether the delete button has pressed or not.
    if deleteHistoryForm.Delete_History.data:
        # Delete the history.
        for each in deleteHistoryForm.History.data:
            db.DeletePaymentOrder(int(each))
    # Get the history.
    history = db.GetPaymentOrder()
    # Close the database.
    db.__del__()
    # Return the training.
    if level == 0:
        if history:
            return User_Info(occupy, history)
        else:
            historyError = "You have no paid order"
            return User_Info(historyError)
    else:
        if history:
            return Admin_Info(occupy, history)
        else:
            historyError = "There is no paid order"
            return Admin_Info(historyError)

# The function for update the info for user or admin.
@app.route('/Update User Admin', methods = ['GET', 'POST'])
@login_required
def Update_User_Admin():
    # Create a variable to occupy the position of the parameter.
    occupy = ""
    # Create an instance of update info of user or admin form.
    update = UpdateUserAdminInfoForm(request.form)
    # Indicate whether the form has posted or not.
    if request.method == 'POST':
        # Indicate the user is an admin or not.
        if level == 1:
            # Indicate the value.
            if update.validate():
                # Create the database connection.
                db = DatabaseOperations()
                # Indicate whether the username has existed.
                if db.AdminExistTest(update.Username.data) and update.Username.data != user_admin.username or db.UserExistTest(update.Username.data) and update.Username.data != user_admin.username:
                    # Get the error message.
                    error = 'This username has existed'
                    # Change the login user name.
                    user_admin.username = update.Username.data
                    # Close the database connection.
                    db.__del__()
                    # Back to the html.
                    return Admin_Info(occupy, occupy, occupy, occupy, occupy, occupy, occupy, occupy, error)
                else:
                    # Update the value.
                    db.UpdateUserAdminInfo(update.Username.data, update.Address.data, update.Email.data, update.Phone.data, update.Gender.data)
                    # Close the database.
                    db.__del__()
                    # Get the edit message.
                    message = "Update successful"
                    # Let the user to login again if the username is edited.
                    if user_admin.username != update.Username.data:
                        return Logout(message)
                    else:
                        # Back to the html.
                        return Admin_Info(occupy, occupy, occupy, occupy, occupy, occupy, occupy, occupy, message)
            else:
                # Get the error message.
                if update.Username.errors:
                    Username_error = update.Username.errors[0]
                else:
                    Username_error = ""
                if update.Address.errors:
                    Address_error = update.Address.errors[0]
                else:
                    Address_error = ""
                if update.Email.errors:
                    Email_error = update.Email.errors[0]
                else:
                    Email_error = ""
                if update.Phone.errors:
                    Phone_error = update.Phone.errors[0]
                else:
                    Phone_error = ""
                if update.Gender.errors:
                    Gender_error = update.Gender.errors[0]
                else:
                    Gender_error = ""
                Message = ""
                # Get back to the html.
                return Admin_Info(occupy, occupy, occupy, occupy, occupy, occupy, occupy, occupy, Message, Username_error, Address_error, Email_error, Phone_error, Gender_error)
        else:
            # Indicate the value.
            if update.validate():
                # Create the database connection.
                db = DatabaseOperations()
                # Indicate whether the username has existed.
                if db.UserExistTest(update.Username.data) and update.Username.data != user_admin.username:
                    # Get the error message.
                    error = 'This username has existed'
                    # Close the database connection.
                    db.__del__()
                    # Back to the html.
                    return User_Info(occupy, occupy, occupy, occupy, occupy, occupy, error)
                else:
                    # Update the value.
                    db.UpdateUserAdminInfo(update.Username.data, update.Address.data, update.Email.data, update.Phone.data, update.Gender.data)
                    # Close the database.
                    db.__del__()
                    # Successful message.
                    message = 'Update successful'
                    # Let the user to login again if the username is edited.
                    if user_admin.username != update.Username.data:
                        return Logout(message)
                    else:
                        # Back to the html.
                        return User_Info(occupy, occupy, occupy, occupy, occupy, occupy, message)
            else:
                # Get the error message.
                if update.Username.errors:
                    Username_error = update.Username.errors[0]
                else:
                    Username_error = ""
                if update.Address.errors:
                    Address_error = update.Address.errors[0]
                else:
                    Address_error = ""
                if update.Email.errors:
                    Email_error = update.Email.errors[0]
                else:
                    Email_error = ""
                if update.Phone.errors:
                    Phone_error = update.Phone.errors[0]
                else:
                    Phone_error = ""
                if update.Gender.errors:
                    Gender_error = update.Gender.errors[0]
                else:
                    Gender_error = ""
                Message = ""
                # Get back to the html.
                return User_Info(occupy, occupy, occupy, occupy, occupy, occupy, Message, Username_error, Address_error, Email_error, Phone_error, Gender_error)  
    else:
        return User_Info()

# The function for logout.
@app.route('/Logout')
@login_required
def Logout(message = ""):
    # Get the logout time.
    global logouttime
    global level
    # Initialize the level.
    level = ''
    # Get the current user.
    username = user_admin.username
    # Get the logout time.
    logouttime = time.time()
    # Get the access time.
    accesstime = logouttime - logintime
    # Create the database connection.
    db = DatabaseOperations()
    # Do the insert operation.
    db.UpdateAccessTime(username,str(logintime),str(logouttime),str(accesstime))
    # Close the database.
    db.__del__()
    # Logout.
    logout_user()
    # Let the user to login again
    if message:
        return redirect('./Login')
    # Redirect to homepage.
    return redirect('.')