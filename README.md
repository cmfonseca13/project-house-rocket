# House Rocket
![house-rocket](https://user-images.githubusercontent.com/85557808/123824263-ca722f00-d8f5-11eb-87ff-45e87deeaca6.png)

## 1. Business Problem
*House Rocket* is a platform for buying and selling properties. Its business model is buying properties and then selling them at a higher price, with the purpose of maximizing profit. The different attributes of the properties influence their quality and drawing power and, therefore, their price.

The CEO would like to maximize the profit of the company, finding good deals. These are the main questions to be answered:
- Which properties should House Rocket buy, and at what price?
- Once the property is aquired, what is the best moment to sell, and by which price?

Currently, the business team is not able to make good buying decisions without analysing the data. The portfolio is extremelly large, and very time consuming for manual analysis.

## 2. Dataset
This dataset contains house sale prices for King County, which includes Seattle. It includes homes sold between May 2014 and May 2015. It can be found at https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885.
These are the 21 attributes available in the dataset for each property:

| Attribute | Description |
| --- | --- |
| id | Unique ID for each property sold |
| date | Date of the property sale |
| price | Price of sale of each property by the owner |
| bedrooms | Number of bedrooms |
| bathrooms | Number of bathrooms, where 0.5 accounts for a room with a toilet but no shower |
| sqft_living | Square footage of each property insterior living space |
| sqft_lot | Square footage of the land lot |
| floors | Number of floors |
| waterfront | Variable that indicates wether the property overlooks the waterfront or not (0 = no, 1 = yes) |
| view | An index from 0 to 4 that indicates how good the view of the property id |
| condition | An index from 1 to 5 that indicates the condition of the property |
| grade | An index from 1 to 13, that indicates the building construction and design. (1-3 = low quality, 7 = average quality, 13-13 = high quality |
| sqft_above | Square footage of the interior housing space that is above ground level |
| sqft_basement | Square footage of the interior housing space that is below ground level |
| yr_built | The year the building was initially built |
| yr_renovated | The year of the building's las renovation |
| zipcode | The zip code of the are the property is located |
| lat | Latitude |
| long | Longitude |
| sqft_living15 | Square footage of the interior housing living space for the nearest 15 neighbours |
| sqft_lot15 | Square footage of the land lots for the nearest 15 neighbours |

## 3. Business Assumptions
The assumptions about the business problem accepted in this project are as follow:
- Values of 0 in attribute **yr_renovated** are buildings that were not renovated.
- **Recent renovations** were considered to be the ones made after, and including, year **2000**.
- The attribute **price** was considered to be the price the property was/will be bought by the House Rocket company.
- The **duplicate ID** values were removed and only considered the most recent buy.
- The **location** and **condition** of the property is key for the decision on wether to buy it or not.
- The **season** is the decisive variable for the selling of the properties.

## 4. Solution Strategy
My strategy to solve this challenge was:

Step 1. Data Collecting and Business Analyzis
- Collect Data from the Kaggle website (https://www.kaggle.com/harlfoxem/housesalesprediction).
- Business problem statement.

Step 2. Data Transformation:
- Variable transformation.
- Data cleaning.

Step 3. Exploratory data analysis
- Explore the data to find insights for the business team.
- You can find the deployed app in Heroku at this link (https://project-house-rocket-app.herokuapp.com/)

Step 4. Answer the business challenges

Step 5. Business solutions

Step 6. Conclusions

## 5. Hypotheses mindmap

**Hypothesis 01:** Properties that are waterfront are, in average, 30% more expensive.

**Hypothesis 02:** Properties built before 1955 are, in average, 50% less expensive.

**Hypothesis 03:** Properties without basement have a sqrt_lot 50% bigger than the ones with basement.

**Hypothesis 04:** Properties with higher number of bedrooms are, in average, 10% more expensive.

**Hypothesis 05:** Properties that were never renovated are, in average, 20% less expensive.

**Hypothesis 06:** Older properties that were never renovated are 40% less expensive.

**Hypothesis 07:** Properties that were renovated recently are 10% more expensive.

**Hypothesis 08:** Properties in bad condition but that are waterfront, are 10% more expensive.

**Hypothesis 09:** The YoY (Year over Year) growth of the price of the properties is of 10%.

**Hypothesis 10:** The MoM (Month over Month) growth of the price of the properties with 3 bathrooms is 15%.

## 6. Top Data Insights
The most relevant insights of this project:

**Hypothesis 04:** Properties with higher number of bedrooms are, in average, 10% more expensive.

False: Properties with 5 to 10 bedrooms are more expensive.

**Hypothesis 09:** The YoY (Year over Year) growth of the price of the properties is of 10%.

False: The average price of the properties is similar between 2014 and 2015.

**Hypothesis 10:** The MoM (Month over Month) growth of the price of the properties is 15%.

False: The average price of the properties is higher between March and July.

## 7. Business results

| ID | Description | Conclusion |
| --- | --- | --- |
| H01 | Properties that are waterfront are, in average, 30% more expensive. | TRUE |
| H02 | Properties built before 1955 are, in average, 50% less expensive. | FALSE |
| H03 | Properties without basement have a sqrt_lot 50% bigger than the ones with basement. | TRUE |
| H04 | Properties with higher number of bedrooms are, in average, 10% more expensive. | FALSE |
| H05 | Properties that were never renovated are, in average, 20% less expensive. | TRUE |
| H06 | Older properties that were never renovated are 40% less expensive. | FALSE |
| H07 | Properties that were renovated recently are 10% more expensive. | TRUE |
| H08 | Properties in bad condition but with that are waterfront, are 10% more expensive. | TRUE |
| H09 | The YoY (Year over Year) growth of the price of the properties is of 10%. | FALSE |
| H10 | The MoM (Month over Month) growth of the price of the properties is 15%. | FALSE |

The **Total profit** (profit = buying price - selling price) of the properties in the portfolio is: **$1,120,904,228.20**

## 8. Conclusions

The main goal of this project was to answer to the CEO questions:

- Which properties should House Rocket buy, and at what price?

- Once the property is aquired, what is the best moment to sell, and by which price?

The properties were grouped by zip code, and the median of the price of the property was determined, taking into account only properties with regular to good condition. A total of 3844 properties presented a buying price bellow the median of their zip code, and therefore were suggested as potential good buys.

The median of the buying price of the properties suggested in the previous point was determined taking into account the season and zip code. For the properties presenting a buying price higher than the median of the price by zipcode + season, the selling price was determined with a 10% increase in property price. For the properties presenting a buying price lower than the median of the price by zipcode + season, the selling price was determined with a 30% increase in property price. The best moment to sell the properties is between the months of March and July, as the average price of the properties is higher.

## 9. Next steps 
For the future, more attention should be given to the possible renovation of older properties as a form of increasing their value, as properties that were renovated recently tend to be more expensive. This could be a viable way to increase profit.
