# Import required libraries and dependencies
import os
import json
from web3 import Web3
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from pathlib import Path
import numpy as np
from PIL import Image
import base64
import numpy as np
import token
import sys
from os import path
import requests
import csv
import time
from common.PinataKeyClass import PinataKey

############Streamlit Code #########################

## Load the environment variables 
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

## Load the Contract
@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path('/Users/anushasundararajan-tzpc-lm00031/final_code/LCA/code_for_NFTs/contracts/compiled/tokens_abi.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract = load_contract()

def main_page():
    ##Function to set up background image 
    @st.cache(allow_output_mutation=True)
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    def set_png_as_page_bg(png_file):
            bin_str = get_base64_of_bin_file(png_file) 
            page_bg_img = '''
            <style>
            .stApp {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: scroll; # doesn't work
            }
            </style>
            ''' % bin_str
    
            st.markdown(page_bg_img, unsafe_allow_html=True)
            return

    # Set up Background Image 
    set_png_as_page_bg('image_2.png')

    ##Function to display PDF
    def show_pdf(file_path):
        with open(file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="600" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)


    # Load the data into a Pandas DataFrame
    df_movie_data = pd.read_csv(
        Path("Movie-Projects.csv"), index_col = 'Name')

    ## Set up the title in black
    st.markdown(f'<h1 style="color:#FF5733;font-size:40px;">{"Lights Camera Action"}</h1>', unsafe_allow_html=True)
    ## Set up the subtitle in black
    st.markdown(f'<h2 style="color:#F78066;font-size:24px;">{"Movie funding made easy!"}</h2>', unsafe_allow_html=True)

    ## Set up image for Movie 1
    image_1 = Image.open('film_projects/bgro/bgro.png')
    st.image(image_1, width=400)

    st.markdown(f'<p style="color:#c5b9cd;font-size:20px;">{"Bach Gaye Re Obama (BGRO) is a sequel to the hit film Phas Gaye Re Obama (PGRO). BGRO is a fast paced, fun-filled , hilarious gangster based satirical comedy, larger in scale and scope than its prequel. The story deals with the problems faced by a maid who is ‘used’ by the powerful diplomats abroad and how her challenging their might shakes the corridors of power both in India and the US."}</p>', unsafe_allow_html=True)

    ## Table with artist details for Movie-1
    st.table(df_movie_data.iloc[0])

    ## More details - Display PDF                  
    if st.button('Get Details on Movie-1 >>'):
        show_pdf('film_projects/bgro/synopsis.pdf')

    ## Set up image for Movie 2
    image_2 = Image.open('film_projects/pgro/pgro.png')
    st.image(image_2, width=400)

    st.markdown(f'<p style="color:#c5b9cd;font-size:20px;">{"The movie is a comedy with satire on recession. The story revolves around a Non-resident- Indian (NRI), Om Shashtri, who lived the American dream and made it big in the US. Then one day, as it happened in America, US economy went into recession and overnight big businesses, banks, and financial institutions crashed."}</p>', unsafe_allow_html=True)

    ## Table with artist details for Movie-2
    st.table(df_movie_data.iloc[1])

    if st.button('Get Details on Movie-2 >>'):
        show_pdf('film_projects/pgro/synopsis.pdf')

    ## Set up image for movie 3
    image_3 = Image.open('film_projects/sjsm/sjsm.png')
    st.image(image_3, width=400)

    def show_pdf(file_path):
        if st.button('Get Details on Movie-3 >>'):
            show_pdf('film_projects/sjsm/synopsis.pdf')


##### Side bar nav for filling out contribution 
def page2():

    @st.cache
    def get_table(table: str, filename:str) :
        table_name = pd.read_csv(filename)
        return table

    df = get_table( 'df', 'captable.csv')
    df = pd.read_csv('captable.csv')

    def write_to_file(df1) :
        df1.to_csv('captable.csv', encoding='utf-8', index=False)
        st.write(df1)

    def collectinfo():
    ##with st.form ("Collecting User Information"):
        option = st.selectbox('Which movie you would like to fund?', ('bgro', 'pgro', 'sjsm'))
        full_name= st.text_input("Full Name")
        wallet_address= st.text_input("Ethereum wallet address")
        amount= st.number_input("USD/ETH")
        submit = st.button("submit") 
        if submit: 
             st.write( "Deposit to 0x19b5d8DaBC9e08eE422D01FF1e7D1bA6aA81B704")
             new_data = {'Asset': option, 'fullname':full_name, 'wallet_address': wallet_address, 'amount': amount, 'deposit_to_address': '0x19b5d8DaBC9e08eE422D01FF1e7D1bA6aA81B704' }
             df1 = df.append(new_data, ignore_index=True)
             write_to_file(df1)
        else : 
            st. write("Please fill form")
         

    collectinfo()
  
## View cap table info 
def view_cap_table_data():
    df = pd.read_csv('captable.csv')
    st.table(df)

##### Side bar nav for issuer internal app 
def page3():

    def viewDividendsValue(asset, share_price):
        df = pd.read_csv('captable.csv')
        df["dividends"] = np.nan
        df["Total_shares_for_Asset"] = 100000000
        df["share_price"] = share_price
        if share_price != 0.00: 
            if option == 'bgro':
                df2= df[df['Asset'] == 'bgro']
                for index, row in df2.iterrows():
                    div = row["amount"]/share_price
                    st.write(row["fullname"], row["amount"], div)
                    df.at[index,'dividends'] = div
            elif option == 'pgro':
                df3= df[df['Asset'] == 'pgro']
                for index, row in df3.iterrows():
                    div = row["amount"]/share_price
                    st.write(row["fullname"], row["amount"], div)
                    df.at[index,'dividends'] = div
            else :
                df4= df[df['Asset'] == 'sjsm']
                for index, row in df4.iterrows():
                    div = row["amount"]/share_price
                    st.write(row["fullname"], row["amount"], div)
                    df.at[index,'dividends'] = div
            st.table(df)
        df.to_csv('dividends.csv')    
 
    st.markdown(f'<h1 style="color:#F78066;font-size:40px;">{"Issuer Internal App"}</h1>', unsafe_allow_html=True)
    option = st.selectbox('Select the asset for which you would like to view the captable', ('bgro', 'pgro', 'sjsm'))
    df = pd.read_csv('captable.csv')
    if option == 'bgro':
        st.write(df[df['Asset'] == 'bgro'])
    elif option == 'pgro':
        st.write(df[df['Asset'] == 'pgro'])
    else :
        st.write(df[df['Asset'] == 'sjsm'])
        
    share_price_in_ether = st.number_input("set share price in ether")
    viewDividendsValue(option, share_price_in_ether )

## Upload to IPFS
def uploadToIPFS():

    filePath = 'film_projects/IPFS-Files'
    textFileList=[]
    item={}

    print(f"Current working directory: {os.getcwd()}")

    headers={}
    endpoint =''
    # construct the Pinata key object
    keylist=PinataKey('pinataApiKey.csv')
    endpoint = keylist.fetchEndpoint('pinFileToIPFS') # choose the pinata endpoint and the corresponding header format


    mode='likerland' # the mode label is defined in the file pinata_api_key.csv.  
    headers=keylist.fetchKey('Free')

    fileCounter=0
    for file in os.listdir(filePath):
    # Check whether file is in text format or not.  If yes, put into the txtFileList
    
        if file.endswith(".txt"):
            fileCounter+=1
            textFileList.append(file)

    textFileList = sorted(textFileList)

    print(f'Number of text file to be uploaded:{fileCounter}')

    # Upload to Pinata, output to csv for record if successfully

    fieldnames=['filename','ipfsHash']
    fileWriter= open('uploadedTxt.csv','w', encoding="utf-8")

    dictWriter = csv.DictWriter(fileWriter,fieldnames)
    dictWriter.writeheader()

    for file in textFileList:
        item['filename']=file
        fullPath=f"{filePath}/{file}"

        files = {"file":open(fullPath, 'rb')}
        print(fullPath)
        resp = requests.post(endpoint, headers=headers, files=files)
        retry=0
        print("Response code %s, headers %s ." % (resp.status_code, headers.keys, ))
        while(resp.status_code != 200 and retry < 3):
          retry +=1
          print("attempt {}...".format(retry+1),end='',flush=True)
          time.sleep(15)
          resp = requests.post(endpoint, headers=headers, files=fullPath)    

        if(resp.status_code == 200):
            print(f"{fullPath} upload successful")
            item['ipfsHash'] = resp.json()["IpfsHash"]
        else:
            print('Upload Failed :')

        dictWriter.writerow(item)


    fileWriter.close()

def registerNFT():

    st.write("Looking at the captable to issue NFT based on share price")
    df_div= pd.read_csv('dividends.csv')
    st.table(df_div)
    commission = st.number_input("Commission %")
    button = st.button('Issue NFTs')
    option = st.selectbox('Select the asset for which you would like to issue NFTs', ('bgro', 'pgro', 'sjsm'))
    availableNow = 100000000
    ipfs_df = pd.read_csv("uploadedTxt.csv")
    artwork_uri = ipfs_df["filename"]
    file_hash = ipfs_df["ipfsHash"]
    msg = bytearray() 

    if st.button("Register with IPFS"):
    # Use the `pin_artwork` helper function to pin the file to IPFS
    
        for index, row in df_div.iterrows():
            if (row["Asset"] == option):
                    owner = df_div.at[index,'wallet_address']
                    film = df_div.at[index,'Asset']
                    filmItem = "filmItem"
                    initial_price = df_div.at[index,'share_price']
                    issueQty = df_div.at[index,'Total_shares_for_Asset']
                    wallet_address = df_div.at[index,'wallet_address']
                    #MINT TOKENS
                    st.write(wallet_address)
                    contract.functions.mint(wallet_address,1, int(issueQty), "").transact({'from': owner, 'gas': 1000000})
                    contract.functions.updateTokenCount(1, int(issueQty))
                    #Pay tokens
                    contract.functions.payForTokens( initial_price *1000000000000000000, owner).transact({'from': wallet_address, 'value': initial_price* 1000000000000000000, 'gas': 1000000})
                    
            else :
                st.write("Invalid Selection")
        

def page4():
        uploadToIPFS()
        registerNFT()



page_names_to_funcs = {
    "Movie Project Information": main_page,
    "Contribution": page2,
    "View captable & Issue NFT": page3,
    "Register & Distribute dividends": page4
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()








