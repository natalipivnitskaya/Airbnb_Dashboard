# Airbnb Web Application - [Dash]

This repository hosts the plotly dash application, which estimates the revenue of Airbnb listings in Austin, TX. The data used in the project comes from Inside Airbnb, a website that provides scrapped data from Airbnb. Austin was a hot housing market in 2020 and 2021. Motivation is to provide an interactive and intuitive way of getting an idea of how much people could get on short-term property rent-out. Estimation is based on price per night and occupancy rate. Occupancy rate is the popularity of the property and proxy for occupancy is the number of reviews per month. Not every guest leaves a review, however, so the underlying assumption is that every 3rd guest would remain the review. Therefore the number of reviews per month was multiplied by 3. 

In this visualization, the most important attributes were encoded. These attributes give the end-user the capability of selecting the desired region and the variables to label the main scatter map through a dropdown menu as well as hovering the data points to access additional information. Each user input is related to all the graphics produced, so when the user selects, for instance, region filter all marks and numerical informative values will automatically be updated.

The Variables dropdown menu allows to select 2 different variables and display their value in our map through the help of a discrete color scale. The variable Superhost tells whether the host of a specific listing is a verified super host by assigning red to regular hosts and green to the superhosts. This feature gives the user a sense of the importance of "superhost" status and how it impacts revenue. The variable Availability show listings in 3 different colors: “Red” corresponds to low or no availability, “Yellow” to medium, and finally “Green” to fully available.



### File Structure:
```
.
|--app.py
|--data_cleaning.py
|--data
|  |--calendar.csv
|  |--reviews.csv
|  |--neighbourhoods.csv
|  |--location_zooming.csv
|  |--listings.csv 
|  |--final_df.csv
|--assets
|  |--style.css
|  |--base.css
|--requirements.txt
```

### Installation

First, you need to clone the repository with the method of you choice (zip download or https). Next, in your command line, navigate to the model directory. Then you can install the required packages with the following commands:
```
pip install -r requirements.txt
```
### Usage

Once you are in the shell, you can run the app locally by:
```
python app.py
```
