
# Project 2: Cryvesto 3.0- LIGHTS-CAMERA-ACTION
--- 

![P2ReadMeTitlePic](Images/P2-ReadMeTitle_2022-07-01181545.png)


*"Using a MachineLearning-Sentiment Trading Bot (ML-STB) that adopts trade signals from Social Media and News feeds about evolving markets ."* 


---
## Background

DANE PLS FILL THIS IN

---
--- 
## LIGHTS-CAMERA-FUNDING: USER STORY
 
 DANE

## ACCEPTANCE CRITERIA

## APPLICATION

### USER INTERFACE - Investor

ANNA/ANUSHA

### USER INTERFACE - App Administration

ANNA/ANUSHA
    - setting campaign targets
    - NFT Registration
    - Dividends
 

### SOLIDITY BACKEND

ASHOK

## CAPSTONE PRESENTATION

DANE/CARLOS - pls link the presentation here

---
---

## Technologies
ANUSHA/ANNA - PLS FILL IN IF U USED SOME OTHER TOOLS/LIBRARIES

The application is developed using:  
* Language: Python 3.7, Solidity
* Libraries: Pandas; Streamlit, Solidity, ERC 1155
* Development Environment: VS Code and Terminal, Anaconda 2.1.1 with conda 4.11.0, Jupyterlab 3.2.9, Remix
* OS: Mac OS 12.1

---
---

## Installation Guide
Before running the applications open your terminal to install the libraries and verify them. The following are instructions to install the libraries for the applications.  

* [python](https://www.python.org/downloads/) 
* [anaconda3](https://docs.anaconda.com/anaconda/install/windows/e) 
* [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [scikitlearn](https://scikit-learn.org/stable/install.html) 
* [NLTK](https://www.nltk.org/install.html)
* [streamlit](https://docs.streamlit.io/library/get-started/installation)

```
pip install streamlit                                     # python library to create 

```
```
### Clone the application code from Github as follows:
copy the URL link of the application from its Github repository      
open the Terminal window and clone as follows:  

   1. %cd to_your_preferred_directory_where_you want_to_store_this_application  
    
   2. %git clone URL_link_that_was_copied_in_step_1_above   
    
   3. %ls       
        CRYVEST2.0  
        
   4. %cd CRYVESTO_2.0/final   

The entire application files in the current directory are as follows:

* alpaca_trade_lib.py       (Alpaca trade lib)
* classification_reports_wsj.pdf
* classification_reports.csv
* CryvestoTradeApp.py       (Cryvesto Trading App)
* load_data.py              (load api library)
* mainline_reddit.ipynb     (reddit feed notebook)
* mainline_twitter.ipynb    (twitter feed notebook)
* mainline_wsj.ipynb        (wsj data notebook)
* ml_lib.py                 (ml library)
* my_api.env          
* newslib.py                (newsapi lib)
* Pipfile
* README.md
* reddit_classification_reports.csv  
* reddit_classification_reports.pdf
* reddit_plots.pdf        (cumulative returns plots)
* results with reddit data only
* results with twitter data only
* results wsj data only
* trade_api.py             (alpaca order api)
* trade.ipynb
* twitter_classification_reports.csv
* twitter_classification_reports.pdf
* twitter_lib.py            (social media lib)
* twitter_plots.pdf         (cumulative returns plots)
* wsj_headlines.csv         (wsj headlines hitorical data)
* wsj_lib.py                (wsj lib)
* wsj_plots.pdf             (cumulative returns plots)
* xactcryptos.py
    
---
---

## Usage
The following details the instructions on how to run the applications.  

### Setup the environment and Run the application 

Setup the environment using conda as follows:

    5. %conda create dev -python=3.7 anaconda  
    
    6. %conda activate dev  (if running the Cryvesto app go to the section on `Setup Streamlit` below')
    
    7. %jupyter lab  

### Run the Notebooks
THIS ASSUMES FAMILIARITY WITH JUPYTER LAB. If not, then [click here for information on Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/).  

- After step 7 above, this will take you to the jupyter lab window, where you can open the application notebook **mainline_twitter.ipynb, or mainline_reddit.ipynb, or mainline_wsj.ipynb** and run the notebook to test the hypothesis with respective data source.  

### Setup Streamlit
Before running the app, please make sure that Streamlit is installed on your system and the libraries mentioned above are installed as well.

### Run the Cryvest 2.0 App

After step 6 of setting up the environment, follow these instructions:
    
     7. pipenv install streamlit
     8. streamlit run CryvestoTradeApp.py
     
Follow the prompts and buy/sell Ethereum and Bitcoin cryptos. 

The Cryvesto 2.0 GUI app prompts the user for an email id for validation purposes (currently, hardcoded to 'admin'). Please enter admin when prompted. The App displays the user's current account information and is presented with a Crypto Sentiment of the Day(CSD) displaying a gauge with values between -1 and 1. It then prompts the user for coin selection and to buy/sell with the amount. Then it executes the trade using Alpaca.

---
---

## Cryvesto 2.0 Trading App
The Graphic User Interface for the Cryvesto 2.0 trading app is built using Streamlit. This development app uses Alpaca API to trade cryptocurrency on a paper account. The code extracts it from api.env file, which is commented out for now. It will be reinstated in the production version.

Presently, the CSD is calculated from the 'Augmento' Bull/Bear sentiment counts picked from a day in June to provide current data. For future development, we will change the code to pick the current date. 

### *Joined dataframe of Bullish & Bearish texts with datetime and signals:* 

![joined_df1](Images/P2-Joined_df1_2022-07-10143958.png) 

![joined_df2](Images/P2-Joined_df2_2022-07-10144017.png) 


### *The Cryptocurrency Sentiment of the Day signal:* 

![SentimentofDaySignl](Images/P2-SntmntofDySig_2022-07-10144040.png) 

### *The Graphic User Interface for the Cryvesto 2.0 trading app is built using* **Streamlit**.

![StreamlitTradeApp](Images/P2-ReadMeStreamlitTrdApp_2022-07-07171518.png) 

#### **The Cryvesto 2.0 Sentiment Meter Gauge** 

In the next release, the App will use the Adabooster model to make a prediction to buy/sell and advise the trader accordingly.

--- 
---

## Contributors 
Ashok Pandey - ashok.pragati@gmail.com, www.linkedin.com/in/ashok-pandey-a7201237  
Dane Hayes - nydane1@gmail.com, https://www.linkedin.com/in/dana-h-2a2a71243/  
Rensley Ramos - ranly196@gmail.com, https://www.linkedin.com/in/rensley-2-nfty/    
Anna Joltaya - annajolt11.04@gmail.com, https://www.linkedin.com/in/anna-joltaya-15a66387/
Anusha Sundarajan
Carlos
---
---

## License
The source code is the property of the developer. The users can copy and use the code freely but the developer is not responsible for any liability arising out of the code and its derivatives.

---
---

=======
