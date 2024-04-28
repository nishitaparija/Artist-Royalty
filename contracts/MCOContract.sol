// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./NFToken.sol";
import "./EnumerableMapAddressToUint.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
//import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";
//import "@openzeppelin/contracts/finance/PaymentSplitter.sol";

contract MCOContract is Ownable {
    using SafeMath for uint256;
    using EnumerableSet for EnumerableSet.AddressSet;
    using EnumerableSet for EnumerableSet.UintSet;
    using EnumerableMap for EnumerableMap.AddressToUintMap;

    // Contract unique identifier
    bytes private _identifier;
    // Contract parties address string map array in Ripple
    // EnumerableSet.AddressSet _parties;
    string[] public _parties;
    // Contract deontic expression NFtoken
    NFToken public _nfToken;
    // Contract deontic expressions token id
    EnumerableSet.UintSet _deonticExpressions;
    // Contract objects token id
    EnumerableSet.UintSet _objects;
    // Contract relations with other contracts
//    EnumerableMap.AddressToUintMap _contractRelations;
    struct ContractInfo {
        string contractAddress;
        uint256 relation;
        }
    mapping(string => ContractInfo) private _contractRelations;
    // Contract related income percentages for payments
//    mapping(address => EnumerableMap.AddressToUintMap) _incomePercentages;
    // Contract content URI
    string public _contentUri;
    // Contract content HASH
    bytes public _contentHash;
    // Add a mapping to keep track of income owned
    mapping(string => uint256) private _incomeOwned;
    // Define the royalty _recipient:
    address payable public _recipient;
    // Define the income beneficiary addresses in a string array
    string[] public _incomeBeneficiaries;
//    address[] public _incomeBeneficiaries;
    // Define the income percentages for each beneficiary
    uint256[] public _incomePercentages;

    constructor(
        bytes memory identifier,
        string[] memory parties,
        NFToken nfToken,
        uint256[] memory deonticExpressionsIds,
        uint256[] memory objects,
        string[] memory relatedContracts,
        uint256[] memory relations,
        string[] memory incomeBeneficiaries,
        uint256[] memory incomePercentages,
        string memory contentUri,
        bytes memory contentHash
    )
    {
        // Set the royalty _recipient by:
        // - using the deployer address
        // - this contract address
        // - Scrow contract address
        _recipient = payable(address(this));

        _identifier = identifier;

        for (uint256 i = 0; i < parties.length; i++) {
            _parties.push(parties[i]);
        }
        _nfToken = nfToken;
        for (uint256 i = 0; i < deonticExpressionsIds.length; i++) {
            _deonticExpressions.add(deonticExpressionsIds[i]);
        }
        for (uint256 i = 0; i < objects.length; i++) {
            _objects.add(objects[i]);
        }
        // Update the _contractRelations mapping with a for loop
        for (uint256 i = 0; i < relatedContracts.length; i++) {
            _contractRelations[relatedContracts[i]] = ContractInfo(relatedContracts[i], relations[i]);
        }
//        for (uint256 i = 0; i < incomePercentages.length; ) {
//            EnumerableMap.AddressToUintMap storage incomeMap =
//                _incomePercentages[incomeBeneficiaries[i]];
//            uint256 shares = incomePercentages[i++];
//            for (uint256 j = 0; j < shares; j++) {
//                incomeMap.set(incomeBeneficiaries[i], incomePercentages[i++]);
//            }
//        }
        _incomeBeneficiaries = incomeBeneficiaries;
        _incomePercentages = incomePercentages;
        _contentUri = contentUri;
        _contentHash = contentHash;
    }

    // @dev Returns all the contract parties
    function getParties() public view returns (string[] memory) {
        return _parties;
    }

    // @dev Returns all the income beneficiaries
    function getIncomeBeneficiaries() public view returns (string[] memory) {
        return _incomeBeneficiaries;
    }

    function getDeonticExpressions() public view returns (uint256[] memory) {
        uint256[] memory deontics = new uint256[](_deonticExpressions.length());
        for (uint256 i = 0; i < _deonticExpressions.length(); i++) {
            deontics[i] = _deonticExpressions.at(i);
        }

        return deontics;
    }

    function getObjects() public view returns (uint256[] memory) {
        uint256[] memory objects = new uint256[](_objects.length());
        for (uint256 i = 0; i < _objects.length(); i++) {
            objects[i] = _objects.at(i);
        }

        return objects;
    }

    // @dev Returns all the contract relations stored in the mapping _contractRelations
    function getContractRelations() public view returns (string[] memory, uint256[] memory) {
        string[] memory relatedContracts = new string[](_parties.length);
        uint256[] memory relations = new uint256[](_parties.length);
        for (uint256 i = 0; i < _parties.length; i++) {
            relatedContracts[i] = _contractRelations[_parties[i]].contractAddress;
            relations[i] = _contractRelations[_parties[i]].relation;
        }

        return (relatedContracts, relations);
    }

//    function getIncomePercentagesBy(address sharer)
//        public
//        view
//        returns (address[] memory, uint256[] memory)
//    {
//        return _incomePercentages[sharer].getAll();
//    }

    // *** Royalties functions ***
    function getContractBalance() public onlyOwner view returns (uint256) {

        return address(this).balance;
    }

    // @dev Keep track of the income owned to each incomeBeneficiaries address
    // based on the income percentage
    function updateIncomeOwned(uint256 amount) public onlyOwner {
        uint256 l = _incomeBeneficiaries.length;
        for (uint256 i = 0; i < l; i++) {
            string memory incomeBeneficiary = _incomeBeneficiaries[i];
            uint256 incomePercentage = _incomePercentages[i];
            uint256 incomeAmount = amount.mul(incomePercentage).div(100);
            _incomeOwned[incomeBeneficiary] = _incomeOwned[incomeBeneficiary].add(incomeAmount);
        }
    }

    // @dev Reduce the income owned to an specific incomeBeneficiary address
    function reduceIncomeOwned(string memory incomeBeneficiary, uint256 amount) public onlyOwner {
        _incomeOwned[incomeBeneficiary] = _incomeOwned[incomeBeneficiary].sub(amount);
    }

    // @dev Get income owned to an specific incomeBeneficiary address
    function getIncomeOwned(string memory incomeBeneficiary) public onlyOwner view returns (uint256) {
        return _incomeOwned[incomeBeneficiary];
    }

    // @dev Update the income percentage for an incomeBeneficiary address
    function updateIncomePercentage(string memory incomeBeneficiary, uint256 incomePercentage) public onlyOwner {
        uint256 l = _incomeBeneficiaries.length;
        for (uint256 i = 0; i < l; i++) {
            if (keccak256(abi.encodePacked(_incomeBeneficiaries[i])) == keccak256(abi.encodePacked(incomeBeneficiary))) {
                _incomePercentages[i] = incomePercentage;
            }
        }
    }

    // @dev Get income percentage for an incomeBeneficiary address
    function getIncomePercentage(string memory incomeBeneficiary) public onlyOwner view returns (uint256) {
        uint256 l = _incomeBeneficiaries.length;
        for (uint256 i = 0; i < l; i++) {
            if (keccak256(abi.encodePacked(_incomeBeneficiaries[i])) == keccak256(abi.encodePacked(incomeBeneficiary))) {
                return _incomePercentages[i];
            }
        }
    }


}
