from requests import post, get, delete

url = "http://localhost:8000/user/"

# Just a while loop that takes user decisions
inp = input("Enter number: \n\t1. GET \n\t2. POST \n\t3. DELETE \n\t4. Quit\n")
while (inp != '4'):
    match inp:

        # GET
        case '1':
            uid = input("Enter User ID: ")

            try:
                print(get(url+uid).json())
            except Exception as e:
                print(f"ERROR: Failed to get user with ID {uid}:", e)

        # POST
        case '2':
            uid = input("Enter User ID: ")
            name = input("Enter User Name: ")

            try:
                print(post(url+uid, data={'data' : name}))
            except Exception as e:
                print(f"ERROR: Failed to create user:", e)
        
        # DELETE
        case '3':
            uid = input("Enter User ID: ")

            try:
                print(delete(url+uid))
            except Exception as e:
                print(f"ERROR: Failed to delete user with ID {uid}:", e)

        # EXIT
        case '4':
            break
        case _:
            print("Idk what u just put broski")

    inp = input("Enter number: \n1. GET \n2. POST \n3. DELETE \n4. Quit\n")
    

