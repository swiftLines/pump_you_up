# function to check if already user registered
def checknotreg(username):
    """
    This function validates if user already registered
    """
    # declare vars
    testreg = True
    resultreg = True
    # open and read file
    usercheck = open("static/newdata.txt", "r")
    # read all the lines
    usercheckdata = usercheck.readlines()
    # close the file
    usercheck.close()
    # loop through until find user
    while testreg:
        # Read the lines
        for line in usercheckdata:
            # Split on the space, and store the results in a list of two strings
            userdata_info = line.split()
            #user = userdata_info[0]
            # print(userdata_info)
            # print(userdata_info[0])
            # test if user exists
            if username in userdata_info:
                # if yes, stop the loop
                testreg = False
                resultreg = False
                # return result is false
                return resultreg
        # return result to registrsation function
        return resultreg
    