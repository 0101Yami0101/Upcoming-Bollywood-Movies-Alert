#Upcoming Bollywood movie alert
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
from twilio.rest import Client

URL = "https://gadgets360.com/entertainment/upcoming-bollywood-movies"

response = requests.get(url= URL)
data = response.text
# pprint(data)

#scrape Gadgets360 for upcoming movies
soup = BeautifulSoup(data, "html.parser")
arefs = soup.select(selector= "div h3 a")

#making list with scraped data
movie_names = []
for i in arefs:
   name = i.getText()
   movie_names.append(name)



dates= soup.find_all(name = "li", class_ = "_flx")
release_dates_list = []
for date in dates:
   try:
      re= date.select_one("div")
      r_date = re.getText()
      release_dates_list.append(r_date)
   except AttributeError:
      pass

# print(release_dates_list)

#getting month-year
month = datetime.now().strftime("%B")
year = datetime.now().strftime("%Y")
this_month = (f"{month} {year}")

#check month and notify
this_month_movie_list = []

for i in range(len(movie_names)-1):
   if this_month in release_dates_list[i]:
      article = (f"Movie: {movie_names[i]} - Releasing: {release_dates_list[i]}")
      this_month_movie_list.append(article)


if len(this_month_movie_list) != 0:
   # TWilio Notify via SMS
   SID = "YOUR TWILIO SID"
   AUTH = "YOUR TWILIO AUTH"

   client = Client(SID, AUTH)
   message = client.messages \
            .create(
               body= (f"Upcoming Movies Alert!! {this_month_movie_list}"),
               from_='YOUR TWILIO NUMBER',
               to='XXXX' #must be twilio verified
            )
else: 
   pass
