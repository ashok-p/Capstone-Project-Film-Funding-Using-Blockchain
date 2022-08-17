import os
import json
from tkinter import Button
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

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
    with open(Path('./contracts/compiled/bolly.json')) as f:
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


st.title("Light-Camera-Action")
# import Image from pillow to open images
from PIL import Image
img1 = Image.open("./film_projects/pgro/pgro.png")
img2 = Image.open("./film_projects/sjsm/sjsm.png")
img3 = Image.open("./film_projects/bgro/bgro.png")

# display image using streamlit
# width is used to set the width of an image
st.image(img1, width=200)
st.write("PGRO - film")
st.image(img2, width=200)
st.write("SJSM - film")
st.image(img3, width=200)
st.write("BGRO - film")

st.write("Choose a project")
accounts = w3.eth.accounts
project = st.selectbox("Select Film Project", options=['PGRO', 'SJSM', 'BGRO'])
st.markdown("---")

pdf_file = project + '.pdf'
with open(pdf_file,"rb") as f:
      base64_pdf = base64.b64encode(f.read()).decode('utf-8')

pdf_display = F'<embed src=”data:application/pdf;base64,{base64_pdf}” width=”700″ height=”1000″ type=”application/pdf”>'

st.markdown(pdf_display, unsafe_allow_html=True)

################################################################################
# Register New Artwork
################################################################################
st.markdown("## Register new Artwork")
# Create the streamlit components required to get the following data from the user:
# 1. Artwork name
artworkName = st.text_input("Artwork Name")
# 2. Artist name
artistName = st.text_input("Artist Name")
# 3. Initial appraisal value
initialValue = st.text_input("Initial Appraisal Value")
# 4. Artwork URI
artworkURI = st.text_input("Artwork URI")

# @TODO: YOUR CODE HERE!

# Create a button called "Register Artwork" that uses the contract's
# registerArtwork function to register new artwork.
# Display the receipt for the transaction on the webpage.
# @TODO: YOUR CODE HERE!

if st.button("Register Artwork"):
    tx_hash = contract.functions.registerArtwork(
        address,
        artworkName,
        artistName,
        int(initialValue),
        artworkURI
    ).transact({'from':address, 'gas':1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")


################################################################################
# Appraise Art
################################################################################
st.markdown("## Appraise Artwork")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
new_appraisal_value = st.text_input("Enter the new appraisal amount")
report_uri = st.text_area("Enter notes about the appraisal")
if st.button("Appraise Artwork"):

    # Use the contract's `newAppraisal` function to record a new appraisal.
    # HINT: You can use the first account in `w3.eth.accounts[0]` for the
    # transaction.
    # @TODO: YOUR CODE HERE!
    tx_hash = contract.functions.newAppraisal (
        int(token_id),
        int(new_appraisal_value),
        report_uri
    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get the appraisal report history")
# Create a streamlit component that inputs a artwork token id from the user
token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)), key=1)
# @TODO: YOUR CODE HERE!
if st.button("Get Appraisal Reports"):
    # Create a filter that lists all of the Appraisal events for the token.
    # @TODO: YOUR CODE HERE!
    set_filter = contract.events.Appraisal.createFilter(
        fromBlock=0,
        argument_filters={'tokenId':token_id}
    )

    appraisals = set_filter.get_all_entries()
    if appraisals:
        for appraisal in appraisals:
            report = dict(appraisal)
            st.write(report)
            st.write(report["args"])
    else:
        st.write("Oops! no appraisals!")

    # Use streamlit to display all entries from the event filter.
    # @TODO: YOUR CODE HERE!
