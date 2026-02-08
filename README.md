# SDA-Project

# Functional and Data-Driven GDP Analysis 

## Description
We have designed and implemented a data-driven GDP analysis system using functional
programming principles in Python, while enforcing the Single Responsibility
Principle (SRP) and introducing configuration-based behavior.

## Getting Started 
### Dependencies
* Python 3.14.3 
* pandas
* matplotlib 

### Installing
* Install dependencies:
    * python -m pip install pandas 
    * python -m pip install matplotlib  
* Ensure GDP-Data.csv and config.json are present
* Run the dashboard: python dashboard.py 

## Objectives
* Load and clean GDP data from a CSV file
* Filter data based on configuration
* Perform statistical operations
* Generate visualizations
* Display results through a dashboard 

## Project Structure
* config.json - all system behaviour is driven by this file
* loadData.py - loads GDP data from a .csv file
* cleanData.py - cleans and normalizes data
* filterDta.py - filters data using values given in config.json
* computeData.py - performs statistical computation
* validateConfig.py - validates configuration fiels
* contryVisualization.py - creates country-based visualizations (Line chart and Histogram)
* regionVisualization - creates region-based visualizations (Pie chart and Bar chart)
* dashboard.py - controls all files and displays output 

### Configuration File:
Fields:
* region: region name or list of regions
* country: specific country
* year: year for analysis
* operatio: statistical operation to perform
* output: output mode 

## Visualizations
### Region-Based Plots:
* Pie Chart - GDP distribution by country
* Bar Chart - Top countries GDP comparison 

### Country-Based Plots:
* Line Chart - GDP trend over years
* Histogram - GDP distribution 

## Error Handling
The dashboard handles:
* Missing or invalid CSV files
* Empty datasets
* Invalid configuration values
* Unsupported operations
* Missing visualization requirements 

## Team Information
Project completed in Pairs
    
    * Sabaina Ijaz
    * Nuwaira Batool 


    



