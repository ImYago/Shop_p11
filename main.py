import os
import json
from colorama import Fore
import datetime
import bcrypt


class Restaurant:
    # simple variables
    def __init__(self):
        self.current_user = 0
        self.current_grade = ''

    # create json files
    @staticmethod
    def create_json():
        # create json files for products
        if not os.path.exists('products.json'):
            with open('products.json', 'w') as f:
                t = '[\n' \
                    '   {\n' \
                    '       "type": "maishiy texnika",\n' \
                    '       "items": []\n' \
                    '   },\n' \
                    '   {\n' \
                    '       "type": "oziq ovqat",\n' \
                    '       "items": []\n' \
                    '   },\n' \
                    '   {\n' \
                    '       "type": "non mahsuloti",\n' \
                    '       "items": []\n' \
                    '   },\n' \
                    '   {\n' \
                    '       "type": "shirinlik",\n' \
                    '       "items": []\n' \
                    '   },\n' \
                    '   {\n' \
                    '       "type": "tozalik mahsuloti",\n' \
                    '       "items": []\n' \
                    '   }\n' \
                    ']'
                f.write(t)
        # create json files for users
        if not os.path.exists('users.json'):
            with open('users.json', 'w') as f:
                f.write('[]')

    # order history
    def order_history(self):
        with open("users.json", "r") as f:
            e = json.load(f)

            for i in e:
                if i["id"] == self.current_user:
                    all_history = i["order history"]

                    if len(all_history) > 0:
                        for order in all_history:
                            print(order)
                    else:
                        print(Fore.LIGHTYELLOW_EX + 'history not found')
                        break

    # check user
    # def check_user(self):
    #
    #     username = input(Fore.RESET + "Enter username: ")
    #     password = input(Fore.RESET + "Enter password: ")
    #
    #     with open('users.json', 'r') as f:
    #         file = json.load(f)
    #         for i in file:
    #             if i["username"] == username and i["password"] == password:
    #                 self.current_user = int(i["id"])
    #                 return True
    #         return False

    @staticmethod
    def make_p_id():
        with open('products.json', 'r') as f:
            e = json.load(f)
            count = 0
            for i in e:
                count += len(i["items"])
            return count + 1

    @staticmethod
    def make_u_id():
        with open('users.json', 'r') as f:
            e = json.load(f)
            return len(e) + 1

    def type_item(self):
        type_text = '''
            | Select product type |
            1. maishiy texnika
            2. oziq ovqat
            3. non mahsuloti
            4. shirinlik
            5. tozalik mahsuloti
            6. CANCEL
            $ '''
        selection = input(Fore.LIGHTCYAN_EX + type_text)
        if selection.isdigit():
            if 1 < int(selection) < 6:
                types = {
                    1: "maishiy texnika",
                    2: "oziq ovqat",
                    3: "non mahsuloti",
                    4: "shirinlik",
                    5: "tozalik mahsuloti"
                }

                product_type = types[int(selection)]
                if self.add_item(product_type):
                    return True
                print(Fore.LIGHTYELLOW_EX + "something wrong")
                return False
            if int(selection) == 6:
                return False

            else:
                print(Fore.LIGHTYELLOW_EX + "selection  not found!")
                self.type_item()
        else:
            print(Fore.LIGHTYELLOW_EX + "select with numbers only!")
            self.type_item()

    # add product
    def add_item(self, s):
        d = {1: "maishiy texnika",
             2: "oziq ovqat",
             3: "non mahsuloti",
             4: "shirinlik",
             5: "tozalik mahsuloti"}
        product_type = d[s]
        print(Fore.LIGHTBLUE_EX + f'default product type: {product_type}')
        p_id = self.make_p_id()
        name = input(Fore.CYAN + 'name: ')
        price = input(Fore.MAGENTA + 'price: ')
        quantity = int(input(Fore.LIGHTRED_EX + 'quantity: '))

        d = {
            "type": product_type,
            "id": p_id,
            "name": name,
            "price": price,
            "quantity": quantity
        }
        with open("products.json", "r") as g:
            l = json.load(g)

        for i in l:
            if i["type"] == product_type:
                i["items"].append(d)

        with open("products.json", "w") as f:
            json.dump(l, f, indent=2)
            print(Fore.GREEN + 'Item added successfully')
            return True
        return False

    # report
    @staticmethod
    def report():

        with open("users.json", "r") as f:
            users = json.load(f)
            if len(users) > 0:
                for user in users:
                    # all_history.append(i["order history"])
                    print(Fore.LIGHTMAGENTA_EX + "username [" + str(user["username"]) + "] - history :" + str(
                        user["order history"]))
            else:
                print(Fore.LIGHTYELLOW_EX + 'users not found')

    # username checking
    @staticmethod
    def check_username(username):
        with open("users.json", "r") as f:
            file = json.load(f)

            for i in file:
                if username == i['username']:
                    return True
            return False

    # login
    def login(self):
        if self.check_user():
            print(Fore.GREEN + 'Success!')
            return True
        else:
            sign_up = input(Fore.YELLOW + 'Password or username incorrect!\n'
                                          'Would you try again? [y/N]\n'
                                          ': ')
            if sign_up.lower() in ['yes', 'y', 'yep', 'ha', 'yeah']:
                return self.login()

        return False

    @staticmethod
    def get_grade(username):
        with open("users.json", "r") as f:
            users = json.load(f)

        for i in users:
            if i["username"] == username:
                return i["grade"]

    # check user
    def check_user(self):
        username = input(Fore.RESET + "Enter username: ")
        password = input(Fore.RESET + "Enter password: ").encode()

        with open('users.json', 'r') as f:
            file = json.load(f)
            for i in file:
                if i["username"] == username:
                    hashed_password = i["password"].encode()
                    if bcrypt.checkpw(password, hashed_password):
                        self.current_user = int(i["id"])
                        self.current_grade = self.get_grade(username)
                        return True
        return False

    # encrypt
    @staticmethod
    def encrypt(password):
        salt = bcrypt.gensalt()  # Generate a salt value
        hashed_password = bcrypt.hashpw(password.encode(), salt)  # Hash the password using bcrypt
        return hashed_password

    # sign up
    def signup(self):
        username = input('Enter username: ')
        password = input('Enter password: ')
        grade = input('Are you client [y/n]: ')

        if not self.check_username(username) and username not in ["0"] and username.strip() != "" and \
                grade.lower() in ["y", "n", "yes", "no"]:
            if password not in [""] and password.strip() != "":
                with open("users.json", "r") as f:
                    file = json.load(f)

                u_id = self.make_u_id()
                self.current_user = int(u_id)
                if grade.lower() in ["y", "yeah", "yes"]:
                    self.current_grade = 'client'
                    grade = 'client'
                else:
                    self.current_grade = 'admin'
                    grade = 'admin'
                password = self.encrypt(password)
                new_user = {
                    "id": u_id,
                    "username": username,
                    "password": password.decode(),
                    "order history": [],
                    "grade": str(grade)
                }
                file.append(new_user)
                with open("users.json", "w") as f:
                    json.dump(file, f, indent=2)
                return True
            else:
                print(Fore.LIGHTYELLOW_EX + "Invalid password!")
                return False
        elif self.check_username(username):
            print(Fore.YELLOW + 'Username already taken')
            self.signup()
        else:
            print(Fore.YELLOW + 'Invalid username')

    # add information to the history
    def add_to_history(self, p_name, p_price, p_quantity):
        with open("users.json", "r") as d:
            users_file = json.load(d)
            time = datetime.datetime.now()
            res = [p_name, int(p_price) * int(p_quantity), p_quantity, str(time)]

            for i in users_file:
                if i["id"] == self.current_user:
                    i["order history"].append(res)

        with open("users.json", "w") as f:
            json.dump(users_file, f, indent=2)

    # get food
    def get_product(self, _type):
        with open("products.json", "r") as f:
            products = json.load(f)

            for o in products:
                if o["type"] == _type:
                    if len(o["items"]) > 0:

                        # if product list is not null
                        for i, v in enumerate(products):
                            if v["type"] == _type:
                                items = products[i]["items"]
                                item_id = i
                                for product in v["items"]:
                                    a_t, b_t = f'currency: {product["quantity"]}x', 'out of stock'
                                    lines = '<------------------------------------------>\n'
                                    print(Fore.LIGHTGREEN_EX + f'{lines}'
                                                               f'| {product["id"]}. {product["name"]} - '
                                                               f'{product["price"]} - '
                                                               f'{a_t if product["quantity"] else b_t}\n'
                                                               f'{lines}')
                        order_id = int(input(Fore.LIGHTCYAN_EX + '$ '))

                        for i, v in enumerate(items):
                            if v["id"] == order_id:
                                print(Fore.LIGHTGREEN_EX + f'{v["name"]} - {v["price"]}')
                                count = int(input(Fore.RESET + 'how much do you want?\n$ '))
                                while 0 > count or count > v["quantity"]:
                                    count = int(input(
                                        Fore.RESET + f'how much do you want? base: [{v["quantity"]}]. {0} for exit\n$ '))
                                if count == 0:
                                    return False
                                self.add_to_history(v["name"], v["price"], count)
                                products[item_id]['items'][i]["quantity"] -= count
                                with open("products.json", "w") as z:
                                    json.dump(products, z, indent=2)
                                print(Fore.GREEN + "successfully ordered products")
                                return True

            print('items not found')
            return False

    # order food and quantity - x
    def order_product(self):
        actions = {
            1: "maishiy texnika",
            2: "oziq ovqat",
            3: "non mahsuloti",
            4: "shirinlik",
            5: "tozalik mahsuloti"
        }
        ot = '''
            1. maishiy texnika
            2. oziq ovqat
            3. non mahsuloti
            4. shirinlik
            5. tozalik mahsuloti
            6. exit
            $ '''
        st = input(Fore.BLUE + ot)
        if st.isdigit():
            st = int(st)
            if 0 < st < 6:
                return self.get_product(actions[st])
            if st == 6:
                return False
            print(Fore.YELLOW + "selection failed")
            self.order_product()
        else:
            print(Fore.YELLOW + 'select with numbers only!')
            self.order_product()

    # dining menu
    def main_menu(self):
        if self.current_grade == 'client':
            menu = '''
                1. order product
                2. history
                3. exit
                $ '''
            s = input(Fore.MAGENTA + menu)
            if s == '1':
                if self.order_product():
                    self.main_menu()
                else:
                    self.main_menu()
            elif s == '2':
                self.order_history()
                self.main_menu()
            elif s == '3':
                self.enterance()
            else:
                print(Fore.YELLOW + 'selection not exist')
                self.main_menu()
        elif self.current_grade == 'admin':
            menu = '''
                1. add product
                2. my adds
                3. report
                4. exit
                $ '''
            s = input(Fore.MAGENTA + menu)
            if s == '1':
                v = '''
            select type: 
            1. maishiy texnika
            2. oziq ovqat
            3. non mahsuloti
            4. shirinlik
            5. tozalik mahsuloti
            6. exit
            $ '''
                s_t = input(Fore.LIGHTCYAN_EX + v)
                if s_t.isdigit() and s_t != '6':
                    self.add_item(int(s_t))
                    self.main_menu()
                else:
                    self.main_menu()
            elif s == '2':
                self.order_history()
                self.main_menu()
            elif s == '3':
                self.report()
                self.main_menu()
            elif s == '4':
                self.enterance()
            else:
                print(Fore.YELLOW + 'selection not exist')

    # the enterance
    def enterance(self):
        self.create_json()
        enterance_text = '''
            1. register
            2. login
            3. exit
            : '''
        selection = input(Fore.BLUE + enterance_text)
        if selection.isdigit() and 0 < int(selection) < 5:
            if selection == '1':
                if self.signup():
                    self.main_menu()
                else:
                    self.enterance()
            elif selection == '2':
                if self.login():
                    self.main_menu()
                else:
                    self.enterance()
            elif selection == '3':
                print(Fore.GREEN + 'See you soon ????\n' + Fore.MAGENTA + "YOUR ADS HERE!")
                exit()
        else:
            print(Fore.YELLOW + 'selection not exist')
            self.enterance()


# ----------------------------------------------------------------
a = Restaurant()
a.enterance()  # main function of the shop
# ----------------------------------------------------------------
