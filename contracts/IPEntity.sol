// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/finance/PaymentSplitter.sol";

contract IPEntity is ERC721, Ownable, PaymentSplitter {
    using Counters for Counters.Counter;
    using EnumerableSet for EnumerableSet.AddressSet;
    using EnumerableSet for EnumerableSet.UintSet;

    address payable public _recipient;
    Counters.Counter private _tokenIds;

    // map the URI metadata to the token ID to fetch the right URI
    mapping(uint256 => string) private _uris;

    // Prints minted tokens
    event Minted(int responseCode, address _tokenAddress);

    uint256 private NFTminted;

    // Enum representing token type
    enum DeonticExpression {Permission, Obligation, Prohibition}

    // Mapping for token DeonticExpressions
    mapping(uint256 => DeonticExpression) private _tokenDeonticExpressions;

    // MCO contract structure
    struct MCOContract {
        EnumerableSet.AddressSet parties;
        EnumerableSet.UintSet deonticExpressions;
    }

    mapping(bytes => MCOContract) _contracts;

    // IP Entity unique identifier
    bytes private _identifier;

    constructor(
        string memory name,
        string memory symbol,
        bytes memory identifier,
        address[] memory _payees,
        uint256[] memory _shares
    )
    public ERC721(name, symbol)
    PaymentSplitter(_payees, _shares) payable
    {
        _identifier = identifier;

        // Set the royalty _recipient by:
        // - using the deployer address
        // - this contract address
        // - Scrow contract address
        _recipient = payable(address(this));

        // Counter of initial NFTs minted
        NFTminted = 0;
    }

    // *** Minter functions ***
    // MCO = Media Contract Ontology (MCO) is a standard for describing media contracts
    function newMCOContract(bytes memory contractId, address[] memory parties)
        public
    {
        MCOContract storage cinfo = _contracts[contractId];
        require(cinfo.parties.length() == 0, "Existing contract");

        for (uint256 i = 0; i < parties.length; i++) {
            cinfo.parties.add(parties[i]);
        }
    }

    function newPermission(
        bytes memory contractId,
        address party,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 newItemId = _newToken(contractId, party, tokenURI);

        _tokenDeonticExpressions[newItemId] = DeonticExpression.Permission;

        return newItemId;
    }

    function newObligation(
        bytes memory contractId,
        address party,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 newItemId = _newToken(contractId, party, tokenURI);

        _tokenDeonticExpressions[newItemId] = DeonticExpression.Obligation;

        return newItemId;
    }

    function newProhibition(
        bytes memory contractId,
        address party,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 newItemId = _newToken(contractId, party, tokenURI);

        _tokenDeonticExpressions[newItemId] = DeonticExpression.Prohibition;

        return newItemId;
    }

    // Use onlyOwner modifier = Set the URI for a given token ID by only the owner of the contract
    function _setTokenURI(uint256 tokenId, string memory uri_token)
        public onlyOwner
    {
        // require to validate the URI has not been set before in map of URIs
        require(bytes(_uris[tokenId]).length == 0, "Cannot set uri twice");

        // Save URI associated to token ID in the map
        _uris[tokenId] = uri_token;
    }

    function _newToken(
        bytes memory contractId,
        address party,
        string memory tokenURI
    ) private returns (uint256) {
        _tokenIds.increment();

        uint256 newItemId = _tokenIds.current();
        _mint(party, newItemId);
        _setTokenURI(newItemId, tokenURI);

        MCOContract storage cinfo = _contracts[contractId];
        cinfo.deonticExpressions.add(newItemId);

        return newItemId;
    }

    // *** Royalties functions ***
    function getContractBalance() public onlyOwner view returns (uint256) {

        return address(this).balance;
    }
}
