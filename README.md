# Amazon-NLP-reviews

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-v3.7-blue)

## Introduction

In the era of online shopping, the plethora of choices available can overwhelm consumers. This project simplifies decision-making by utilizing Natural Language Processing (NLP) to recommend the best Amazon products based on specific user criteria. 

## Prerequisites

- Python 3.7+
- Flask
- SQLAlchemy
- NLTK

## Installation


git clone https://github.com/AmineHamane/Amazon-NLP-reviews.git
cd Amazon-NLP-reviews
pip install -r requirements.txt


## Data Collection

### Product Information

Data is collected from Amazon's product search pages, including:

- Product Names
- Product Prices
- Product Ratings
- Product Images
- Product Links

![Product Info Image](assets/your-image-link)

### Reviews

For each product, the following review information is collected:

- Profile Names
- Review Ratings
- Review Titles
- Review Content

![Review Info Image](assets/your-image-link)

## Data Cleaning

After gathering product and review information, the dataset underwent several cleaning steps:

- Filtering out reviews in languages other than English using NLTK.
- Handling missing values.
- Trimming whitespace from text fields.

These cleaning steps ensure that the dataset is focused and free of noise, improving the quality of the analysis and recommendations.
## Creating the NLP Model

Sentiment analysis is performed using VADER from NLTK and a pre-trained RoBERTa-based model. These tools allow for accurate sentiment analysis, enabling better product recommendations.

![NLP Model Image](assets/your-image-link)

## Creating a Flask Web App

The web app is built using Flask and SQLAlchemy and is styled using Bootstrap 5. It serves as a platform where users can filter product reviews based on specific features they're interested in.

![Web App Image](assets/your-image-link)





