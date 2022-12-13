from time import strftime
import pandas as pd
import os
from datetime import datetime
import json


class Profile:

    def __init__(self, profile_number):

        self._profile_number = profile_number
        try:
            with open(
                f"info_profile/profile_{self._profile_number}_info.json", "r"
            ) as json_file:
                self._info_profile = json.load(json_file)
        except:
            self._phone_contacts = {"phone_number":[],"contact_name":[],"contact_date":[],"valid_number":[]}
            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_base = datetime.fromtimestamp(
                os.path.getmtime(f"bases/base_{self._profile_number}.csv")
            ).strftime("%Y-%m-%d %H:%M:%S")
            self._info_profile = {"index": "0", "date_base": date_base, "created_date":created_date, "last_access" : "0", 'contacts': "0", "phone_contacts":self._phone_contacts}
            Profile.write_json(self)
            print("A new info profile json was created")

        self._info_profile.update({"last_access": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        Profile.write_json(self)
        self._phone_contacts = self._info_profile["phone_contacts"]

        try:
            base_path = f"./bases/base_{self._profile_number}.csv"
            self._base = pd.read_csv(base_path)
            self._date_base = datetime.fromtimestamp(
                os.path.getmtime(base_path)
            ).strftime("%Y-%m-%d %H:%M:%S")
            if datetime.fromtimestamp(os.path.getmtime(base_path)).strftime('%Y-%m-%d %H:%M:%S') != self._info_profile['date_base']:
                print("A new contact list was accepted")
                self._info_profile.update({"index": "0","date_base":datetime.fromtimestamp(os.path.getmtime(base_path)).strftime('%Y-%m-%d %H:%M:%S')})
                Profile.write_json(self)

            messages = pd.read_csv(f"messages/messages_{profile_number}.csv", sep=";")
            self._message = messages["MESSAGES"]

        except Exception as e:
            print(e)

        self._index_number = int(self._info_profile["index"])

        if self._index_number < len(self._base):
            self._contact_number = self._base.loc[int(self._index_number), "phone_no"]
            self._contact_name = self._base.loc[int(self._index_number), "name"]
            if (self._index_number) >= len(self._base):
                print(
                    f"The mailing of Profile {self._profile_number} is over, please insert a new contact base and start it again"
                )
            else:
                self._phone_contacts["phone_number"].append(str(self._contact_number))
                self._phone_contacts["contact_name"].append(str(self._contact_name))
                self._phone_contacts["contact_date"].append(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                self._phone_contacts["valid_number"].append("valid")
                self._info_profile.update({"index": str(int(self._info_profile["index"]) + 1),})
                self._info_profile.update({"contacts": str(int(self._info_profile["contacts"]) + 1),})
                Profile.write_json(self)

        else:
            self._contact_number = "19971632843"
            self._contact_name = " "
            self._message = [f"The mailing of Profile {self._profile_number} is over, please insert a new contact base and start it again"] 

        if os.path.exists(f"./images/image_{profile_number}.jpeg"):
            self._image = f"C:/Users/user/Documents/whatsbot/whatsbot/images/image_{profile_number}.jpeg"
        else:
            self._image = False
    
    def write_json(self):
        json_object = json.dumps(self._info_profile, indent=4)
        with open(f"info_profile/profile_{self._profile_number}_info.json", "w+") as json_file:
            json_file.write(json_object)
        
    def __str__(self):
        return f"{self._contact_name}, {self._contact_number}, {self._index_number}, {self._profile_number}"

    def invalid_number(self):
        print("invalid")
        self._phone_contacts["valid_number"].pop()
        self._phone_contacts["valid_number"].append("O número de telefone compartilhado através de url é inválido.")
        Profile.write_json(self)
     
    def reset_index(self):
        self._info_profile.update({"index": 0})
        Profile.write_json()

    @property
    def contact_number(self):
        return self._contact_number

    @property
    def contact_name(self):
        return self._contact_name

    @property
    def message(self):
        return self._message

    @property
    def image(self):
        return self._image