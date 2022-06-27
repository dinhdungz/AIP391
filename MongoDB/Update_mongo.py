
from pymongo import MongoClient
import pandas as pd
import datetime
import time

class database:
    def __init__(self):
        self.client=MongoClient()
        self.db=self.client.students

    def update(self,name):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        self.db.Attendance.update_one({"Name":name},{"Time":dt_string})

    # def export_csv(self):
    #     data={
    #            "Id":self.Id,
    #            "name":self.name,
    #            "Time":self.Time
    #          }
    #
    #     df=pd.DataFrame(data,columns=["Id","name","Time"])
    #     df.to_csv("Attendance.csv",index=True)
