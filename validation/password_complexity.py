import re

# function to validate password
# must have at least 12 characters in length, and
# include at least 1 uppercase character,
# 1 lowercase character, 1 number and 1 special character.
def is_password_complex(password):
    if len(password) < 12:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*]", password):
        return False
    return True


# function to validate password
# must have at least 12 characters in length, and
# include at least 1 uppercase character,
# 1 lowercase character, 1 number and 1 special character.
def validate_password(password):
    """
    This function validates user password complexity
    """
    # create regex
    validpwd = (
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!#%*?&]{12,25}$"
    )
    pattern = re.compile(validpwd)
    # call method search to compare
    match = re.search(pattern, password)
    testval = False
    # validating conditions
    if match:
        testval = True
    return testval


# function to compare pwds
def compare(newpwd):
    """
    This function compares passwords
    with a list of compromised passwords
    """
    testcompare = True
    resultcompare = True
    # read file
    fcp = open("static/CommonPassword.txt", "r")
    data = fcp.readlines()
    fcp.close()
    # loop through data and compare
    while testcompare:
        for item in data:
            # test user pwd with a list
            if newpwd == item.strip():
                testcompare = False
                resultcompare = False
                # return false if found
                return resultcompare
        # return true if not found
        return resultcompare
    
    
    # writes to the file new updated pwd
def update_password(repl):
    """
    This function creates and updates
    user password
    """
    # create new file and add new pwd of the user
    with open("static/newdata.txt", "a+") as newreset:
        newreset.write("%s\n" % (repl))
