# DEC_PJ04_TIKI.VN

## SOURCE

### I. GET DATA
#### 1. Get list of all Categories [get_categories.py](src/get_data/get_categories.py)
- For each category, we have `id`, `parent's id`, `name`, `level`, `url`
- The output data is `data/categories_[time-stamp].csv`. Exp: [categories_20230510_132551.csv](data/categories_20230510_132551.csv)
####
#### 2. Nomarlizing Data for next step: [normalize_categories.py](src/get_data/normalize_categories.py)
- Insert data from above result to MySQL
- Normalize Data by executing SQL stament in [normalize_categories.sql](SQL/normalize_categories.sql)
- The output data is [categories_with_relationship.csv](data/categories_with_relationship.csv)
#### 
#### 3. Crawling Product data from TIKI [get_product_API.py](src/get_data/get_product_API.py)
- Crawl Product in each category from [categories_with_relationship.csv](data/categories_with_relationship.csv) **(exluced Finished Categories)** by API that public by TIKI. 
- Store collected data in MongoDB.
- Tracking finished categories to file [DONE_CATEGORIES](data/DONE_CATEGORIES) in scenario the script would be restarted when error occurred.
- In case of host blocking, wait 10s for unblocking. Then retry. Increase waiting time by 1s for each failed retry.
- When other unexpected error occurred, script will be automated restarts.
- Logging file is [crawling.log](log/crawling.log)

### II. TRANSFER DATA
There are 3 ways to export and transfer data from MongoDB to MySQL
#### 1. Transfer all data in 1 bulk insert: [transfer_products.py](src/transfer_data/transfer_products.py)
- Query all data from MongoDB
- Config `max_allowed_packet` attribute in MySQL
- Insert all data to MySQL
#### 2. Transfer data for each product: [transfer_products_iterate.py](src/transfer_data/transfer_products_iterate.py)
- Query all data from MongoDB
- Iterate through dataset, insert one by one product
#### 3. Transfer data by spiting list of product: [transfer_products_split.py](src/transfer_data/transfer_products_split.py)
- Divide number of records in MongoDB to multi part
- Query each part and insert to MySQL

### III. ANALYSIS
#### 1. Module: [analysis.py](src/analysis/analysis.py)
- Get Product's Quantity by Category
- Get TOP10 Product's Origin
- Get TOP10 Best Seller
- Get TOP10 Best Rating
- Get TOP10 Lowest Price

Result store at folder [result](result)
#### 2. Module [search_ingredient.py](src/analysis/search_ingredient.py)
- Create Text Index at column `description`
- Search for `Thành phần` in `description`

Result store at folder [result](result)
#### 3. Module [download_images.py](src/analysis/download_images.py)
- Download all image of Product
- Store at folder [images](images)
