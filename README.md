# insee-firms
Enrich companies datas with INSEE open data in Python using Google Big Table / Query.

Purpose of this program is to enrich company data based on french SIRET number using INSEE SIREN open data.

INSEE Sirene open data : 
https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3&provider=insee*

Use case : 
We have a big table in Google Cloud plateform with INSEE SIRET number and we enrich a column with company size
Then we use Google data studio to render the data.

Method : 
We start from a CSV file : companies-siret-source.csv
We import it into Big Query
We find the JSON key for authentication
And run the program
