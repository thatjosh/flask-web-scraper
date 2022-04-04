# Web Scraper Project

### 1   |   Video Demo
[![Web Scraper Project](/readme-images/index.PNG)](https://youtu.be/QuNGGkdoPdo)
<https://youtu.be/QuNGGkdoPdo>

### 2   |   Description
This is a simple web scraping project that allows users to web scrape text from websites. This webscraper is built with the intention of being used to web scrape news sites like TechCrunch.com.

To run the app:
```bash
    flask run
```

### 3   |   Features
#### User Login & History
![History](/readme-images/history.PNG)
This website can be used without logging in. However, logging in provides users the ability to recall past websites that they scraped. With the click of a single button ("Go"), the user will be redirected to the page displaying the scraped text.

#### Sessions
This website uses sessions to keep track of the current user that is logged into the website. Moreover, it is used to pass over information from one page onto another.

### 4   |   How to Navigate the Site
#### / (hompage)
![Index](/readme-images/index.PNG)
This is the homepage.
Clicking ("Scrape it!") leads to /pagescrape.
On the right side of the navigation bar, users can register for an account and/ or log in.
The site can be used by users who do not intend to log in to a registered account, but they will not be able to access the history page.

#### /pagescrape, /pagescraped

![Pagescrape](/readme-images/pagescrape.PNG)
Users can drop an input in pagescrape.html.
Data scraped will then be displayed in /pagescraped.
If the HTML address submitted is invalid, the user will then be redirected an apology page.

![Pagescraped](/readme-images/pagescraped.PNG)
Clicking Copy text will allow the user to copy the text to their clipboard.
Clicking Download as text file will result in the text being loaded in textfile and subsequently downloaded.

#### /register, /login
![Register](/readme-images/register.PNG)
Pages for registering an account and logging in.
The user will be redirected to an apology page if the submissions are invalid.

#### /apology
![Apology](/readme-images/apology.PNG)
Indicate that a client side error occured.
Could be due to error in registering the user, logging the user in or web scraping the webpage based on the link provided.
Clicking the ("Go Back") button will send the user back to the previous page they were on.

#### /history, /empty
![History](/readme-images/history.PNG)
Shows the history of webpages scraped.
These webpages can only be accessed when the user is logged on.
/empty is shown if the user's history is empty.
The user will be redirected to the page displaying the web scraped text when ("Go") is clicked.

### 5   |   Tech Stack
- Flask Web Framework
- Boostrap CSS Framework
- SQLite Database
- Beautiful Soup Library