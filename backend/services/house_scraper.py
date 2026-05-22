# backend/services/house_scraper.py

import requests
from bs4 import BeautifulSoup

def get_tumkur_houses():

    url = "https://www.nobroker.in/property/rent/tumkur"

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        houses=[]

        cards=soup.find_all(
            "div",
            class_="card"
        )

        for card in cards[:10]:

            houses.append({

                "title":
                card.get_text(strip=True),

                "location":
                "Tumakuru",

                "price":
                "Dynamic",

                "distance":
                "Nearby"

            })

        return houses

    except Exception as e:

        print(e)

        return []
    
