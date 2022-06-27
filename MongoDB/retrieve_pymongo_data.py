
from pymongo import MongoClient
import pandas as pd
from datetime import datetime


class database:
    def __init__(self):
        self.client=MongoClient()
        self.db=self.client.students

    # def update(self,name): #,lecture
    #     now = datetime.now()
    #     dt_string = now.strftime("%H:%M:%S")
    #     self.db.English.update_one({"Name":name},{"$inc" : {"Time": dt_string}})

    # def export_csv(self): #lecture
    #     df=pd.DataFrame(columns=["Id","Name","Time"])
    #     records=self.db.English.find()
    #     path="Attendance/"
    #
    #
    #     for i in records:
    #         to_append=[i["Id"],i["Name"],i["Time"]]
    #         a_series = pd.Series(to_append, index = df.columns)
    #         df=df.append(a_series,ignore_index=True)
    #     CSV_Name=path+"Attendance.csv"
    #     df.to_csv(CSV_Name,index=True)
   
