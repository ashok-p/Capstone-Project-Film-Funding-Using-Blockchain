import os
import json
import token
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv('my.env')

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/tokens_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


def pin_artwork(owner, film, filmItem, price,issueQty,availableNow,commission, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "owner": owner,    #address of who owns it, initially the film company
        "film": film,       #film name
        "filmItem": filmItem, #item of the film that is NFTd
        "price" : price,    #price for this one
        "issueQuantity": issueQty, #how many of this nft issued at the beginning
        "amtAvailableNow": availableNow, # howmany available now
        "commission": commission,  #seller fee or commission
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, ipfs_file_hash


st.title("NFT Items Registry System")
# In production version, the user would have logged in and his/her associated account will be used
# Here we are asking for a User Account from Ganache to work with
st.write("Choose an account to get started")
accounts = w3.eth.accounts
owner = st.selectbox("Select Account", options=accounts)
st.markdown("---")
################################################################################
# Register NFT Item
################################################################################
#        "owner": owner,    #address of who owns it, initially the film company
#        "film": film,       #film name
#        "filmItem": filmItem, #item of the film that is NFTd
#        "price" : price,    #price for this one
#        "issueQuantity": issueQty, #how many of this nft issued at the beginning
#        "amtAvailableNow": availableNow, # howmany available now
#        "commission": commission,  #seller fee or commission
################
name = st.text_input("Name ")
initial_price = st.number_input("Enter the Initial Price")
issueQty = st.text_input("How many NFT Tokens for this item")  #amt is uint256

data = 0x0000  #data is bytes data, if any
availableNow = issueQty



tokenPrice= int(initial_price)
tokenId = 1


    #display tokens and their prices etc

st.write("Price of this Token is; ", tokenPrice)
st.write("Maximum count available for this item: ", availableNow)
amt= st.number_input("How many do you want", min_value=1, max_value=int(availableNow))
addr=st.text_input("Enter your Wallet Address for ETH withdrawl")
st.button("Confirm to Purchase")

#contract.functions.byuersList(addr,name,tokenId,  int(amt), tokenPrice).transact({'from': owner, 'gas': 1000000})
contract.functions.mint(owner,tokenId,  int(amt), int(amt), tokenPrice).transact({'from': owner, 'gas': 1000000})

#contract.functions.updateTokenCount(int(tokenId), int(amt)).transact({'from': addr})

    





# Now setting a sidebar menu


