// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts@4.7.3/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts@4.7.3/access/AccessControl.sol";
import "@openzeppelin/contracts@4.7.3/security/Pausable.sol";
import "@openzeppelin/contracts@4.7.3/token/ERC1155/extensions/ERC1155Supply.sol";

contract NFTs is ERC1155, AccessControl, Pausable, ERC1155Supply {
    bytes32 public constant URI_SETTER_ROLE = keccak256("URI_SETTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    // NftMetaData for NFT assigned to n investor
    struct nftInfo {
        address owner; //who owns it
        uint256 value;  //price for this one
        uint256 amount; //how many of this nft

    }
    mapping(uint256 => nftInfo) public artCollection;
    uint256 tokenId;

    mapping (uint256 => string) private _uris;


    constructor() ERC1155("") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(URI_SETTER_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
    }

    //defined to set uri for each token. this function used t b there in earlier versions

    function setTokUri(uint256 tokenId, string memory uri) public {
        _uris[tokenId] = uri;
    }

    //OVERridden the default uri function to return the uri for each token

    function uri(uint256 tokenId) override public view returns (string memory) {
        return (_uris[tokenId]);
    }

    function setURI(string memory newuri) public onlyRole(URI_SETTER_ROLE) {
        _setURI(newuri);
    }

    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }

    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
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

    function _beforeTokenTransfer(address operator, address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        internal
        whenNotPaused
        override(ERC1155, ERC1155Supply)
    {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
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


    function registerNFT(
        address owner,  //who owns
        // the below two items not needed as we r handling it in the streamlit interface
        //string memory filmName, //film name 
       // string memory nftItem,  //nftitem name
        uint256 initialValue, //price
        uint256 amount,  //how many
        string memory nftURI,  //uri of the nft
        bytes memory data //associated data if any. 0x0000 if not
    ) public returns (uint256) {
        //uint256 tokenId;

        tokenId +=1; 

         _mint(owner, tokenId, amount, data);
         _setURI(nftURI);

        artCollection[tokenId] = nftInfo(owner, initialValue, amount);

        return tokenId;
    }
}
