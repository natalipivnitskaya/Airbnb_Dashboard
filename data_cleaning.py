# imports
import zipfile as zp
import pandas as pd
from datetime import datetime



listings = pd.read_csv('./data/listings.csv')
neighbourhoods = pd.read_csv('./data/neighbourhoods.csv')

#"square_feet", "cleaning_fee", "cancellation_policy"

listings = listings.loc[:, ["id", "host_id", "room_type", "amenities", "price",
                      "availability_30", "availability_60", "availability_90",
                      "reviews_per_month", "review_scores_rating", "review_scores_accuracy",
                      "review_scores_cleanliness", "review_scores_checkin", "review_scores_communication",
                      "review_scores_location", "review_scores_value", "listing_url",
                      "host_since", "host_response_time", "host_response_rate", "host_is_superhost",
                      "host_listings_count", "host_has_profile_pic", "host_identity_verified", 
                      "host_neighbourhood", "property_type", "neighbourhood_cleansed", 
                      "neighbourhood_group_cleansed", "latitude", "longitude", "minimum_nights"]]


listings["neighbourhood"] = listings.loc[:, ['neighbourhood_cleansed']].to_numpy()
listings = pd.merge(listings, neighbourhoods, on="neighbourhood", how='outer')


# Drop columns not needed
listings = listings.drop(columns = ["review_scores_accuracy","review_scores_cleanliness",
                                "review_scores_checkin","review_scores_communication","review_scores_value",
                                "host_has_profile_pic", "host_identity_verified"])

abt_df = listings


abt_df["cleaning_fee"] = 0
abt_df.dropna(subset = ["review_scores_location"], inplace = True)
abt_df.dropna(subset = ["host_listings_count"], inplace = True)
abt_df["host_since"] = abt_df["host_since"].fillna("10/23/2012") #fill with mode
abt_df["host_response_rate"] = abt_df["host_response_rate"].fillna("0%")
abt_df["host_response_time"] = abt_df["host_response_time"].fillna("a few days or more")
abt_df["host_is_superhost"] = abt_df["host_is_superhost"].fillna("f") 

#Transform Variables

abt_df['price'] = abt_df['price'].str.strip("$")
abt_df['price'] = abt_df['price'].str.replace(",",'')
abt_df['price'] = abt_df['price'].str.strip(" ")
#abt_df["cleaning_fee"] = '0$'
#abt_df["cleaning_fee"] = abt_df["cleaning_fee"].str.strip("$")

abt_df['host_since'] = abt_df['host_since'].str.strip(" ")

#Change datatypes
abt_df['price'] = abt_df['price'].astype(float)
#abt_df["cleaning_fee"] = abt_df["cleaning_fee"].astype(float)

abt_df["host_since"] = pd.to_datetime(abt_df["host_since"], format = "%Y/%m/%d")

abt_df.loc[abt_df["host_is_superhost"] == 't', "host_is_superhost"]=1 
abt_df.loc[abt_df["host_is_superhost"] == 'f', "host_is_superhost"]=0
abt_df['demand_per_month'] = abt_df["reviews_per_month"]*3 #every third person leaves a review



abt_df['amenities'] = abt_df['amenities'].str.strip("[")
abt_df['amenities'] = abt_df['amenities'].str.strip("]")
abt_df['amenities'] = abt_df['amenities'].str.replace('"','')
abt_df["amenities"] = abt_df["amenities"].str.split(",")
abt_df["amenities"] = abt_df['amenities'].apply(lambda x: [i.strip(' ') for i in x]) 


abt_df['ordinal_rating'] = '5 Stars'
abt_df.loc[abt_df['review_scores_rating']<=80,'ordinal_rating'] = '1 Star'
abt_df.loc[(abt_df['review_scores_rating']>80) & (abt_df['review_scores_rating']<=90),'ordinal_rating'] = '2 Stars'
abt_df.loc[(abt_df['review_scores_rating']>90) & (abt_df['review_scores_rating']<=95),'ordinal_rating'] = '3 Stars'
abt_df.loc[(abt_df['review_scores_rating']>95) & (abt_df['review_scores_rating']<100),'ordinal_rating'] = '4 Stars' # ordinal rating

abt_df['available'] = 'Low'
abt_df.loc[abt_df['availability_30']>7,'available'] = 'High'
abt_df.loc[(abt_df['availability_30']>0) & (abt_df['availability_30']<=7),'available'] = 'Medium' # ordinal availability next 30 days


# abt_df.loc[abt_df["cancellation_policy"] == "strict_14_with_grace_period", "cancellation_policy" ]= "strict"  #join variable categories into strict
# abt_df.loc[abt_df["cancellation_policy"] == "super_strict_60", "cancellation_policy"] = "strict"
# abt_df.loc[abt_df["cancellation_policy"] == "super_strict_30", "cancellation_policy"]= "strict"


abt_df["host_since"] = abt_df["host_since"].dt.year
abt_df["years_host"] = 2021-abt_df["host_since"] # years as host
abt_df["estimated_annual_revenue"] = abt_df["price"]*abt_df['demand_per_month']*abt_df["minimum_nights"]*12

pref_amenities = ["Wifi","TV","Smoking allowed","Free parking on premises","Pets allowed"]
abt_df['pref_amenities'] = abt_df['amenities'].apply(lambda x: [i for i in x if i in pref_amenities]) # aminities prefered

location_zooming = abt_df.groupby(by = "neighbourhood_group").agg("mean")[["latitude", "longitude"]].reset_index()

# Drop unused columns
abt_df = abt_df.drop(['availability_60','availability_90','reviews_per_month',
                      'host_since', 'host_response_rate', 'host_listings_count', 'neighbourhood_group_cleansed'], axis = 1)

#Save the final df
abt_df.to_csv('./data/final_df.csv', index=False)
#location_zooming.to_csv('./data/location_zooming.csv', index=False)

