# Charles Candelaria | PROGRAMMING ASSIGNMENT 8 - STOCKS WITH DATABASES AND DATA VISUALIZATION

## Assignment Description
This script generates a line plot for stock values in a portfolio.

Steps:
1. Sets up a database in memory
2. Creates an investor in the db
3. Imports stocks and bonds data from files
4. Parses data to class and persists it to db
5. Imports stock pricing data to db
6. Queries investor stocks
7. Queries historical stock pricing for each stock symbol in portfolio
8. User `matplotlib` to generate visualization of data
9. Saves report for investor to `out_files/` for investor

### Sample Visualization
![Sample Plot](./documents/bob_smith_20_05_23.png)

## Running Script
```bash
# installing packages
pip install -r requirements.txt
# running script OSX
python3 main.py
```

## Object Hierarchy
![Object Hierarchy](./documents/object-design.png)

## Libraries
- `matplotlib` Used for create data visualizations
- `SQLite3` User for storing and querying local data

## Datasources
All files provided from course material in canvas
- `AllStocks.json` Stock pricing data
- `Lesson6_Data_Bonds.csv` Bonds data for single investor
- `Lesson6_Data_Stocks.csv` Stocks data for single investor

**Note: There was a typo fixed in the `Lesson6_Data_Stocks.csv` where stock GOOG was GOOGL**


