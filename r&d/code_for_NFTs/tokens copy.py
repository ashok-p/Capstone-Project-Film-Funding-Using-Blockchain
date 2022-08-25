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


def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
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
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")
################################################################################
# Register NFT Item
################################################################################
st.markdown("## Register NFT Item")
item_from = st.text_input("Enter the name of the Movie/ Web-Series")
item_name = st.text_input("Enter the name for the Item from this Movie/Series")
initial_price = st.text_input("Enter the Initial Price")
amount = st.text_input("How many NFT Tokens for this item")  #amt is uint256
artwork_file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
data = 0x0000  #data is bytes data, if any

if st.button("Register with IPFS"):
    # Use the `pin_artwork` helper function to pin the file to IPFS

    artwork_ipfs_hash, file_hash =  pin_artwork(item_name, artwork_file) # @TODO: YOUR CODE HERE!

    artwork_uri = f"ipfs://{artwork_ipfs_hash}"

    tx_hash = contract.functions.registerToken(
        address,
        int(initial_price),
        int(amount),
        artwork_uri,
        file_hash,
        bytes(0x0000)
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #st.write("Transaction receipt mined:")
   # st.write(dict(receipt))
   # st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    #st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
    st.markdown(f"[Click to see the NFT just added](https://gateway.pinata.cloud/ipfs/{file_hash})")
    st.write(file_hash)
st.markdown("---")

# DISPLAY AVAILABLE TOKENS
tokensAvailable = contract.functions.numberOfTokens().call()

st.write("Number of tokens available-> "+ str(tokensAvailable))

if tokensAvailable > 0:
    tokenList = []
    for item in range (1,tokensAvailable+1):
        tokenData = contract.functions.tokenCollection(item).call()
        tokenList.append(tokenData)
    tokenSelected=st.sidebar.selectbox("Select Option", tokenList)
    availableNow = tokenSelected[6]

    if tokenSelected and int(availableNow) > 0:
        st.write("Selected Token Data")

        tokenPrice=tokenSelected[1]
        maxTokens = tokenSelected[2]
        tokenId = tokenSelected[5]
        tokenOwner=tokenSelected[0]

        st.write(tokenSelected[3], tokenSelected[2], tokenSelected[1], tokenSelected[0])
        st.write("token Id=>", tokenId)
        st.markdown(f"[Click to see the Token you selected](https://gateway.pinata.cloud/ipfs/{tokenSelected[4]})")

    #display tokens and their prices etc

        st.write("Price of this Token is; ", tokenPrice)
        st.write("Maximum count available for this item: ", availableNow)
        amt= st.number_input("How many do you want", min_value=1, max_value=int(availableNow))
        st.write("Your order will be executed upon the closing date of this campaign")
        name = st.text_input("Your Name Please")
        addr=st.text_input("Enter your Wallet Address for ETH withdrawl")
        if  st.button("Confirm to Purchase"):
            contract.functions.updateBuyersList (
                addr,   # buyer addr
                name,   # name
                tokenId,  #token id
                amt,  # how many he wants
                tokenPrice  # price paid. at present, taking the same price as offered
            ).transact({'from': addr, 'gas': 1000000})
            contract.functions.updateTokenCount(int(tokenId), int(amt)).call()

    





# Now setting a sidebar menu


