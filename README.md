# About

![prediction_page](https://github.com/arnavgaddam/nba_stats/assets/108426505/8e26baaa-b662-4f70-be06-33e12998bcd8)

Basic machine learning application created to predict an NBA player's future performance based on their performance in the season so far. Predicted values include points scored, assists made, rebounds collected, and 3 pt field goals made. 

# Project Structure

The user interacts with the application through a flask server, which makes internal http requests to prompt the python backend to scrape and/or process information. Scraping is done using http requests directly to nba.com, without the use of a third-party library or dataset. As a result, all data is real-time and is updated whenever predictions are made. 

# Machine Learning Model

The model used is scikit-learn's ridge regression model. Although the accuracy of predictions isn't great, this regression model is a good proof of concept for the application and can be improved in the future if necessary. First, a feature selector is used to narrow down some of the 100+ features available to choose a small number to train the model. As for training, since this is time series data, predictions can only be made on past data points, not data from the future. 







