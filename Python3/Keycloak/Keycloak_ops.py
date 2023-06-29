import requests
import json
import configparser
config = configparser.ConfigParser()
config.read('variables.ini')

###########################
import logging

# Debug logging

logging.basicConfig()
logging.getLogger("requests").setLevel(logging.DEBUG)
from http.client import HTTPConnection
HTTPConnection.debuglevel = 0


def getAuthToken():
    tknFtchURL  = config.get("Settings","Baseurl")+config.get("Settings","tokeURI")
    payload = "grant_type=client_credentials&client_id="+config.get("Settings","client_id")+"&client_secret="+config.get("Settings","client_secret")
    authTokenresponse = requests.request("POST", tknFtchURL, headers = {'Content-Type': 'application/x-www-form-urlencoded','Accept': 'application/json'}, data=payload)
    if authTokenresponse.status_code == 200:
        return((authTokenresponse.json()['access_token']))
    else:
        print("Something went wrong\n Status Code: {0}\n Error :{1}\n".format(authTokenresponse.status_code,authTokenresponse.content))


def getUsers():
    getUsrlistURL = config.get("Settings","Baseurl")+config.get("Settings","userURI")
    authToken = getAuthToken()
    users_list_resp = requests.request("GET", getUsrlistURL, headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': "Bearer "+ authToken})
    print(users_list_resp.status_code)
    userlist = []
    for usr in users_list_resp.json():
        userlist.append(usr['username'])
    print("The list of users in the system\n" + str(userlist))

def getUserAttr(username,flexible,getID):
    getUsrlistURL = config.get("Settings","Baseurl")+config.get("Settings","userURI")+"?q=username:"+str(username)+"&exact="+flexible
    authToken = getAuthToken()
    user_attr = requests.request("GET", getUsrlistURL, headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': "Bearer "+ authToken})
    if getID == "yes":
        return (user_attr.json()[0]['id'])
    else:
        print("The user details is as below")
        print(json.dumps(user_attr.json(), indent=4))

def getGrplist():
    getGrplistURL = config.get("Settings","Baseurl")+config.get("Settings","grpsURI")
    print(getGrplistURL)
    authToken = getAuthToken()
    kc_grps = []
    grp_list = requests.request("GET", getGrplistURL, headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': "Bearer "+ authToken})
    for grps in grp_list.json():
        kc_grps.append(grps['name'])
    print("The Group list is as below")
    print(kc_grps)

def getUserGrplist(username,flexible):
    authToken = getAuthToken()
    userID = getUserAttr(username,flexible,"yes")
    print("authToken {} \n userID {}\n".format(authToken,userID))
    getGrplistURL = config.get("Settings","Baseurl")+config.get("Settings","userURI")+"/"+userID+"/groups"
    print(getGrplistURL)
    grp_list = requests.request("GET", getGrplistURL, headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': "Bearer "+ authToken})
    userGrplist = []
    for grps in grp_list.json():
        userGrplist.append(grps['name'])
    print("The User Group list for member {} is as below.".format(username))
    print(userGrplist)



Choice = int(input('''###############################
What would you like to do
1)Get User list
2)Get User details
3)Get Groups
4)Get Token
5)Get User Group Membership
###############################\n'''))

match Choice:
    case 1:
        getUsers()
    case 2:
        username = "someone"
        #username =input("The name of the user you wish to dig\n")
        flexible = input("Strictly look of an exact match? true or false\n")
        getUserAttr(username,flexible,"No")
    case 3:
        getGrplist()
    case 4:
        print("AuthToken\n" + str(getAuthToken()))
    case 5:
        username = "someone"
        flexible = "false"
        #username =input("The name of the user you wish to dig\n")
        #flexible = input("Strictly look of an exact match? true or false\n")
        getUserGrplist(username,flexible)
    case _:
        print("I knew you were clueless")



