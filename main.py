import pandas as pd
import numpy as np
import seaborn as sns
import sklearn as sk
import matplotlib.pyplot as plt
import json
import sqlite3


class SarsV2():
    def __init__(self, file):
        self.file = file


    def _parseData(file):
        """
        Clean data and prepare structurally for usage
        Input:  JSON file
        Return:  xlsx file
        """
        global df

        with open(file, "r") as f:
            data = json.load(f)

        """
        CHANGE NAMES OF COLUMNS TO BE SHORTER
        """

        df = pd.DataFrame(data["records"])
        df = df.rename(columns={"Cumulative_number_for_14_days_of_COVID-19_cases_per_100000" : "Cum2WeekCasesPer10k"})

        print(df.head())
        print(df.describe(include="all"))
        print(df.info())
        print("Success!")


    def retrieveInformation(file):
        """
        Retrieve information for Afghanistan
        Input: JSON file
        Output: Dataframe object
        """
        conn = sqlite3.connect("SarsV2")
        df.to_sql("records", conn, if_exists='replace', index=False)

        # afg
        print(pd.read_sql_query("SELECT * FROM records WHERE countryterritoryCode = 'AFG'", conn))
        # sbn plot, countries by cases

        labels = (pd.read_sql_query("SELECT DISTINCT countriesAndTerritories FROM records", conn))["countriesAndTerritories"].to_list()
        sizes = (pd.read_sql_query("SELECT DISTINCT Cum2WeekCasesPer10k FROM records WHERE Cum2WeekCasesPer10k IS NOT NULL AND Cum2WeekCasesPer10k != '' AND Cum2WeekCasesPer10k > 0", conn))["Cum2WeekCasesPer10k"].to_list()
        fig, ax = plt.subplots()
        ax.pie(sizes, labels = labels, autopct='%1.1f%%')


        
def main():
    SarsV2._parseData(file_path)
    SarsV2.retrieveInformation(file_path)

file_path = "SarsCov2//SarsV2Dataset.customization"

if __name__ == "__main__":
    main()