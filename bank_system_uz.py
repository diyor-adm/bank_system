def inputCredentials():
    login = input('Enter login: ').strip().lower()
    password = input('Enter password: ').strip()
    return login, password


def checkCredentials(login, parol): 
    names,lens = readData()
    for i in range(0,lens):
        if names[i]['username'][0]==login and names[i]['password'][0]==parol:
            return names[i]
    return False


def readData():
    with open('bankdata.txt', 'r', encoding='utf-8') as data:
        global structuredData
        structuredData = []
        date_name = ['fullname', 'username', 'password', 'numOfAccs', 'accounts']
        lines = data.readlines()
        nums = 0
        for len_lines in lines:
            if not len_lines[0][0].isdigit():
                nums+=1
        for num in range(0,nums):
            user = {'fullname':[], 'username':[], 'password':[], 'numOfAccs':[], 'accounts':[]}
            for line in lines:
                usersData = line.strip().split(';')
                if not usersData[0].isdigit():
                    len_users = int(usersData[-1])
                    break
            for i, name_lines in enumerate(lines[:len_users+1],0):
                acc={} 
                name_line = name_lines.strip().split(';')
                if i == 0:
                    for k, value in enumerate(name_line,0):
                        user[date_name[k]].append(value)
                else:
                    for j, value in enumerate(name_line,0):
                        if j == 0:
                            acc[f'account-{i}'] = value
                        else:
                            acc[f'balans'] = value
                            user['accounts'].append(acc)
                lines.remove(name_lines)
            structuredData.append(user)
        return structuredData,nums


def accounts(value):
    print('Your accounts:')
    for num, account in enumerate(value,1):
        account_num = account[f'account-{num}']
        balance = account['balans']
        print(f'{num}. {account_num} - Balance: {balance} USD')


def source_account(account_data):
    while True:
        try:
            source_acc = int(input('Select the source account: '))
            if len(account_data)>=source_acc and source_acc>0:
                if int(account_data[source_acc-1]['balans'])>=1:
                    return source_acc
                else:
                    print('There are no funds in your account!')
            else:
                print('Please select an existing account from the list: ')
        except:
            print('Please select an available action from your accounts!')


def target_account(account_data):
    source_acc = source_account(account_data)
    while True:
        try:
            target_acc = int(input('Select the target account: '))
            if len(account_data)>=target_acc and target_acc>0 and source_acc != target_acc:
                return source_acc, target_acc
            elif source_acc == target_acc:
                print('Do not choose the same account number!. Please select another account!')
            else:
                print('Please select an existing account from the list!')
        except:
            print('Please select an available action from your accounts!')


def check_balance(balance):
    while True:
        try:
            sum = int(input('Enter amount to transfer: '))
            if sum<=int(balance) and sum>=1:
                return sum
            elif sum<1:
                print('Money cannot be less than $1')
            else:
                print(f'Please transfer $ {balance} from your account!\n')
        except:
            print('Please enter only the amount!\n')
        


def operation_money(source_acc, target_acc):
    sum = check_balance(source_acc['balans'])
    source_acc = int(source_acc['balans'])-sum
    target_acc = int(target_acc['balans'])+sum
    return source_acc, target_acc


def transfer_money(account_data):
    global account_user
    account_user = account_data
    accounts(account_data)
    sa_num, ta_num = target_account(account_data)
    source_acc = account_data[sa_num-1]
    target_acc = account_data[ta_num-1]
    sour_acc, tar_acc = operation_money(source_acc, target_acc)
    return sour_acc, sa_num, tar_acc, ta_num


def options():
    print('\n1 - list accounts\n2 - transfer money\n3 - open a new account\n4 - logout')
    while True:
        try:
            option = int(input('Choose an action: '))
            if option>0 and option<5:

                return option
            else:
                print('Please select an available action from the menu: ')
        except:
            print('Please select an available action from the menu: ')
        

def menu(user):
    option = options()
    if option == 1:
        accounts(user['accounts'])
    elif option == 2:
        if len(user['accounts'])>1: 
            balans_flag = False
            for acc_balans in user['accounts']:
                if int(acc_balans['balans'])>0:
                    balans_flag = True
            if balans_flag:        
                source_acc, sa_num, target_acc, ta_num = transfer_money(user['accounts'])
                user['accounts'][sa_num-1]['balans'] = source_acc
                user['accounts'][ta_num-1]['balans'] = target_acc
                print('\n<<< Operation succeeded! >>>\n')
                accounts(user['accounts'])
            else:
                print('There are no funds in your accounts')
                accounts(user['accounts'])
        else:
            print('You only have 1 account!')
    elif option == 3:
        user['accounts'].append(new_account(user['accounts']))
        user['numOfAccs'][0] = str(int(user['numOfAccs'][0])+1)
        print('\n<<< Operation succeeded! >>>\n')
        accounts(user['accounts'])   
    else:
        return option


def new_acc_number():
    from random import randint
    account = ''
    for i in range(16):
        account += str((randint(1,9)))
    return account


def new_account(accounts):
    new_acc = {}
    new_acc[f'account-{len(accounts)+1}'] = new_acc_number()
    new_acc[f'balans'] = '0'
    return new_acc


def inputNewUser():
    while True:
        fullname = input('Enter your fullname: ').strip().title()
        login = input('Enter new login: ').strip().lower()
        password = input('Enter new password: ').strip()
        if len(login)>3 and len(password)>3:
            flag_account = check_profil(login)
            if flag_account:
                return fullname,login, password
                
            else:
                print('This login is available on the system, try again!')
        else:
            print('Login and password should not be less than 4 characters and no spaces')


def check_profil(login): 
    names,lens = readData()
    for i in range(0,lens):
        if names[i]['username'][0]==login:
            return False
    return True
            
    
def new_profil():
    fullname,loginn, parol = inputNewUser()
    new_acc = new_acc_number()
    with open('bankdata.txt', 'a') as new_user:
        new_user.write(f'{fullname};{loginn};{parol};1\n{new_acc};0')
    print('\n<<< Operation succeeded! >>>\n')
    login()


def dashboard(user):
    fullname = user['fullname'][0]
    print(f'Hi! {fullname}')
    while True:
        value = menu(user)
        if value == 4:
            structuredData.append(user)
            with open('bankdata.txt', 'w') as new_data:
                for k in structuredData:
                    for num ,value in enumerate(k.values(),0):
                        try:
                            if num <3 :
                                new_data.write(value[0]+';')
                                
                            else:
                                new_data.write(value[0]+'\n')
                            
                        except:
                            for account in value: 
                                for acc_num, acc in enumerate(account.values(),0):
                                    if acc_num<1:
                                        new_data.write(str(acc)+';') 
                                    else:
                                        new_data.write( str(acc) +'\n')
            return auth()


def login():
    while True:
        login, password = inputCredentials()
        user = checkCredentials(login, password)
        if user:
            structuredData.remove(user)
            return dashboard(user)
        else:
            print("Login or password error. Please re-enter!")


def auth():
    print('\n1. Log in\n2. Sign up\n')
    selection = int(input('Choose an action: '))
    if selection > 0 and selection < 3:
        if selection == 1:
            login()
        else:
            new_profil()
    else:
        print('Please select an available action from the menu:')                
    
            
def welcome():
    print('Hi! Welcome to our digital bank!')
    auth()


welcome()
