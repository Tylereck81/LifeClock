from bs4 import BeautifulSoup 
from urllib.request import urlopen 
from time import strftime
from datetime import datetime

url = "https://www.worldometers.info/demographics/life-expectancy/"


def parse_website(url): 
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


def get_country(data): 
    countries = [d[1] for d in data]
    countries.sort()
    for c in countries: 
        print(c)
        
    selection = ""
    while selection == "": 
        selection = input("Enter your country from list: ")
        if selection.strip().lower() not in [c.lower() for c in countries]: 
            print("Error, not a valid country")
            selection = ""
        else:
            break

    for d in data: 
        if d[1].lower()  == selection.lower():
            return d

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

def get_gender(): 
    selection = ""

    while selection == "": 
        selection = input("Enter Gender (Male or Female): ")
        if selection.strip().lower() != "male" and selection.strip().lower() != "female":
            print("Error, not valid input")
            selection = ""
        else:
            break
    
    return 3 if selection.strip().lower() == "female" else 4


def main():
    # Get Data 
    data = parse_website(url)
    country_data = get_country(data)
    today_date = datetime.today()
    birth_day = get_DOB()
    diff = today_date - birth_day
    age = round(float(diff.days/365),1)
    life_expectancy = float(country_data[get_gender()])
    time = (age/life_expectancy)*24

    hour = int(time)
    min = round((time - hour)*60)
    print("Time: ",hour,":",min)


if __name__ == "__main__": 
    main()