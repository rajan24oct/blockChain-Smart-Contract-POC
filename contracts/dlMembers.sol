pragma solidity ^0.4.21;

import "stringUtils.sol";

contract memberRecords {

    enum genderType {male, female}
    struct user {
        string name;
        genderType gender;
        string email;

    }

    // user object
    // you can also declare it public to access it from outside contract
    // https://solidity.readthedocs.io/en/v0.4.24/contracts.html#visibility-and-getters
    user user_obj;

    function getGenderFromString(string gender) internal returns (genderType) {
        if (StringUtils.equal(gender, "male")) {
            return genderType.male;
        } else {
            return genderType.female;
        }
    }

    // Internal function to conver genderType enum to string
    function getGenderToString(genderType gender) internal returns (string) {
        if (gender == genderType.male) {
            return "male";
        } else {
            return "female";
        }
    }

    // set user public function
    // This is similar to persisting object in db.
    function setUser(string name, string gender, string email) public {
        genderType gender_type = getGenderFromString(gender);
        user_obj = user({
            name : name, gender : gender_type, email: email

            });
    }

    // get user public function
    // This is similar to getting object from db.
    function getUser() public returns (string, string, string) {
        return (
        user_obj.name, getGenderToString(user_obj.gender), user_obj.email
        );
    }


}
