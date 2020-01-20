import pymongo
import re
from datetime import datetime
from datetime import date

# Create Database
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['my_db']

# Create Collection (Table)
myCol = mydb["emp_details"]
myColSal = mydb["emp_salaries"]
myColHoliday = mydb['emp_holidays']
myColAttendance = mydb['emp_attendance']
myColFunctions = mydb['emp_functions']


def addEmp(empId, empName, empAdd, empStatus, empDob, empEmail, empContact):
    empDob = str(empDob)
    mydict = {'id':empId, 'emp_name': empName.capitalize(), 'emp_add': empAdd.capitalize(), 'emp_status': empStatus.capitalize(), 'emp_dob': empDob, 'emp_email': empEmail, 'emp_contact': empContact ,'is_deleted':False}
    x = myCol.insert_one(mydict)

    if bool(x):
        print("1 document inserted.\n")
    else:
        print("0 document inserted.\n")


def showEmp():
    # for x in myCol.find({},{'_id':0,'id':1,'empname':1,'empadd':1,'empstatus':1,'empdob':1,'empemail':1,'empcontact':1}):
    for x in myCol.find({},{'_id':0}):           
        if x['is_deleted'] == False:
            for i in x:
                print(i.capitalize(), ':', x[i])
            print('\n')
    print('-'*30)
    
    for x in myCol.find({},{'_id':0}):
        if x['is_deleted']:
            print('Deleted Accounts')
            for i in x:
                print(i.capitalize(), ':', x[i])
            print('\n')
            print('-'*30)

def deleteEmp(empEmail):
    i = None
    for j in myCol.find({'emp_email': empEmail.lower()},{'_id':0,'emp_email':1,'is_deleted':1}):
        i=j
        if i['is_deleted']:
            print("Employee details already Deleted... :(\n")
        else:
            oldValue = {'emp_email':empEmail}
            newValue = {'$set': {'is_deleted': True}}
            x = myCol.update_one(oldValue, newValue)
            print(x.modified_count, " document deleted.\n")
    if i == None:
        print("Email not found... :(")
    

    # for x in myColSal.find({'empid': empId},{'_id':0}):
    #     op = myColSal.delete_one(x)
    #     print(op.deleted_count," document deleted from Salary Collection.")

    # for x in myColAttendance.find({'empid': empId},{'_id':0}):
    #     op = myColAttendance.delete_one(x)
    #     print(op.deleted_count," document deleted from Attendance Collection.")

    # x = myCol.delete_one(myquery)
    # print(x.deleted_count," document deleted.")


def editempName(empName, empNewName):
    myquery = {'emp_name': empName.capitalize()}
    newvalue = {'$set':{'emp_name':empNewName.capitalize()} }
    x = myCol.update_one(myquery, newvalue)
    print(x.modified_count," document updated.\n")
    print('-'*30)


def editempAdd(empName, empNewAdd):
    myquery = {'emp_name': empName.capitalize()}
    newvalue = {'$set': {'emp_add': empNewAdd} }
    x = myCol.update_one(myquery, newvalue)
    print(x.modified_count," document updated.\n")
    print('-'*30)

def editempStatus(empName, empNewStatus):
    myquery = {'emp_name': empName.capitalize()}
    newvalue = {'$set': {'emp_status': empNewStatus.capitalize()} }
    x = myCol.update_one(myquery, newvalue)
    print(x.modified_count," document updated.")
    print('-'*30)

    empId = myCol.find({'emp_name':empName.capitalize()},{'_id':0,'id':1})

    for i in empId:
        colId = i['id']

    myquery = myColSal.find({'emp_id':colId},{'_id':0,'emp_status':1})

    for i in myquery:
        checkStatus = i['emp_status']
        print(checkStatus)

        if checkStatus == 'Fresher':
            oldValue = {'emp_id': colId,'emp_status': "Fresher"}
            newValue ={'$set': {'emp_status': empNewStatus.capitalize()}}
            myColSal.update_one(oldValue, newValue)
        else:
            print("Else")

def editempDob(empName, empNewDob):
    myquery = {'emp_name': empName.capitalize()}
    empNewDob = str(empNewDob)
    newvalue = {'$set': {'emp_dob': empNewDob}}
    x = myCol.update_one(myquery, newvalue)
    print(x.modified_count," document updated.\n")
    print('-'*30)

def editempEmail(empName, empNewEmail):
    myquery = {'emp_name': empName.capitalize()}
    newvalue = {'$set': {'emp_email': empNewEmail}}
    x = myCol.update_one(myquery, newvalue)
    print(x.modified_count," document updated.\n")
    print('-'*30)

def editempContact(empName, empNewContact):
    myquery = {'emp_name': empName.capitalize()}
    newValue = {'$set': {'emp_contact': empNewContact}}
    x = myCol.update_one(myquery, newValue)
    print(x.modified_count," document updated.\n")
    print('-'*30)

def addEmpSalary():
    salFresher = 7000
    salExperience = 20000
    # Calculate Salary for Fresher
    myquery = {'emp_status': 'Fresher'}
    mydoc = myCol.find(myquery)

    for x in mydoc:
        i = None
        count = 0

        for j in myColSal.find():
            i = j

        if i == None:
            mydict = {'emp_id':x['id'],'emp_status':x['emp_status'], 'emp_salary': salFresher}
            myColSal.insert_one(mydict)
            
        else:
            count = 0

            for i in myColSal.find():
                if i["emp_id"] == x["id"]:
                    count = count + 1

            if count == 0:
                mydict = {'emp_id':x['id'],'emp_status':x['emp_status'], 'emp_salary': salFresher}
                myColSal.insert_one(mydict)
                print("Document Inserted.\n")
                  
            else:
                print("Already present")
    
    # /End Calculate Salary for Fresher

    # Calculate Salary for Experience
    myquery = {'emp_status': 'Experience'}
    mydoc = myCol.find(myquery)

    for x in mydoc:
        i = None

        for j in myColSal.find():
            i = j

        if i == None:
            mydict = {'emp_id':x['id'],'emp_status':x['emp_status'], 'emp_salary': salExperience}
            myColSal.insert_one(mydict)   
        else:
            count = 0

            for i in myColSal.find():
                if i["emp_id"] == x["id"]:
                    count = count + 1

            if count == 0:
                mydict = {'emp_id':x['id'],'emp_status':x['emp_status'], 'emp_salary': salExperience}
                myColSal.insert_one(mydict)
            else:
                print("Already present")

            if j['emp_status'] == 'Experience':
                oldValue = {'emp_status': 'Experience'}
                newValue = {'$set': {'emp_salary': salExperience}}
                myColSal.update_one(oldValue, newValue)    
    # /End Calculate Salary for Experience
    print('\n')


def showEmpSal():
    
    for i in myCol.find():
        if i['is_deleted'] == False:
            for x in myColSal.find({'emp_id':i['id']},{'_id':0}):

                for i in x:
                    print(i, ':', x[i])
                print('\n')
    print('-'*30)
    for i in myCol.find():
        if i['is_deleted']:
            print('Deleted Employee Salary Details')
            for x in myColSal.find({'emp_id':i['id']},{'_id':0}):

                for i in x:
                    print(i, ':', x[i])
                print('\n')
            print('-'*30)


def holiday(holiDate, title):
    mydict = {'holiday':str(holiDate),'title':title.capitalize()}
    x = myColHoliday.insert_one(mydict)
    if bool(x):
        print("1 document inserted.\n")
        print('-'*30)
    else:
        print("0 document inserted.\n")
        print('-'*30)


def showHoliday():
    i = None
    for j in myColHoliday.find({},{'_id':0}):
        i = j
    if i == None:
        print("No Record found... :(\n")
        print('-'*30)
    else:
        for x in myColHoliday.find({},{'_id':0}):

            for i in x:
                print(i.capitalize(), ':', x[i])
            print("\n")
        print('-'*30)


def monthHoliday(monthNo):
    for x in myColHoliday.find({},{'_id':0}).sort("holiday"):

        y = datetime.strptime(x['holiday'], '%Y-%m-%d').strftime('%m')
        
        if monthNo == int(y):
            for i in x:
                print(i.capitalize(), ':', x[i])
            print("\n")
        else:
            print("Invalid Month... :(")


def addAttendance(empName,attDate,attendance):
    empnm = myCol.find({'emp_name': empName.capitalize()},{'_id':0,'id':1})

    for x in empnm:
        i = None

        for j in myColAttendance.find():
            i = j

        if i == None:
            mydict = {'emp_id': x['id'], 'attendancedate': str(attDate), 'attendance': attendance}
            x = myColAttendance.insert_one(mydict)

            if bool(x) == True:
                print("1 document inserted.")
            else:
                print("0 document inseted.")
        else:
            count = 0
            
            for i in myColAttendance.find({'empid':x['id'],'attendancedate': str(attDate)},{'_id':0, 'attendancedate':1}):
        
                if i != None:
                    count = count + 1
            
            if count == 0:
                mydict = {'emp_id': x['id'], 'attendancedate': str(attDate), 'attendance': attendance}
                x = myColAttendance.insert_one(mydict)
                
                if bool(x) == True:
                    print("1 document inserted.\n")
                else:
                    print("0 document inseted.\n")
            else:
                print("Already Present")


def showAllAttendance():
    i = None
    for x in myColAttendance.find({},{'_id':0}):
        i = x

    if i == None:
        print("No Record found... :(\n")
        print('-'*30)
    else:
        for x in myCol.find({},{'_id':0}):
            if x['is_deleted'] == False:

                for i in myColAttendance.find({'emp_id':x['id']},{'_id':0}):
                    print('emp_name:',x['emp_name'],)
                    
                    for j in i:
                        print(j,':',i[j])
                    print("\n")
        print('-'*30)
        for x in myCol.find({},{'_id':0}):
            if x['is_deleted']:
                i = None
                for j in myColAttendance.find({'emp_id':x['id']},{'_id':0}):
                    i = j

                if i == None:
                    pass
                else:

                    print('Deleted Employee Attendance Details')
                    for i in myColAttendance.find({'emp_id':x['id']},{'_id':0}):
                        print('emp_name:',x['emp_name'],)
                        
                        for j in i:
                            print(j,':',i[j])
                        print("\n")
                    print('-'*30)

def showAttendance(empName):
    i = None
    for x in myColAttendance.find({},{'_id':0}):
        i = x
    if i == None:
        print("No Record found.. :(\n")
        print('-'*30)
    else:
        totalP = 0
        totalA = 0
        
        for x in myCol.find({'emp_name': empName.capitalize()},{'_id':0}):

            i = None
            for j in myColAttendance.find({'emp_id':x['id']},{'_id':0}):
                i = j

            if i == None:
                print("No Record found... :(\n")
                print('-'*30)

            else:
                print('\n')
                for i in myColAttendance.find({'emp_id':x['id']},{'_id':0}):

                    
                    print('emp_name:',x['emp_name'],)
                    
                    for j in i:
                        print(j,':',i[j])
                    print("\n")

                    if i['attendance'] == 1:
                        totalP = totalP + 1
                    else:
                        totalA = totalA + 1

                print("Total Present Attendance: ",totalP)
                print("Total Absent Attendance: ",totalA)
                print('\n')
                print('-'*30)


def functionData(functionDate, funcName):
    i = None
    
    for x in myColFunctions.find():
        i = x

    if i == None:
        mydict = {'functiondate': str(functionDate), 'functionname': funcName}
        myColFunctions.insert_one(mydict)
    else:
        count = 0
        
        for i in myColFunctions.find({'functiondate': str(functionDate)},{'_id':0}):
        
            if i != None:
                count = count + 1
        
        if count == None:
            mydict = {'functiondate': str(functionDate), 'functionname': funcName}
            myColFunctions.insert_one(mydict)
        else:
            print('Already Present')
            print('\n')


def showFunctions():
    i = None
    for j in myColFunctions.find({},{'_id':0}):
        i = j

    if i == None:
        print('No Record found... :(\n')
        print('-'*30)
    else:
        for x in myColFunctions.find({},{'_id':0}):

            for i in x:
                print(i.capitalize(), ':', x[i])
            print('\n')


def checkEmail(empEmail):
    checkEmail = myCol.find({},{'_id':0})
    for i in checkEmail:
        
        if i['emp_email'] == empEmail:
            return 0
    return empEmail
    

def checkEmailValidation(empEmail):
    result = re.findall(r"[-a-zA-Z0-9.`?{}]+@\w+\D\.\w*",empEmail)
    return result


def checkContactLen(empContact):
    if len(empContact) < 10 :
        return 0
    elif len(empContact) > 11:
        return 0
    else:
        return empContact 

def checkEmpName(empName):
    i = None
    for j in myCol.find({'emp_name': empName.capitalize()},{'_id':0}):
        i = j
    if i == None:
        return 0
    else:
        return empName
        

# def checkId(empId):
#     checkId = myCol.find({'id':empId},{'id_':0})
#     for i in checkId:
#         if i != None:
#             return i
#         else:
#             pass

while True:
    print('1. Add Employee')
    print("2. Delete Employee")
    print("3. Edit Employee Details")
    print("4. Dispaly all Employee Details")
    print("5. Salary Management")
    print("6. Attendance Management")
    print("7. Function Management")
    print("8. Holiday Management")
    print("0. Exit")
    ch = int(input("Enter your choice: "))
    print('-'*30)
    
    # Add Employee
    if ch == 1:
        i = None
        empId = 0
        for x in myCol.find():
            i = x
        if i == None:
            empId = 1
        else:
            count = 0
            for i in myCol.find({},{'_id':0,'id':1}).sort('id',-1).limit(1):
                empId = 'global'
                empId = i['id']
            empId = empId + 1

        empName = input("Enter Employee name: ")
        empAdd = input("Enter Emplyee address: ")
        empStatus = input("Enter Employee status (Fresher or Experience): ")
        dates = input("Enter Employee DoB (DD/mm/YYYY): ")
        
        # Try for DoB
        try:
            empDob = datetime.strptime(dates, '%d/%m/%Y').date() # date.fromisoformat(dates)
        # Exception
        except ValueError:
            print("Invalid Date, Please try again!!! :( \n")
            dates = input("Enter Employee DoB (DD/mm/YYYY): ")
            # Try
            try:
                empDob = datetime.strptime(dates, '%d/%m/%Y').date() # date.fromisoformat(dates)
            # Exception
            except ValueError:
                print("Invalid Date, Please try again!!! :( \n")
                break  
        # /end Try for DoB         

        empEmail = input("Enter Employee email: ")
        empEmail = checkEmail(empEmail)
        
        if empEmail == 0:
            print('Already Present')
            print('Please Try again... :(\n')
            print('-'*30)

            empEmail = input("Enter Employee email: ")
            empEmail = checkEmail(empEmail)
        
            if empEmail == 0:
                print('Already Present')
                print('Please Try again... :(\n')
                print('-'*30)
            else:
                empEmail = checkEmailValidation(str(empEmail))
                if empEmail:
                    empEmail = ''.join(empEmail)
                else:
                    print("Invalid Email Format.")
                    print("Please try again... :(\n")
                    print('-'*30)
                    empEmail = input("Enter Employee email: ")
                    empEmail = checkEmail(empEmail)
                
                    if empEmail == 0:
                        print('Already Present')
                        print('Please Try again... :(\n')
                        print('-'*30)
                    else:
                        empEmail = checkEmailValidation(str(empEmail))
                        if empEmail:
                            empEmail = ''.join(empEmail)
                        else:
                            print("Invalid Email Format... :(\n")
                            print('-'*30)
                            break

        else:
            empEmail = checkEmailValidation(str(empEmail))

            if empEmail:
                empEmail = ''.join(empEmail)
                empEmail = checkEmail(empEmail)

            else:
                print("Invalid Email Format.")
                print("Please try again... :(\n")
                print('-'*30)
                empEmail = input("Enter Employee email: ")
                empEmail = checkEmail(empEmail)
            
                if empEmail == 0:
                    print('Already Present')
                    print('Please Try again... :(\n')
                    print('-'*30)
                else:
                    empEmail = checkEmailValidation(str(empEmail))
                    if empEmail:
                        empEmail = ''.join(empEmail)
                    else:
                        print("Invalid Email Format... :(\n")
                        print('-'*30)
                        break

        # Try for Contact
        try:
            empContact = int(input("Enter Employee mobile no: "))
            empContact = checkContactLen(str(empContact))
            if empContact == 0:
                print("Invalid length of contact, Please enter 10 digit contact number!!! :(\n")
                print('-'*30)
                empContact = int(input("Enter Employee mobile no: "))
                empContact = checkContactLen(str(empContact))
                if empContact == 0:
                    print("Invalid length of contact, Please enter 10 digit contact number!!! :(\n")
                    print('-'*30)
                    break
            
        # Except
        except ValueError:
            print("Invalid Mobile number, Please try again!!! :( \n")
            # Try
            try:
                empContact = int(input("Enter Employee mobile no: "))
                empContact = int(input("Enter Employee mobile no: "))
                empContact = checkContactLen(str(empContact))
                if empContact == 0:
                    print("Invalid length of contact, Please enter 10 digit contact number!!! :(\n")
                    print('-'*30)
                    empContact = int(input("Enter Employee mobile no: "))
                    empContact = checkContactLen(str(empContact))
                    if empContact == 0:
                        print("Invalid length of contact, Please enter 10 digit contact number!!! :(\n")
                        print('-'*30)
                        break
                    
            # Except
            except ValueError:
                print("Invalid Mobile number, Please try againg!!! :( \n")
                break
        # /end Try for Contact
        addEmp(empId, empName, empAdd, empStatus, empDob, empEmail, empContact)
        print('-'*30)
    # /End Add Employee

    # Delete All Records
    elif ch == 2:
        empEmail = input("Enter employee email for delete record: ")
        deleteEmp(empEmail)
        print('-'*30)
    # /End Delete All Records

    # Update Employee Details
    elif ch == 3:
        print("0. No need to update record.")
        print("1. Need to update record.")
        ch =int(input("Need to Update employeee name? "))
        
        if ch == 1:
            empName = input("Enter employee name for update record: ")
            empName = checkEmpName(empName)
            if empName == 0:
                print("Employee name not found, Please try again.. :(\n")
                print('-'*30)
                empName = input("Enter employee name for update record: ")
                empName = checkEmpName(empName)
                if empName == 0:
                    print("Employee name not found, Please try again.. :(\n")
                    print('-'*30)
                    break
            empNewName = input("Enter employee new name: ")
            data = editempName(empName, empNewName)
        
        elif ch == 0:
            ch = int(input("Need to update employee addresss? "))
            
            if ch == 1:
                empName = input("Enter employee name for update record: ")
                empName = checkEmpName(empName)
                if empName == 0:
                    print("Employee name not found, Please try again.. :(\n")
                    print('-'*30)
                    empName = input("Enter employee name for update record: ")
                    empName = checkEmpName(empName)
                    if empName == 0:
                        print("Employee name not found, Please try again.. :(\n")
                        print('-'*30)
                        break
                empNewAdd = input("Enter employee new address: ")
                editempAdd(empName, empNewAdd)
            
            elif ch == 0:
                ch = int(input("Need to update employee status? "))
                
                if ch == 1:
                    empName = input("Enter employee name for update record: ")
                    empName = checkEmpName(empName)
                    if empName == 0:
                        print("Employee name not found, Please try again.. :(\n")
                        print('-'*30)
                        empName = input("Enter employee name for update record: ")
                        empName = checkEmpName(empName)
                        if empName == 0:
                            print("Employee name not found, Please try again.. :(\n")
                            print('-'*30)
                            break
                        else:
                            empNewStatus = input("Enter employee new status (Fresher or Experience): ")
                            editempStatus(empName, empNewStatus)
                    else:
                        empNewStatus = input("Enter employee new status (Fresher or Experience): ")
                        editempStatus(empName, empNewStatus)
                elif ch == 0:
                    ch = int(input("Need to  update employee d.o.b.? "))
                    
                    if ch == 1:
                        empName = input("Enter employee name for update record: ")
                        empName = checkEmpName(empName)
                        if empName == 0:
                            print("Employee name not found, Please try again.. :(\n")
                            print('-'*30)
                            empName = input("Enter employee name for update record: ")
                            empName = checkEmpName(empName)
                            if empName == 0:
                                print("Employee name not found, Please try again.. :(\n")
                                print('-'*30)
                                break
                        dob = input("Enter employee dob (DD/mm/YYYY):")
                        empNewDob = datetime.strptime(dob, '%d/%m/%Y').date()

                        # Try
                        try:
                            empNewDob = datetime.strptime(dob, '%d/%m/%Y').date() # date.fromisoformat(dates)
                            editempDob(empName, empNewDob)
                        # Exception
                        except ValueError:
                            print("Invalid Date, Please try again!!! :( \n")
                            print('-'*30)
                            dob = input("Enter employee dob (DD/mm/YYYY):")

                            # Try
                            try:
                                empNewDob = datetime.strptime(dob, '%d/%m/%Y').date() # date.fromisoformat(dates)
                                editempDob(empName, empNewDob)
                            # Exception
                            except ValueError:
                                print("Invalid Date, Please try again!!! :( \n")
                                break 
                        # editempDob(empName, empNewDob)
                    
                    elif ch == 0:
                        ch = int(input("Need to update employee email? "))
                        
                        if ch == 1:
                            empName = input("Enter employee name for update record: ")
                            empName = checkEmpName(empName)
                            if empName == 0:
                                print("Employee name not found, Please try again.. :(\n")
                                print('-'*30)
                                empName = input("Enter employee name for update record: ")
                                empName = checkEmpName(empName)
                                if empName == 0:
                                    print("Employee name not found, Please try again.. :(\n")
                                    print('-'*30)
                                    break
                            empNewEmail = input("Enter employee new email: ")
                            empNewEmail = checkEmail(empNewEmail)
                
                            if empNewEmail == 0:
                                print('Already Present')
                                print('Please Try again... :(\n')
                                print('-'*30)
                                empNewEmail = input("Enter employee new email: ")
                                empNewEmail = checkEmail(empNewEmail)
                    
                                if empNewEmail == 0:
                                    print('Already Present')
                                    print('Please Try again... :(\n')
                                    print('-'*30)
                                else:
                                    empNewEmail = checkEmailValidation(str(empNewEmail))
                                    if empNewEmail:
                                        empNewEmail = ''.join(empNewEmail)
                                        editempEmail(empName, empNewEmail)
                                    else:
                                        print("Invalid Email Format... :(\n")
                                        print('-'*30)
                                        break
                            else:
                                empNewEmail = checkEmailValidation(str(empNewEmail))
                                if empNewEmail:
                                    empNewEmail = ''.join(empNewEmail)
                                    editempEmail(empName, empNewEmail)
                                else:
                                    print("Invalid Email Format... :(\n")
                                    print('-'*30)
                                    break
                            # editempEmail(empName, empNewEmail)
                        elif ch == 0:
                            ch = int(input("Need to update employee contact? "))
                            if ch == 1:
                                empName = input("Enter employee name for update record: ")
                                empName = checkEmpName(empName)
                                if empName == 0:
                                    print("Employee name not found, Please try again.. :(\n")
                                    print('-'*30)
                                try:
                                    empNewContact = int(input("Enter Employee mobile no: "))
                                    empNewContact = checkContactLen(str(empNewContact))
                                    if empNewContact == 0:
                                        print("Invalid length of contact, Please enter 10 digit contact number!!! :(\n")
                                        print('-'*30)
                                        empNewContact = int(input("Enter Employee mobile no: "))
                                        empNewContact = checkContactLen(str(empNewContact))
                                        if empNewContact == 0:
                                            print("Invalid length of contact, Please enter 10 digit contact number!!! :(\n")
                                            print('-'*30)
                                            break
                                        else:
                                            editempContact(empName, empNewContact)
                                    else:
                                        editempContact(empName, empNewContact)
                                # Except
                                except ValueError:
                                    print("Invalid Mobile number, Please try again!!! :( \n")
                            else:
                                print("\n")
                                print('-'*30)
                                pass
                        else:
                            print("Invalid Input... :(\n")
                            print('-'*30)
        
                    else:
                        print("Invalid Input... :(\n")
                        print('-'*30)
                    
                else:
                    print("Invalid Input... :(\n")
                    print('-'*30)
        
            else:
                print("Invalid Input... :(\n")
                print('-'*30)
        
        else:
            print("Invalid Input... :(\n")
            print('-'*30)
    # /End Update Employee Details

    # Display All Employees
    elif ch == 4:
        showEmp()
        
    # /End Display All Employees

    # Salary Management
    elif ch == 5:
        print("1. Add Salary (Base on Month)")
        print("2. Display Salary with Employee Details")
        ch = int(input("Enter your chioce: "))
        print('-'*30)
        
        if ch == 1:
            addEmpSalary()
            print('-'*30)
        elif ch == 2:
            showEmpSal()
        else:
            print("Invalid Input... :(")
    # /End Salary Management

    # Attendance Management
    elif ch == 6:
        print("1. Add Employee Attendance")
        print("2. Display All Employee attendance")
        print("3. Display Particular employee attendance")
        ch = int(input("Enter your choice: "))
        print('-'*30)
        
        if ch == 1:
            empName = input("Enter employee name for add attendance: ")
            empName = checkEmpName(empName)
            if empName == 0:
                print("Employee name not found, Please try again.. :(\n")
                print('-'*30)
                empName = input("Enter employee name for add attendance: ")
                empName = checkEmpName(empName)
                if empName == 0:
                    print("Employee name not found, Please try again.. :(\n")
                    print('-'*30)
                else:
                    print("1. Auto select Today Date: ")
                    print("2. Enter Manual Date: ")
                    ch = int(input("Enter your choice: "))
                    print('-'*30)

                    if ch == 1:
                        attDate = datetime.now().date()
                        attendance = int(input("Enter attendance 0-Absent or 1-Present: "))
                        attendance = abs(attendance)
                
                        if attendance < 2:
                            addAttendance(empName,attDate,attendance)
                        else:
                            print("Invalaid Input... :(\n")
            else:
                print("1. Auto select Today Date: ")
                print("2. Enter Manual Date: ")
                ch = int(input("Enter your choice: "))
                print('-'*30)

                if ch == 1:
                    attDate = datetime.now().date()
                    attendance = int(input("Enter attendance 0-Absent or 1-Present: "))
                    attendance = abs(attendance)
            
                    if attendance < 2:
                        addAttendance(empName,attDate,attendance)
                    else:
                        print("Invalaid Input... :(\n")
        
                elif ch == 2:
                    date = input("Enter a previous date(DD/mm/YYYY): ")
                    # Try
                    try:
                        attDate = datetime.strptime(date, '%d/%m/%Y').date()
                        curDate = datetime.now().date()
                
                        if curDate < attDate :
                            print("You are insert future's date...! Please try again... :(\n")
                            print('-'*30)

                            date = input("Enter a previous date(DD/mm/YYYY): ")
                            # Try
                            try:
                                attDate = datetime.strptime(date, '%d/%m/%Y').date()
                                curDate = datetime.now().date()
                        
                                if curDate < attDate :
                                    print("You are insert future's date...! Please try again... :(\n")
                                    print('-'*30)
                                    break
                                else:
                                    attendance = int(input("Enter attendance 0-Absent or 1-Present: "))
                                    attendance = abs(attendance)
                        
                                    if attendance < 2:
                                        addAttendance(empName,attDate,attendance)
                                    else:
                                        print("Invalaid Input... :(\n")
                                        print('-'*30)
                            # Exception
                            except ValueError:
                                print("Invalid Date, Please try again!!! :( \n")
                                print('-'*30)

                        else:
                            attendance = int(input("Enter attendance 0-Absent or 1-Present: "))
                            attendance = abs(attendance)
                
                            if attendance < 2:
                                addAttendance(empName,attDate,attendance)
                            else:
                                print("Invalaid Input... :(\n")
                                print('-'*30)
                    # Exception
                    except ValueError:
                        print("Invalid Date, Please try again!!! :( \n")
                        print('-'*30)
                        date = input("Enter a previous date(DD/mm/YYYY): ")
                        # Try
                        try:
                            attDate = datetime.strptime(date, '%d/%m/%Y').date()
                            curDate = datetime.now().date()
                            if curDate < attDate :
                                print("You are insert future's date...! Please try again... :(\n")
                                print('-'*30)
                                break
                            else:
                                attendance = int(input("Enter attendance 0-Absent or 1-Present: "))
                                attendance = abs(attendance)
                    
                                if attendance < 2:
                                    addAttendance(empName,attDate,attendance)
                                else:
                                    print("Invalaid Input... :(\n")
                                    print('-'*30)
                        # Exception
                        except ValueError:
                            print("Invalid Date, Please try again!!! :( \n")
                            print('-'*30)
                            break
        
                else:
                    print("Invalid Input... :(")
                print('\n')
                print('-'*30)
        
        elif ch == 2:
            showAllAttendance()

        elif ch == 3:
            empName = input("Enter employee name: ")
            empName = checkEmpName(empName)
            if empName == 0:
                print("Employee name not found, Please try again.. :(\n")
                print('-'*30)
                empName = input("Enter employee name: ")
                empName = checkEmpName(empName)
                if empName == 0:
                    print("Employee name not found, Please try again.. :(\n")
                    print('-'*30)
                    break
                else:
                    showAttendance(empName)
            else:
                showAttendance(empName)
            
        else:
            print("Invalid Input... :(\n")
            print('-'*30)
    # /End Attendance Management

    # Function Management
    elif ch == 7:
        print("1. Add Function Date and Name")
        print("2. List of all Function")
        ch = int(input("Enter your choice: "))
        print('-'*30)
        
        if ch == 1:
            date = input("Enter date (DD/mm/YYYY): ")
            
            # Try
            try:
                functionDate = datetime.strptime(date,"%d/%m/%Y").date() # date.fromisoformat(dates)
                # funcName = input("Enter name of Function: ")

                curDate = datetime.now().date()
                curYear = curDate.strftime("%Y")
                functionYear = functionDate.strftime("%Y")

                if functionYear == curYear:
                    if functionDate < curDate:
                        print('You are input Past Date. You does not set Function in Past.')
                        print('Please try again!!! :(\n')
                        print('-'*30)
                    else:    
                        funcName = input("Enter name of Function: ")
                        functionData(functionDate, funcName)
                else:
                    print("\nPlease insert present year... :(")
                print('-'*30)
            # Exception
            except ValueError:
                print("Invalid Date, Please try again!!! :( \n")
                print('-'*30)
                date = input("Enter date (DD/mm/YYYY): ")
            
                # Try
                try:
                    functionDate = datetime.strptime(date,"%d/%m/%Y").date() # date.fromisoformat(dates)
                    # funcName = input("Enter name of Function: ")

                    curDate = datetime.now().date()
                    curYear = curDate.strftime("%Y")
                    functionYear = functionDate.strftime("%Y")

                    if functionYear == curYear:
                        if functionDate < curDate:
                            print('You are input Past Date. You does not set Function in Past.')
                            print('Please try again!!! :(\n')
                            prnt('-'*30)
                        else:
                            funcName = input("Enter name of Function: ") 
                            functionData(functionDate, funcName)
                    else:
                        print("\nPlease insert present year... :(")
                    print('-'*30)
                # Exception
                except ValueError:
                    print("Invalid Date, Please try again!!! :( \n")
                    break 

            

        elif ch == 2:
            showFunctions()
            
        else:
            print("Invalid Input... :(")
    # /End Fnction Management

    # Holiday Management
    elif ch == 8:
        print("1. Add Holiday (date, title)")
        print("2. Display holiday with particular month")
        print("3. Display all holidays")
        ch = int(input("Enter your choice: "))
        print('-'*30)
        
        if ch == 1 :
            date = input("Enter date (DD/mm/YYYY): ")

            # Try
            try:
                holiDate = datetime.strptime(date,"%d/%m/%Y").date() # date.fromisoformat(dates)
                
                curDate = datetime.now().date()
                curYear = curDate.strftime("%Y")
                holiYear = holiDate.strftime("%Y")
                
                if holiYear == curYear:
                    # print("\nPresent Year")
                    title = input("Enter title of holiday: ")
                    holiday(holiDate, title)
                else:
                    print("\nPlease insert present year... :(\n")
                    print('-'*30)
                    date = input("Enter date (DD/mm/YYYY): ")

                    # Try
                    try:
                        holiDate = datetime.strptime(date,"%d/%m/%Y").date() # date.fromisoformat(dates)
                        

                        curDate = datetime.now().date()
                        curYear = curDate.strftime("%Y")
                        holiYear = holiDate.strftime("%Y")
                        
                        if holiYear == curYear:
                            # print("\nPresent Year")
                            title = input("Enter title of holiday: ")
                            holiday(holiDate, title)
                        else:
                            print("\nPlease insert present year... :(\n")
                            print('-'*30)
                    # Exception
                    except ValueError:
                        print("Invalid Date, Please try again!!! :( \n")
                        print('-'*30)
                        break
            # Exception
            except ValueError:
                print("Invalid Date, Please try again!!! :( \n")
                print('-'*30)
                date = input("Enter date (DD/mm/YYYY): ")

                # Try
                try:
                    holiDate = datetime.strptime(date,"%d/%m/%Y").date() # date.fromisoformat(dates)
                    

                    curDate = datetime.now().date()
                    curYear = curDate.strftime("%Y")
                    holiYear = holiDate.strftime("%Y")
                    
                    if holiYear == curYear:
                        # print("\nPresent Year")
                        title = input("Enter title of holiday: ")
                        holiday(holiDate, title)
                    else:
                        print("\nPlease insert present year... :(\n")
                        print('-'*30)
                # Exception
                except ValueError:
                    print("Invalid Date, Please try again!!! :( \n")
                    print('-'*30)
                    break
            

        elif ch == 2:
            monthNo = int(input("Enter month number: "))
            
            if monthNo > 0 and monthNo <= 12:
                monthHoliday(monthNo)
            else:
                print("Invalide Input... :(")
            print('-'*30)

        elif ch == 3:
            showHoliday()
            
        else:
            print("Invalid Input... :(")
    # /End Holiday Management

    elif ch == 0:
        break
    else:
        print("Invalid Input... :(")
        print('-'*30)
        break