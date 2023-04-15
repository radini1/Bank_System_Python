from tkinter import *
import os 
from PIL import Image, ImageTk

master = Tk()
master.title('Banking System')

#Functions part 
def finish_registration():
	name = temp_name.get()  #store the name 
	age = temp_age.get()  #store the age 
	gender = temp_gender.get()  #store the gender
	password = temp_password.get()  #store the password
	all_accounts = os.listdir()

	if name == "" or age == "" or gender == "" or password == "":
		notif.config(fg="red", text='All fields required')
		return

	# check if the account already exist or not (by checking the person's name).
	for check_name in all_accounts:
		if check_name == name:
			notif.config(fg="red", text="acccount already exist.")
			return
		else:
			new_file = open(name, 'w')
			new_file.write(name+'\n')
			new_file.write(age+'\n')
			new_file.write(gender+'\n')
			new_file.write(password+'\n')
			new_file.write('0')
			new_file.close()
			notif.config(fg="blue", text="Account's been created successfuly.")

def register():
	#Variables
	global temp_name
	global temp_age
	global temp_gender
	global temp_password
	global notif
	temp_name = StringVar()
	temp_age = StringVar()
	temp_gender = StringVar()
	temp_password = StringVar()

	register_screen = Toplevel(master)
	register_screen.title('register')

	Label(register_screen, text='Please enter your details below : ', font=('Arial', 12)).grid(row=0, sticky=N, pady=10)
	Label(register_screen, text='FullName : ', font=('Calibri', 12)).grid(row=1, sticky=W)
	Label(register_screen, text='Age : ', font=('Calibri', 12)).grid(row=2, sticky=W)
	Label(register_screen, text='Gender : ', font=('Calibri', 12)).grid(row=3, sticky=W)
	Label(register_screen, text='Password: ', font=('Calibri', 12)).grid(row=4, sticky=W)
	notif = Label(register_screen, font=('Calibri', 12))
	notif.grid(row=6, sticky=N, pady=10)

	Entry(register_screen, textvariable=temp_name).grid(row=1, column=1)
	Entry(register_screen, textvariable=temp_age).grid(row=2, column=1)
	Entry(register_screen, textvariable=temp_gender).grid(row=3, column=1)
	Entry(register_screen, textvariable=temp_password, show="*").grid(row=4, column=1)

	Button(register_screen, text='Register', fg='darkgreen', command=finish_registration, font=('Arial', 12), width=30).grid(row=5, sticky=N, pady=10)

def login_session():
	global login_name
	all_accounts = os.listdir()
	login_name = temp_login_name.get()
	login_password = temp_login_password.get()

	if login_name == "" or login_password == "":
		login_notif.config(fg="red", text='All fields required')
		return

	# checking if user has an account to login or not.
	for name in all_accounts:
		if name == login_name:
			file = open(name, "r")
			file_data = file.read()
			file_data = file_data.split('\n')
			password = file_data[3]
			#Account dashboard
			if login_password == password :
				login_screen.destroy()
				account_dashboard = Toplevel(master)
				account_dashboard.title('Dashboard')
				Label(account_dashboard, text='Account Dashboard', font=('Arial', 14)).grid(row=0, sticky=N, pady=10)
				Label(account_dashboard, text=f'Welcome {name}.', font=('Calibri', 12)).grid(row=1, sticky=N, pady=5)
				Button(account_dashboard,text='Personal details', font=('Calibri', 12), width=28, fg='darkgreen', command=personal_info).grid(row=2, sticky=N, padx=10)
				Button(account_dashboard,text='Deposit', font=('Calibri', 12), width=28, fg='darkgreen', command=deposit).grid(row=3, sticky=N, padx=10)
				Button(account_dashboard,text='Withdraw', font=('Calibri', 12), width=28, fg='darkgreen', command=withdraw).grid(row=4, sticky=N, padx=10)
				Label(account_dashboard).grid(row=5, sticky=N, pady=10)  # just an empty line for space.
				return
			else:
				login_notif.config(fg="red", text='Wrong password.')
				return 

	login_notif.config(fg="red", text='No account found..')

def deposit():
	global amount 
	global deposit_notif
	global current_balance_label 
	amount = StringVar()
	file = open(login_name, "r")  # We define 'login_name' as a global variable so we can use it here.
	file_data = file.read()
	user_details = file_data.split('\n')
	details_balance = user_details[4]

	deposit_screen = Toplevel(master)
	deposit_screen.title('Deposit')

	Label(deposit_screen, text='Deposit', font=('Arial', 14)).grid(row=0, sticky=N, pady=10)
	current_balance_label =  Label(deposit_screen, text=f'Current balance : t{details_balance}', font=('Calibri', 12))
	current_balance_label.grid(row=1, sticky=N)
	Label(deposit_screen, text='Amount', font=('Calibri', 12)).grid(row=2, sticky=W)
	deposit_notif = Label(deposit_screen, font=('Calibri', 12))
	deposit_notif.grid(row=4, sticky=N, pady=5)

	Entry(deposit_screen, textvariable=amount).grid(row=2, column=1)

	Button(deposit_screen, text='finish',font=('Calibri', 12), fg='darkgreen', command=finish_deposit).grid(row=3, sticky=W, pady=5)

def finish_deposit():
	if amount.get() == "":
		deposit_notif.config(fg="red", text='!amount is required!.')
		return 
	if float(amount.get()) <= 0:
		deposit_notif.config(fg="red", text='!please enter a valid currency!.')
		return 	
	file = open(login_name, "r+")
	file_data = file.read()
	details = file_data.split('\n')
	current_balance = details[4]
	updated_balance = float(current_balance)
	updated_balance += float(amount.get())
	file_data = file_data.replace(current_balance, str(updated_balance))  # replacing new amount in the file
	file.seek(0)  # 1-We need to delete previous detail
	file.truncate(0)  #2-delete
	file.write(file_data)
	file.close()

	current_balance_label.config(fg="darkblue", text=f'Current balance : t{current_balance}')
	deposit_notif.config(fg="blue",text='Updated...')

def withdraw():
	global withdraw_amount 
	global withdraw_notif
	global current_balance_label 
	withdraw_amount = StringVar()
	file = open(login_name, "r")  # We define 'login_name' as a global variable so we can use it here.
	file_data = file.read()
	user_details = file_data.split('\n')
	details_balance = user_details[4]

	withdraw_screen = Toplevel(master)
	withdraw_screen.title('Withdraw')

	Label(withdraw_screen, text='Withdraw', font=('Arial', 14)).grid(row=0, sticky=N, pady=10)
	current_balance_label =  Label(withdraw_screen, text=f'Current balance : t{details_balance}', font=('Calibri', 12))
	current_balance_label.grid(row=1, sticky=N)
	Label(withdraw_screen, text='Amount', font=('Calibri', 12)).grid(row=2, sticky=W)
	withdraw_notif = Label(withdraw_screen, font=('Calibri', 12))
	withdraw_notif.grid(row=4, sticky=N, pady=5)

	Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2, column=1)

	Button(withdraw_screen, text='finish',font=('Calibri', 12), fg='darkgreen', command=finish_withdraw).grid(row=3, sticky=W, pady=5)
 
def finish_withdraw():
	if withdraw_amount.get() == "":
		withdraw_notif.config(fg="red", text='!amount is required!.')
		return 
	if float(withdraw_amount.get()) <= 0:
		withdraw_notif.config(fg="red", text='!please enter a valid currency!.')
		return 	
	file = open(login_name, "r+")
	file_data = file.read()
	details = file_data.split('\n')
	current_balance = details[4]
	if float(withdraw_amount.get()) > float(current_balance):
		withdraw_notif.config(fg='red', text='!invalid amount!')
		return
	updated_balance = float(current_balance)
	updated_balance -= float(withdraw_amount.get())
	file_data = file_data.replace(current_balance, str(updated_balance))  # replacing new amount in the file
	file.seek(0)  # 1-We need to delete previous detail
	file.truncate(0)  # 2-delete
	file.write(file_data)
	file.close()

	current_balance_label.config(fg="darkblue", text=f'Current balance : t{current_balance}')
	withdraw_notif.config(fg="blue",text='Updated...')


def personal_info():
	file = open(login_name, "r")
	file_data = file.read()
	user_details = file_data.split('\n')
	detail_name = user_details[0]
	detail_age = user_details[1]
	detail_gender = user_details[2]
	detail_password = user_details[3]

	personal_info_screen = Toplevel(master)
	personal_info_screen.title('personal information')

	Label(personal_info_screen, text='Personal details', font=('Arial', 14)).grid(row=0, sticky=N, pady=10)
	Label(personal_info_screen, text=f'Name : {detail_name}', font=('Arial', 12)).grid(row=1, sticky=W, pady=10)
	Label(personal_info_screen, text=f'Age : {detail_age}', font=('Arial', 12)).grid(row=2, sticky=W, pady=10)
	Label(personal_info_screen, text=f'Gender : {detail_gender}', font=('Arial', 12)).grid(row=3, sticky=W, pady=10)
	Label(personal_info_screen, text=f'Password : {detail_password}', font=('Arial', 12)).grid(row=4, sticky=W, pady=10)


def login():
	#Variables
	global temp_login_name
	global temp_login_password
	global login_notif
	global login_screen
	temp_login_name = StringVar()
	temp_login_password = StringVar()
	login_screen = Toplevel(master)
	login_screen.title('log-in')

	Label(login_screen, text='Log-in to your account : ', font=('Arial', 12)).grid(row=0, sticky=N, pady=10)
	Label(login_screen, text='userame : ', font=('Calibri', 12)).grid(row=1, sticky=W)
	Label(login_screen, text='Password : ', font=('Calibri', 12)).grid(row=2, sticky=W)
	login_notif = Label(login_screen, font=('Calibri', 12))
	login_notif.grid(row=4, sticky=N)

	Entry(login_screen, textvariable=temp_login_name).grid(row=1, column=1)
	Entry(login_screen, textvariable=temp_login_password, show="*").grid(row=2, column=1)

	Button(login_screen, text='Log-in', font=('Arial', 12), width=30, fg='darkgreen', command=login_session).grid(row=3, sticky=N, pady=10)


#images part
img = Image.open("Bank-PO.png")
img = img.resize((350,200))
img = ImageTk.PhotoImage(img)

#Labels part 
Label(master, text='Costum Banking Beta',font=('Arial', 14)).grid(row=0, sticky=N, pady=10)
Label(master, text='The most secure bank system!',font=('Arial', 12)).grid(row=1, sticky=N)
Label(master, image=img).grid(row=2, sticky=N, pady=15)

#Buttons part
Button(master, text='Register', fg='darkgreen', command=register, font=('Courier', 12), width=20).grid(row=0, sticky=E, column=1, padx=10)
Button(master, text='Login', fg='darkgreen', command=login, font=('Courier', 12), width=20).grid(row=1, sticky=E, column=1, padx=10, pady=10)

master.mainloop()
