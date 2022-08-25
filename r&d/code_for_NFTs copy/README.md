# lights_camera_action
## Code for NFTS
If Streamlit is not working..follow:
* pipenv install streamlit
* pipenv shell
* conda activate dev
* pip install web3
* pip3 install python-dotenv

### To run the NFTs code

* compile nfts.sol in Remix 
* deploy the nfts.sol contract
* copy the deployed contract address and paste it in the env file.
* copy the ABI for the deployed contract. make sure to select the nfts.sol is showing in the Contracts dropdown window
* paste the ABI just copied to the nfts_abi.json.  

* configure the my.env file with the following 4 variables:
WEB3_PROVIDER_URI="HTTP://127.0.0.1:7545"  
SMART_CONTRACT_ADDRESS=0xE6E84ed5dCf836d2Bc4417ADc27DC145b3b63585 ( u just copied above)  
PINATA_API_KEY="16964e6ec52b9d83919c"   
PINATA_SECRET_API_KEY="ff374cb6bb78bfa689ca28bcfce5bed56e6d4915b6a624088a7cac9831f39a9d"  
your Pinata keys for IPFS. These are mine. they too will work, i believe.  

* make sure you are in the folder containing the nfts.py file. Then run the streamlit
* streamlit run nfts.py


