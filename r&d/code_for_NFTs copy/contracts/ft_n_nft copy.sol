// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts@4.7.3/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts@4.7.3/access/AccessControl.sol";

contract Bolly is ERC1155, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    constructor() ERC1155("") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
    }

    // NftMetaData for NFT assigned to n investor
    struct nftInfo {
        address owner; //who owns it
        uint256 value;  //price for this one
        uint256 amount; //how many of this nft
        string uri;  //uri of the. token

    }
    mapping(uint256 => nftInfo) public tokenCollection;
    uint256 tokenId;

    mapping (uint256 => string) private _uris;

    //defined to set uri for each token. this function used t b there in earlier versions



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

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC1155, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }



    function registerToken(
        address owner,  //who owns
        // the below two items not needed as we r handling it in the streamlit interface
        //string memory filmName, //film name 
       // string memory nftItem,  //nftitem name
        uint256 initialPrice, //price
        uint256 howMany,  //how many
        string memory nftURI,  //uri of the nft
        bytes memory data //associated data if any. 0x0000 if not
    ) public returns (uint256) {
        //uint256 tokenId;

        tokenId +=1; 

         _mint(owner, tokenId, howMany, data);
         //_setURI(nftURI);

        tokenCollection[tokenId] = nftInfo(owner, initialPrice, howMany, nftURI);

        return tokenId;
    }
}
