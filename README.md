# dentistas_app
Dash application to visualize dentists scraped from doctoralia

Dependency:

### BeautifulSoup : 
pip install beautifulsoup4
### plotly : 
pip install plotly 
### pandas : 
pip install pandas
### dash : 
pip install dash==0.35.1  # The core dash backend
pip install dash-html-components==0.13.4  # HTML components
pip install dash-core-components==0.42.1  # Supercharged components
pip install dash-table==3.1.11  # Interactive DataTable component (new!)

### To Run

1. The file reparse_dentistas_rj.py is a webscrape script to get the data from the doctoralia website.
2. This script writes the file out to dentistas_2019_bairros.csv
3. The visualization tool is dash_app.py
          run -> python dash_app.py
          in the browser go to: 127.0-0.1:8050
          
          In the visualization is posible to donwload small parts of the data by selecting desired columns on the table.
          
