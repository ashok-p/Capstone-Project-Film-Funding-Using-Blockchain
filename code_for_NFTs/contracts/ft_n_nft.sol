// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts@4.7.3/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts@4.7.3/access/AccessControl.sol";
import "@openzeppelin/contracts@4.7.3/token/ERC1155/extensions/ERC1155Supply.sol";


contract Bolly_ft_and_nft is ERC1155, AccessControl, ERC1155Supply {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    uint256 public rate;    
    address payable owner_address;                      

    constructor(uint exchangeRate) ERC1155("") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);

        rate = exchangeRate; //wei to token unit
    }

// NftMetaData for NFT assigned to n investor
    struct tokenInfo {
        address payable owner; //who owns it. This account gets credited upon minting to investor
        string film;
        string filmItem;
        uint256 value;  //price for this one
        uint256 amount; //how many of this nft
        uint256 availableNow;
        uint256 commission;
        string uri;  //uri of the. token
        string file_hash; // for Streamlit Ease
        bytes data;
        uint256 tokenid; //for Streamlit ease
    }

    //Map token id to TokenInfo
    mapping(uint256 => tokenInfo) public tokenCollection;

    uint256 tokenId; //number of tokens registered

// Map tokenId to TokenBalance,i.e. what's left after a sale
    mapping (uint256 => uint256) public tokenBalance;

    mapping (uint256 => string) private _uris;
    mapping (string => uint256) private _idOfUris;

    struct buyer {
        address  payable addrOfBuyer;
        string  name;
        uint256 tokenId;
        uint256 numberOfTokensToBuy;
        uint256 purchasePrice;
    }

// Buyers list is accumulated until the time the campaign is SUCCESSFULLY over
// This can be used if the campaign is unsuccessful, to process refunds

    mapping (address => buyer) public buyersList;
    address [] public buyerAddress;

    function buyersListMintAndPay( 
                    address payable buyerAddr,  // buyers wallet addr, can/will be paid profit upon realization
                    string memory buyersName,  // buyers name.. oops!
                    uint256 tokenPurchased,  // which token or NFT
                    uint256 numOfTokens,  // how many of those tokens, 1 for NFT - obviously!
                    uint256 pricePaid
                    ) public {
        buyersList[buyerAddr] = buyer(
                    buyerAddr,
                    buyersName,
                    tokenPurchased,
                    numOfTokens,
                    pricePaid);

        // make an array of addresses as we add buyer to the buyerslist, because iterating over mapping is not possible
        // this is a workaround to iterate over the mapping,i.e. buyersList. we will iterate later. when we mint
        // we will use buyerAddress array to iterate oner the mapping using the address as. they mapping key

        buyerAddress.push(buyerAddr);  //push adds the item to the array
        mint(buyerAddr, tokenPurchased, numOfTokens, "");  //mint tokens
        payForTokens(pricePaid, owner_address); //pay to the owner for tokens
        updateTokenCount(tokenPurchased, numOfTokens); //update tokencount
    }

    // After building the orderbook called buyersList, each entry in this mappping is an order.
    // The decision whether the Target is reached is taken elsewhere in the program

    //function mint_buyersList() public {
    //  for (uint i=0; i < buyerAddress.length ; i++){
            // mint(owner, tokenId, howMany, data);
            // buyersList is a mapping, it is acccessed through an array that was created while building
            // the buyersList, so it is in the same exact sequence
    //        mint ( 
     //           buyersList[buyerAddress[i]].addrOfBuyer,  //buyer's address that can be paid dividend/profit
    //            buyersList[buyerAddress[i]].tokenId, // which token, ie tokenID
    //            ""      // no more data needed to be passed, thats why null ""
    //        );
    //    }
    //}
    // Refund the buyers if. the campaign was unsuccessful

    function refund_buyers() public {
      for (uint i=0; i < buyerAddress.length ; i++){
            // mint(owner, tokenId, howMany, data);
            // buyersList is a mapping, it is acccessed through an array that was created while building
            // the buyersList, so it is in the same exact sequence
            refundForTokens (
                buyersList[buyerAddress[i]].tokenId,
                buyersList[buyerAddress[i]].numberOfTokensToBuy,
                buyersList[buyerAddress[i]].purchasePrice, 
                buyersList[buyerAddress[i]].addrOfBuyer);
        }
    }


// reset the buyerlist array and buyerAddress mapping

    function reset_buyerlist() public {
        for (uint i=0; i < buyerAddress.length ; i++){
            // mint(owner, tokenId, howMany, data);
            // buyersList is a mapping, it is acccessed through an array that was created while building
            // the buyersList, so it is in the same exact sequence
              //buyer address
              // buyersList[buyerAddress[i]].addrOfBuyer = address(0x0000); How to initialize this?
                buyersList[buyerAddress[i]].name = "";
                buyersList[buyerAddress[i]].tokenId = 0;
                buyersList[buyerAddress[i]].numberOfTokensToBuy = 0;
                buyersList[buyerAddress[i]].purchasePrice = 0   ; 
        }
        // reset the buyerAddress array
        uint len = buyerAddress.length; 
        for (uint i=0; i<len; i++){
            buyerAddress.pop();
        }

    }

    uint256 public fundsToRaise; // wei
    uint256 public timeTarget; //in seconds
    uint256 public startTime; // start time in seconds (UNIX time) from Jan 1, 1970

    // set campaign Targets - ETHs, timeBegin - is time to start (UNIX Time), timeInSeconds - duration of campaign
    function setCampaignTarget(uint256 ethToRaise, uint256 timeBegin, uint256 timeInSeconds) public {
        fundsToRaise = ethToRaise * rate * 1000000000000000000;
        timeTarget = timeInSeconds;  // duration of campaign starting at startTime
        startTime = timeBegin;  // start time in seconds (UNIX time) from Jan 1, 1970
    }

    // extend the time for the campaign, if needed
    function extendTime (uint256 newTime) public {
        timeTarget = timeTarget + newTime;  // extend time target by the newTime amount
    }

    // balanceTime is the time left for the campaign
    // i don't trust block.timestamp as it has been unreliable. To make any decision, we shd use actual time clock
    // and not depend upon block.tiemstamp. I m using it as I am asked to by the compiler. for now, i will leave it an
    // see if it works all the time..

    function balanceTime() public returns (uint256) {
        uint256 t = startTime+timeTarget;

        require (block.timestamp <= t, "Time Expired!!");   // seems like 'now' is deprecated. compiler asked to use
        return (t - block.timestamp);                       // block.timestamp instead of 'now'
    }


    function mint(address account, uint256 id, uint256 amount, bytes memory data)
        public
        onlyRole(MINTER_ROLE)
    {
        _mint(account, id, amount, data);

    }

    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        public
        onlyRole(MINTER_ROLE)
    {
        _mintBatch(to, ids, amounts, data);
    }

    // The following functions are overrides required by Solidity.

    function _beforeTokenTransfer(address operator, address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        internal
        override(ERC1155, ERC1155Supply)
    {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC1155, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    //Register a token with all initial metadata information

    function registerToken(
        address payable owner,   //who owns
        string memory film,  // which film
        string memory filmItem,  // which item of the film
        uint256 initialPrice, // initial price or issue price
        uint256 howMany,  // initial or issue qty
        uint256 availNow,  // how much available now
        uint256 commission, // sellers commission in percent, 5 for 5 percent
        string memory nftURI, // IPFS uri
        string memory file_hash, // IPFS file hash for eas of access
        bytes memory data // any other data, if
        
    ) public returns (uint256) {
        //uint256 tokenId;

        tokenId +=1; 


         // mint(owner, tokenId, howMany, data); we will mint ONLY when the campaign is successful
         // For now, we just register the tokens and build the order book

         //_setURI(nftURI);
        // added file_hash for ease of display in Streamlit-IPFS, 
        // added tokenId on RHS, though not needed here, but eases work from Streamlit for updating
        // count of tokens/tokenId

        
        tokenCollection[tokenId] = tokenInfo(owner, film, filmItem, initialPrice, howMany, availNow, commission, nftURI, file_hash, data, tokenId);
        tokenBalance[tokenId] = howMany; //initialize the totalcount of this token
        _uris[tokenId] = nftURI;  // uri of the token  mapped to tokenID
        _idOfUris[nftURI] = tokenId;  // tokenId mapped to Uri
  
        return tokenId;
    }
 
 // get Uri from the Id of the token
    function getUri( uint256 tokenId) public view returns (string memory) {
        return _uris[tokenId];
    }

// get TokenId from the Uri of the token

    function getIdFromUri(string memory uri) public view returns (uint256) {
        return _idOfUris[uri];
    }

// token count per tokenId available for sale
    function tokenCount(uint256 Id) public view returns (uint256) {
        return tokenBalance[Id];
    }

// upon a sale, reduce the token balance for that token

    function updateTokenCount(uint256 Id, uint256 count) public {
        // While selling the token, it shd be checked if there is enough to sell
        // Here we assume that there was enough to sell, so balance will NOT be negative

        tokenBalance[Id] = tokenBalance[Id] - count;
        tokenCollection[Id].availableNow = tokenBalance[Id];

    }
//upon refund, update the token counts

    function updateRefundTokenCount(uint256 Id, uint256 count) public {

        tokenBalance[Id] = tokenBalance[Id] + count;
        tokenCollection[Id].availableNow = tokenBalance[Id];

    }
// number of types of tokens available for sale. For each token there is ONE item in case of a NFT
// and in case of FT (fungible token) there are generally MORE than ONE copies of the same item for that TOKEN
// do not confuse this numberOfTokens from total number of items for sale, which could be significantly large
// for example - you may have 3 NFTs (one item) for special edition picture of MonaLisa, RobertDeniro, Amitabh Bacchan
// while, you may 100 of copies of the poster of BOBBY film. This poster would be one token, but it will have 100 copies.
// so, in this case total numberOfTokens would return 4.

    function numberOfTokens() public view returns (uint256) {
        return tokenId;
    }

    // funds raised amount
    uint256 fundsRaised=0;

// at this point the code is bieng executed by the invester, so the reipient will be owner_address, where the proceeds
// from the sale of tokens shd go
    function payForTokens(uint256 amount, address payable recipient) public payable {
        require(recipient == owner_address , "The recipient address is not authorized!");
        recipient.transfer(amount);
        fundsRaised += amount;
    }

// while refunding the Company is executing this code so msg.sender would be company and the account will be theirs to send from
// so recipient is the investor
    function refundForTokens(uint256 tokenid, uint256 count,  uint256 amount, address payable recipient) public payable {
        recipient.transfer(amount);
        fundsRaised -= amount;
        updateRefundTokenCount(tokenid, count);
    }   
}