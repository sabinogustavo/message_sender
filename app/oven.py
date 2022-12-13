import pandas as pd
import os
from datetime import datetime
import json


class Oven:

    def __init__(self, profile_number):

        self._profile_number = profile_number

        try:
            with open(
                f"oven/profile_{self._profile_number}_info.json", "r"
            ) as json_file:
                self._info_profile = json.load(json_file)
        except:
            date_base = datetime.fromtimestamp(
                os.path.getmtime(f"oven/base.csv")
            ).strftime("%Y-%m-%d %H:%M:%S")
            self._info_profile = {"index": "0", "date_base": date_base}
            Oven.write_json(self)
            print("A new info profile json was created")

        try:
            base_path = f"./oven/base.csv"
            self._base = pd.read_csv(base_path)
            self._date_base = datetime.fromtimestamp(
                os.path.getmtime(base_path)
            ).strftime("%Y-%m-%d %H:%M:%S")
            if datetime.fromtimestamp(os.path.getmtime(base_path)).strftime('%Y-%m-%d %H:%M:%S') != self._info_profile['date_base']:
                print("A new contact list was accepted")
                self._info_profile.update({"index": 0,"date_base":datetime.fromtimestamp(os.path.getmtime(base_path)).strftime('%Y-%m-%d %H:%M:%S')})
                Oven.write_json(self)

            messages = pd.read_csv(f"oven/messages.csv", sep=",")
            self._message = messages["MESSAGES"]

        except Exception as e:
            print(e)

        self._index_number = int(self._info_profile["index"])

        try:
            self._contact_number = self._base.loc[int(self._index_number), "phone_no"]
            self._contact_name = self._base.loc[int(self._index_number), "name"]

        except Exception as e:
            Oven.reset_index(self)

    def __str__(self):
        return f"{self._contact_name}, {self._contact_number}, {self._index_number}, {self._profile_number}"

    def write_json(self):
        json_object = json.dumps(self._info_profile, indent=4)
        with open(f"oven/profile_{self._profile_number}_info.json", "w+") as json_file:
            json_file.write(json_object)

    def increase_index(self):

        if (self._index_number) >= len(self._base):
            Oven.reset_index(self)
        else:
            self._info_profile.update({"index": int(self._info_profile["index"]) + 1})
            Oven.write_json(self)

    def reset_index(self):
        self._info_profile.update({"index": 0})
        Oven.write_json(self)

    @property
    def contact_number(self):
        return self._contact_number

    @property
    def contact_name(self):
        return self._contact_name

    @property
    def message(self):
        return self._message
