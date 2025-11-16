"""
Tyler Eck 
Clock Life 
Simple program to translate/convert your age in military time/clock format. It gives insights into where you are in the day based on your age, gender, and country. 

"""
from bs4 import BeautifulSoup 
from urllib.request import urlopen 
from time import strftime
from datetime import datetime
import json
import os
from pathlib import Path

url = "https://www.worldometers.info/demographics/life-expectancy/" # URL to get data
cache = Path("life_expectancy_cache.json") # cache to fetch data from
MAX_CACHE_AGE_DAYS = 30 # cache date in days, reloads data every 30 days

# parse website to get life expectancy data 
def parse_website(url): 
    print("ACCESSING WEBSITE")
    data = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    tbody = table.find("tbody")
    rows = tbody.find_all('tr')

    for row in rows: 
        cols = row.find_all('td')
        col = [str(col.text.strip()) for col in cols]
        data.append(col)

    return data

# receive country input from user
def get_country(data): 
    countries = [d[1] for d in data]
    countries.sort()
    for c in countries: 
        print(c)
        
    selection = ""
    while selection == "": 
        selection = input("Enter your country from list: ").strip()
        if selection.lower() not in [c.lower() for c in countries]: 
            print("Error, not a valid country")
            selection = ""
        else:
            break

    for d in data: 
        if d[1].lower()  == selection.lower():
            return d

# receive date of birth input from user 
def get_DOB(): 
    while True: 
        date = input("Enter your date of birth in format day/month/year: ")
        try:
            d = datetime.strptime(date,"%d/%m/%Y")
            today = datetime.today()

            if d>today: 
                print("Date entered should be before today")
                print()
            else: 
                break

        except ValueError: 
            print("Invalid date, Enter date in format day/month/year. Example '28/05/1999'")
            print()
    
    return datetime.strptime(date,"%d/%m/%Y")

# receive gender input from user
def get_gender(): 
    selection = ""

    while selection == "": 
        selection = input("Enter Gender (Male or Female): ").strip().lower()
        if selection != "male" and selection != "female":
            print("Error, not valid input")
            selection = ""
        else:
            break
    
    return 3 if selection.strip().lower() == "female" else 4

# load data either from cache or from website
def load_data(): 

    if cache.exists(): 
        mtime = datetime.fromtimestamp(cache.stat().st_mtime)
        age_days = (datetime.now() - mtime).days

        if age_days <=MAX_CACHE_AGE_DAYS: 
            print("Accessing Cache")
            with open(cache,"r", encoding = "utf-8") as f: 
                data= json.load(f)
        else: 
            print(f"Cache is {age_days} days old. Refreshing from web")
            data = parse_website(url)

            with open(cache, "w", encoding="utf-8") as f: 
                json.dump(data, f, ensure_ascii=False, indent = 2)
            
    else: 
        data = parse_website(url)

        with open(cache, "w", encoding="utf-8") as f: 
            json.dump(data, f, ensure_ascii=False, indent = 2)
    
    return data

def main():
    # Get Data 
    data = load_data()
    country_data = get_country(data)
    today_date = datetime.today()
    birth_day = get_DOB()
    diff = today_date - birth_day
    age = round(float(diff.days/365),1)
    gender = get_gender()
    life_expectancy = float(country_data[gender])
    time = (age/life_expectancy)*24

    print("TOday date: ",today_date)
    print("Birthday: ", birth_day)
    print("Age: ", age)
    print("Life exp: ", life_expectancy)
    print("Time: ", time)

    hour = int(time)
    min = round((time - hour)*60)
    if min <10: min = str("0"+str(min))
    print("Time: ",hour,":",min)
    

if __name__ == "__main__": 
    main()