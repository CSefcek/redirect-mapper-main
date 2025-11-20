# Redirect Mapper

## Description
This is a command-line tool that automates redirect mapping when migrating a website or web app.

## Use case
Since it evaluates how similar URLs are, its ideal use case is when both the old website’s URLs and the new website’s URLs are speaking URLs (i.e., human-readable, descriptive URLs).

## Dependencies
This script requires the following libraries:
* RapidFuzz
* Pandas
* OpenPyXL

## Project status
This project is a work in progress, and several best practices and improvements are still missing. Here are some of the planned next steps:
* Adding a requirements.txt file and improving the overall dependency installation experience
* Creating a UI to make the program more accessible
* Improving the logic so the program can handle migrations involving non-descriptive URLs
* Translating all column names in the input and output .xlsx files into English

## How to use

### Inputs
The program expects two input files containing the exported crawl data. Both files must be .xlsx files named crawl-current-website.xlsx and crawl-new-website.xlsx, and each must contain a sheet called crawl.
The current website file must include a column named URL sorgente.
The new website file must include columns named URL destinazione and Status code.

Sample input files are provided for testing and can be edited or replaced as needed for your project.

### Output
The script generates a single .xlsx file named mapping_results.xlsx, which contains three sheets:

Results – This sheet contains the actual redirect mapping. Each row includes the source URL, the status code that should be applied, the destination URL, and a similarity score (ranging from 0 to 100).

Destinazioni no 200 – Lists all URLs from crawl-new-website.xlsx that were detected with a non-200 status code.

Destinazioni inutilizzate – Lists all URLs from crawl-new-website.xlsx that were not used as redirect destinations.