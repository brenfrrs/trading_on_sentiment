# Trading on Sentiment.
#### First steps towards classifying market movements across the DOW Industrial Average with text mining.

![banner](./images/banner_image.jpg) 

**Author:** [Brendan Ferris](https://www.linkedin.com/in/brendangferris/)

## Overview

Historically two routes to predicting market movements have been utilized. The first route is technical analysis, which primarily focuses on the use of quantitative stock indicators in order to predict fluctuations. The second most popular route is fundamental analysis, which takes qualitative information like news and behavioral economics into consideration. By focusing on the sentiment of news related to a given company, we employ the latter method in this project. 

## Business Problem

Predicting stock price movements is a historically difficult task. A large asset management firm has contracted me to train a classifier to predict the short term (24 hour) price movements of Apple, with later plans to apply what I learned in order to predict movements of the entire Dow Jones Industrial Index. Predictions made by the model will be used as a supplemental tool to guide decision making on behalf of the firms clients. According to the [Efficient Market Hypothesis (EMH)](https://www.sciencedirect.com/topics/economics-econometrics-and-finance/efficient-market-hypothesis), financial assets are priced fairly in developed markets -- making it impossible to gain an 'edge' with any measure of consistency over time. According to this theory the only way for a normal investor to make large gains would be to either adopt a passive investment strategy or make riskier investments on smaller companies. 

## Data

Article links and publish dates were obtained by scraping [Newslookup](https://www.newslookup.com/) in tandem with the [Newspaper3k](https://newspaper.readthedocs.io/en/latest/) package, which enables a streamlined method to scrape fulltext articles from various news sources. Each article is indexed on the date it was published. In total, ~39,000 fulltext news articles from 448 sources were obtained.

![breakdown of sources](images/news_articles_by_source.png)

## Methods

In order to complete this task, three primary objectives must be met. First, a data pipeline must be established which allows for a variety of past and present news sources to be scraped. Second, the data must be cleaned and processed in a machine-readable format. Third, the classifier needs to be trained on the cleaned data.

![workflow](./images/workflow_diagram.png)

## Results

After aggregating all of the article text to one row per day, and performing analysis on the 30 day rolling mean, we are able to visualize the impact (or lack thereof) that news and sentiment have on stock price movements. 

![30 day rolling](images/effect_of_news_on_price.png)

From the graph above, we can see that there are a few interesting regions that have  

## Conclusions

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Bibendum at varius vel pharetra vel turpis nunc eget. Quis lectus nulla at volutpat diam ut venenatis tellus. Posuere ac ut consequat semper viverra nam libero justo laoreet. Pulvinar elementum integer enim neque volutpat ac tincidunt vitae. Aliquam etiam erat velit scelerisque in. Porta non pulvinar neque laoreet suspendisse. Ac tincidunt vitae semper quis. In iaculis nunc sed augue lacus viverra. Posuere ac ut consequat semper viverra nam libero justo laoreet.

## Next Steps

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Bibendum at varius vel pharetra vel turpis nunc eget. Quis lectus nulla at volutpat diam ut venenatis tellus. Posuere ac ut consequat semper viverra nam libero justo laoreet. Pulvinar elementum integer enim neque volutpat ac tincidunt vitae. Aliquam etiam erat velit scelerisque in. Porta non pulvinar neque laoreet suspendisse. Ac tincidunt vitae semper quis. In iaculis nunc sed augue lacus viverra. Posuere ac ut consequat semper viverra nam libero justo laoreet.

## For More Information

Insert links to relevant information here.

## Repository Structure

<pre>Tree goes here.</pre>