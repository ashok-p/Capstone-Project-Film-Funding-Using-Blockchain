import os
import json
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
    with open(Path('./contracts/compiled/nfts_abi.json')) as f:
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
initial_appraisal_value = st.text_input("Enter the Initial Price")
amount = st.text_input("How many NFT Tokens for this item")  #amt is uint256
artwork_file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
data = 0x0000  #data is bytes data, if any

if st.button("Register with IPFS"):
    # Use the `pin_artwork` helper function to pin the file to IPFS

    artwork_ipfs_hash, file_hash =  pin_artwork(item_name, artwork_file) # @TODO: YOUR CODE HERE!

    artwork_uri = f"ipfs://{artwork_ipfs_hash}"

    tx_hash = contract.functions.registerNFT(
        address,
        int(initial_appraisal_value),
        int(amount),
        artwork_uri,
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

