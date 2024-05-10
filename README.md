# MGT 6203 - Team 48
## Understanding Mobile Phone Features Importance in India

 Team 48's group project GitHub repository for MGT 6203 (Canvas) Spring of 2023 semester.
 
 ---

 ### 1. Project Description
 
 The Main objective of this project is to determine and quantify the significance of smartphone features that impact	the	buying	decision of smart phone customers in India. To achieve this, smartphone ratings obtained from *flipkart.com* were analyzed against various phone features using different data modeling techniques. In order to evaluate the changes in features importance over time, datasets from 2019 and 2023 were studied and the results were compared.
 
 The project can be divided into 2 main phases:
 1. ***Data Acquisition*** In addition to *Kaggle.com* available datasets (Links to datasets provided in data sources section), Python scripts were used to web scrap a 2023 version of the data [Web Scraping Scripts](https://github.gatech.edu/MGT-6203-Spring-2023-Canvas/Team-48/tree/main/Code)
 2. ***Analysis*** The analysis of the final datasets is available in 2 R-based Jupyter notebooks [Analysis of 2019 Datasets](https://github.gatech.edu/MGT-6203-Spring-2023-Canvas/Team-48/blob/main/Final%20Code/Analysis_2019%20-%20Final.ipynb) and [Analysis of 2023 Datasets](https://github.gatech.edu/MGT-6203-Spring-2023-Canvas/Team-48/blob/main/Final%20Code/Analysis_2023%20-%20Final.ipynb)
 
 ### 2. Folder Structure: 
    ├── Code                               # Preliminiary code files 
       ├── Web_scraping                    # Python web scraping scripts
    ├── Data                               # Final datasets used in the project
    ├── Final Code                         # Final notebooks that run the analysis
    ├── Final Presentation Slides          # Final Presentation Slides and Youtube Link
    ├── Final Report                       # Final Project Report
    ├── Progress Report                    # Progress Report
    ├── Project Proposal                   # Project Proposal Report
    ├── Proposal Presentation              # Proposal Presentation Slides and Youtube Link
    └── README.md 
 
 ### 3. Getting Started:
 
 #### How to update the web scraped datasets:
 In order to update / web scrap a fresh dataset from *Flipkart.com*:
 1. Run [Flipkart_web_scraping.py](https://github.gatech.edu/MGT-6203-Spring-2023-Canvas/Team-48/blob/main/Code/Web_scraping/Flipkart_web_scraping.py) to web scrap a new version of the data. *Note* brands.txt is required to run the code successfully.
 2. Run [Flipkart_processing.py](https://github.gatech.edu/MGT-6203-Spring-2023-Canvas/Team-48/blob/main/Code/Web_scraping/Flipkart_processing.py) to clean and process the created data file from the first process.

 In order to update / web scrap a fresh dataset from *Gadgets360.com*:
 1. Run [gadget360.py](https://github.gatech.edu/MGT-6203-Spring-2023-Canvas/Team-48/blob/main/Code/Web_scraping/gadget360_web_scrapping.py) to web scrap a new version of the data.

*Notes on web scraping outputs:*
- Some manual data manipulation (clean up) could be required on the exported excel files.
- Outputs are exported from the python scripts in Excel format (.xlsx) and need to be manually converted to .csv format to be easily read by the Analysis notebooks.
 
 #### How to reproduce analysis results:
 The Analysis notebooks are designed to install required dependencies automatically. Markdown and comments are used to explain the various steps in the analysis and provide commentary when needed. [Analysis of 2019 Datasets](https://github.gatech.edu/MGT-6203-Spring-2023-Canvas/Team-48/blob/main/Final%20Code/Analysis_2019%20-%20Final.ipynb) and [Analysis of 2023 Datasets](https://github.gatech.edu/MGT-6203-Spring-2023-Canvas/Team-48/blob/main/Final%20Code/Analysis_2023%20-%20Final.ipynb)

 ### 4. Data Sources:
 Four different datasets are used in the project that when merged represent 2 final datasets:
 
 1. New (2023) datasets: Web scraped datasets of the websites of [Flipkart](https://flipkart.com) and [Gadgets360](https://gadgets360.com) website using Python.
 2. Existing (2019) datasets: datasets available on Kaggle for both Flipkart and Gadgets360 website. [Flipkart](https://www.kaggle.com/datasets/devsubhash/flipkart-mobiles-dataset) & [Gadgets360](https://www.kaggle.com/datasets/pratikgarai/mobile-phone-specifications-and-prices)
 
 ### 5. Dependencies
 Note that the analysis notebooks are configured to automatically install required packages.
 The following R packages are required to run the analysis notebooks:
+ [ggplot2](https://ggplot2.tidyverse.org/)
+ [corrplot](https://cran.r-project.org/web/packages/corrplot/vignettes/corrplot-intro.html)
+ [car](https://www.rdocumentation.org/packages/car/versions/3.1-2)
+ [MASS](https://www.rdocumentation.org/packages/MASS/versions/7.3-58.3)
+ [dplyr](https://www.rdocumentation.org/packages/dplyr/versions/0.7.8)
+ [lubridate](https://lubridate.tidyverse.org/)
+ [randomForest](https://www.rdocumentation.org/packages/randomForest/versions/4.7-1.1/topics/randomForest)
+ [xgboost](https://www.rdocumentation.org/packages/xgboost/versions/1.7.5.1)
+ [caret](https://www.rdocumentation.org/packages/caret/versions/6.0-94)
+ [stats](https://www.rdocumentation.org/packages/stats/versions/3.6.2)

The following Python libraries are required to run the web scraping scripts:
+ [pandas](https://pandas.pydata.org/)
+ [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
+ [requests](https://requests.readthedocs.io/en/latest/)
+ [numpy](https://numpy.org/)
+ [collections](https://docs.python.org/3/library/collections.html)
+ [urllib](https://docs.python.org/3/library/urllib.request.html)
+ [sys](https://docs.python.org/3/library/sys.html)
+ [time](https://docs.python.org/3/library/time.html)
+ [json](https://docs.python.org/3/library/json.html)
+ [traceback](https://docs.python.org/3/library/traceback.html)
+ [re](https://docs.python.org/3/library/re.html)

### 6. Contributors:
Adam Hall, Mohamed Hussien, Virginia Sahagun, Nazmus Sakib Sumon, Shadman Chowdhury

 ### 7. Acknowledgments
 As a team, we would like to show our gratitude and appreciation to Professor Bien and all the staff of MGT-6203 for the knowledge and inspiration that we have acquired through the project. We would also like to thank our TA, Leland Bolleter, for his great support and guidance throughout the project.
