# Full Stack Data Science Project

Application of the full-stack data science components. \
https://scrapy-app-test-8pazuhjvkp6bygcmduyuuj.streamlit.app \
Stack: Scrapy &rarr; MongoDB &rarr; Pandas &rarr; TextBlob &rarr; Streamlit &rarr; GitHub Action

## Description
Taught myself full-stack development, applied Scrapy on https://quotes.toscrape.com, and then finally applied all of it on https://news.ycombinator.com\
1. Created a spider to scrape the Hacker News website.
2. Made a pipeline that puts the scraped data into the MongoDB.
3. Used PyMongo and Pandas to extract and format data from the MongoDB database.
4. Used TextBlob and Pandas to make meaningful analysis, such as sentiment, articles per day, and average sentiment per day.
5. Used Streamlit to act as the front end. handling the coding part and the actual launch of the site.

## Getting Started
### Dependencies
- Install with requirements.txt: `pip install -r requirements.txt`
- Create a MongoDB Account, a cluster, a database user, allow network access, and get a connection string: `mongodb+srv://scraper_user:<password>@scraper-cluster.xxxxx.mongodb.net/` (password from database user)
- Create a .env file with: \
MONGO_URI=mongodb+srv://scraper_user:yourpassword@scraper-cluster.xxxxx.mongodb.net/ \
MONGO_DB=newsdb
- I then used the repository's secrets to store the MONGO_URI for automation (as seen in the YAML)
