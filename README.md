This project uses Python and Selenium library to scrape the News  websites for news articles. The program allows the user to select a search phrase, category, and date range for the articles they want to retrieve. The data is extracted and saved to a CSV file.

This program requires Python and the following libraries:

    rpaframework
    Selenium
    Robocorp

The program can be run on any operating system that supports Python.

#Getting Started

To use this program, follow these steps:

    Clone the repository
    Install the prerequisites using pip or any other package manager
    Check the setup.py file and set your variables
    Run the main.py file with Python

How to use

To use the program, open the main.py file and set the following variables in the setup.py file:

    URL: The URL for the New York Times website
    SEARCH_PHRASE: The search phrase for the articles you want to retrieve
    CATEGORY: The category of the articles you want to retrieve
    NUMBER_OF_MONTHS: The number of months in the past to search for articles

    ```

Once you have set these variables, you can run the program.


Sample Payload to run inside Robocorp
```
{
  "url": "https://www.apnews.com/",
  "search_phrase": "business",
  "number_of_months": 1,
  "category": [
    "Arts",
    "Books"
  ]
}
```
