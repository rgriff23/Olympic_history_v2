# Olympic history (version 2)

This project scrapes and processes data from www.sports-reference.com. 

It is a follow up to a project I did last year using R: http://www.randigriffin.com/2018/05/27/olympic-history-1-web-scraping.html

In retrospect, designing a script that collect athlete data alphabetically is extremely limiting. The script takes a long time to make all the requests, and my original design made it impossible to select subsets of the data prior to scraping the entire database (unless you cared about subsetting athletes alphabetically for some reason).  

This new scrape takes a different approach by:

1. Using Python's Beautiful Soup library.
2. Giving the code a modular structure that makes it possible to scrape subsets of athletes based on specific characteristics. 
3. Designing the functions to extract additional features (still thinking about what these will be). 
4. Including improved error handling and messaging.

This will make the code easier to use, improve, and debug. For example, it would be possible to add data from subsequent Olympics without repeating the entire scrape (if www.sports-reference.com should decide to continue updating their Olympics site... not sure what is going on there). It will also be much easier to modify the data handling functions for specific countries, if one wishes to extract more nuanced information from some subset of the data (e.g., deep dive into places of birth, which may be difficult to write scripts that work for ALL countries, but could work well for specific countries where the researcher has the domain knowledge to extract and match that information with external data). 
