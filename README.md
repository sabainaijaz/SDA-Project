# GDP Data Analysis Pipeline

## Description
This project implements a modular GDP Data Analysis System using:
* Dependency Inversion Principle (DIP)
* Clean layered architecture
* Functional programming style
* Pluggable input and output drivers
The system reads GDP data from a JSON file, processes and filters it based on user configuration, performs various analyses, and outputs results either to the console or as graphical charts 

## Project Architecture
Follows a layered design: 
    project_root/
    │
    ├── main.py                # Entry point (Orchestrator)
    ├── config.json            # Configuration 
    ├── core/
    │   ├── __init__.py
    │   ├── contracts.py       # Protocols (The 'Boss')
    │   └── engine.py          # Transformation Logic
    ├── plugins/
    │   ├── __init__.py
    │   ├── inputs.py          # CSVReader, JSONReader 
    │   └── outputs.py         # ConsoleWriter, GraphicsWriter
    └── data/                  # Source files

## Features and Analysis Supported
1.	Top 10 Countries by GDP for the given continent & year
2.	Bottom 10 Countries by GDP for the given continent & year
3.	GDP Growth Rate of Each Country in the given continent for the given data range
4.	Average GDP by Continent for given date range
5.	Total Global GDP Trend for given date range
6.	Fastest Growing Continent for the given date range
7.	Countries with Consistent GDP Decline in Last x Years
8.	Contribution of Each Continent to Global GDP for given data range

## Configuration
Example configuration structure:
{
    "continent": "",
    "country": "",
    "analysis": [ "growth"],
    "year_range": [ 2010, 2020 ],
    "input": "csv",
    "input_file": "data\\GDP-Data.csv",
    "output": "console",
    "chart_type": "bar"
}

## Design principles used
* Dependency Inversion Principle (DIP)
    * Core depends on abstractions
    * Inpurt & Output implement protocols
    * Easy to extend without modifying core
* Functional Programming Style
    * Avoids explicit loops
    * Uses map, filter, lambda
* Modular Structure
    * Input handles file issues
    * core handles logic
    * output handles presentation

## How to Run
- python main.py 
Ensure:
    * JSON/CSV data file is availabe
    * Configuration is properly defined
    * Required libraries installed 

## Requirements
* python 3.10+
* matplotlib (download using: pip install matplotlib)

## Author 
* Sabaina Ijaz
* Nuwaira Batool
