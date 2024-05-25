// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

contract pilotDataContract {
    struct pilot {
        uint256 id;
        string name;
        string FlightDescription;
        uint256 result;
        uint256 flight age; 
    }

    pilot[] public pilots;
    uint256 public nextpilotId;

    function addpilot(
        string memory _name,
        string memory _FlightDescription,
        uint256 _result,
        uint256 _flight age
    ) public {
        pilots.push(pilot(nextpilotId, _name, _FlightDescription, _result, _flight age));
        nextpilotId++;
    }

    function getpilotsCount() public view returns (uint256) {
        return pilots.length;
    }

    function getpilotById(uint256 _id) public view returns (pilot memory) {
        require(_id < pilots.length, "pilot ID does not exist");
        return pilots[_id];
    }

    function updatepilot(
        uint256 _id,
        string memory _name,
        string memory _FlightDescription,
        uint256 _result,
        uint256 _flight age
    ) public {
        require(_id < pilots.length, "pilot ID does not exist");
        pilots[_id].name = _name;
        pilots[_id].FlightDescription = _FlightDescription;
        pilots[_id].result = _result;
        pilots[_id].flight age = _flight age;
    }

    function deletepilot(uint256 _id) public {
        require(_id < pilots.length, "pilot ID does not exist");
        pilots[_id] = pilots[pilots.length - 1];
        pilots.pop();
    }
}

contract StringArrayContract {
    string[] public stringArray;

    function setStringArray(string[] memory _array) public {
        stringArray = _array;
    }

    function getStringArray() public view returns (string[] memory) {
        return stringArray;
    }
}