# TRG Week 50

## $GS (Goldman Sachs)

- Goldman Sachs Group Inc. is a leading global investment bank and financial services company providing investment banking, securities trading, asset management, and wealth management services to institutional and individual clients worldwide, with historical stock data dating back to May 1999.

- https://www.kaggle.com/borismarjanovic/datasets

### 1st Commit

- Created a Flask API in `app/data.py` that loads the `gs.us.txt` CSV file using pandas and displays the Goldman Sachs stock data as an interactive HTML dataframe table with Bootstrap styling. The API includes a root route (`/`) that renders the data with metadata showing the date range and total number of records.

### 2nd Commit

- Dropped the `OpenInt` column from the original dataframe and created three time-period-based dataframes: (1) **Pre-2008 Financial Crisis** (1999-05-04 to 2007-12-31) representing early market growth, (2) **Financial Crisis & Recovery** (2008-01-01 to 2012-12-31) capturing the impact and recovery from the 2008 financial crisis, and (3) **Post-Recovery Growth** (2013-01-01 to 2017-11-10) showing sustained market recovery and growth. Updated the Flask API to display all three periods with record counts and period descriptions.

### 3rd Commit

- Added a new `/volume-analysis` route that visualizes the average yearly trading volume for all three time periods as a multi-panel bar chart using matplotlib. The visualization displays side-by-side comparisons of average volume trends across the Pre-2008 Crisis, Crisis & Recovery, and Post-Recovery Growth periods, with summary cards showing aggregate statistics for each period. All existing code remains unchanged.

### 4th Commit

### 5th Commit