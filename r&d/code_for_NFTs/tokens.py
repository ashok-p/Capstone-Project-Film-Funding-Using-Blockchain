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
st.markdown("## Register NFT Item")
film = st.text_input("Enter the name of the Movie/ Web-Series")
filmItem = st.text_input("Enter the name for the Item from this Movie/Series")
initial_price = st.text_input("Enter the Initial Price")
issueQty = st.text_input("How many NFT Tokens for this item")  #amt is uint256
commission = st.number_input("Commission in percent- Enter 5 for 5 percent ")

artwork_file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])

data = 0x0000  #data is bytes data, if any
availableNow = issueQty

if st.button("Register with IPFS"):
    # Use the `pin_artwork` helper function to pin the file to IPFS

    artwork_ipfs_hash, file_hash =  pin_artwork(owner, film, filmItem, initial_price,issueQty,availableNow,commission, artwork_file) 

    artwork_uri = f"ipfs://{artwork_ipfs_hash}"

    tx_hash = contract.functions.registerToken(
        owner,
        film,
        filmItem,
        int(initial_price),
        int(issueQty),
        int(availableNow),
        int(commission*100),  # commission multiplied by hundred bec of Solidity 
        artwork_uri,
        file_hash,
        bytes(0x0000)
    ).transact({'from': owner, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #st.write("Transaction receipt mined:")
   # st.write(dict(receipt))
   # st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    #st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
    st.markdown(f"[Click to see the NFT just added](https://gateway.pinata.cloud/ipfs/{file_hash})")
    st.write(file_hash)

# DISPLAY AVAILABLE TOKENS
tokensAvailable = contract.functions.numberOfTokens().call()

st.write("Number of tokens available-> "+ str(tokensAvailable))
st.write ("TYPE of OWNER is ==>> ", type(owner))

# SET THE TARGETS

fundsTarget = st.number_input("Target Amount to Raise")
timeBegin = st.number_input("Time Begin Campaign, enter in SECONDS since Jan 1 1970, UNIX Time ")
timeLimit =  st.number_input("How long for the Campaign, enter in SECONDS..(sorry!)")
st.button("SetTargets")


contract.functions.setCampaignTarget(int(fundsTarget), int(timeBegin), int(timeLimit)).transact({'from': owner, 'gas': 1000000})


# RETRIEVE THE TARGETS
fundsToRaise = contract.functions.fundsToRaise().call()
timeTarget = contract.functions.timeTarget().call()

st.write("FUNDSTORAISE-> ", fundsToRaise)
st.write("TIMETARGET-> ", timeTarget)

if tokensAvailable > 0:
    tokenList = []
    for item in range (1,tokensAvailable+1):
        tokenData = contract.functions.tokenCollection(item).call()
        tokenList.append(tokenData)
    tokenSelected=st.sidebar.selectbox("Select Option", tokenList)
    availableNow = tokenSelected[5]
    st.write("TOKEN SELECTED data-> ", tokenSelected)
    if tokenSelected and int(availableNow) > 0:
        st.write("Selected Token Data")

        tokenPrice=tokenSelected[3]
        maxTokens = tokenSelected[4]
        tokenId = tokenSelected[10]
        tokenOwner=tokenSelected[0]

        st.write("token Id=>", type(tokenId), type(tokenPrice), tokenId)
        st.write(tokenOwner, maxTokens, tokenPrice, availableNow)

        st.markdown(f"[Click to see the Token you selected](https://gateway.pinata.cloud/ipfs/{tokenSelected[4]})")

    #display tokens and their prices etc

        st.write("Price of this Token is; ", tokenPrice)
        st.write("Maximum count available for this item: ", availableNow)
        amt= st.number_input("How many do you want", min_value=1, max_value=int(availableNow))
        st.write("Your order will be executed upon the closing date of this campaign")
        #name = st.text_input("Your Name Please")
        addr=st.text_input("Enter your Wallet Address for ETH withdrawl")
        if st.button("Confirm to Mint"):
            contract.functions.mint(addr,tokenId,  int(amt), "").transact({'from': owner, 'gas': 1000000})

        if st.button("Confirm to PAY"):
            contract.functions.payForTokens(  int(tokenPrice)*1000000000000000000, owner).transact({'from': addr, 'value': int(tokenPrice)* 1000000000000000000, 'gas': 1000000})


       # contract.functions.updateTokenCount(int(tokenId), int(amt)).transact({'from': addr})

    





# Now setting a sidebar menu


