import requests
import re
import getpass
import datetime
import json
import csv 

#getName is used as a helper for sorting lists by name
def getName(e):
    return e['name']

#getID is used as a helper for sorting lists by id
def getID(e):
    return e['id']



class PyAppdApi:
    def __init__(self, controller, client, secret=None):
        """ Initialize API Object"""
        self.controller = controller
        self.accountName = self.getAccountName()
        self.client = f"{client}@{self.accountName}"
        self.secret = secret
        if self.secret == None:
            self.secret = getpass.getpass("Enter Client Secret")
        self.expiration = datetime.datetime.now()
        self.url = "/controller/rest/applications"
        self.token = None

    @staticmethod
    def searchArray(array, key, value):
        for keyval in array:
            if value == keyval[key]:
                return keyval

    def getAccountName(self):
        '''
        Our controllers are multi-tenant and the FQDN is actually an alias to server.  
        Any authentication requires an account name
        '''
        regex = r"https:\/\/(.*?)\."
        accountName = re.search(regex, self.controller).group(1)
        return accountName
    
    #getToken - get a token that can be used for subsequent requests
    def getToken(self):
        if self.secret == None:
            self.secret = getpass.getpass("Enter Client Secret")
        headers = {"Content-Type": "application/vnd.appd.cntrl", "v": "1"}
        payload = {"grant_type": "client_credentials", "client_id": self.client, "client_secret": self.secret}
        self.token = requests.request("POST", f"{self.controller}/controller/api/oauth/access_token", headers=headers, data=payload).json()
        self.expiration =  datetime.datetime.now() + datetime.timedelta(seconds=self.token['expires_in'])
        return f"Token expires at: {self.expiration.ctime()}"
    
    def jsonPayload(f):
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    
    def getAuthHeader(self):
        if datetime.datetime.now() > self.expiration:
            self.getToken()
        return {"Authorization": "Bearer " + self.token['access_token']}
    
    #GET THE LIST OF APPLICATIONS  authHeader = {"Authorization": "Bearer " + token['access_token']}
    def getApps(self, timeRange=None):
        headers = self.getAuthHeader()
        apps = requests.request("GET", self.controller+self.url+"?output=JSON", headers=headers).json()
        apps.sort(key=getName)
        return apps
    
    def getTiers(self, app, timeRange=None):
        tierURL = self.controller+self.url+"/"+str(app['id'])+"/tiers?output=JSON"
        headers = self.getAuthHeader()        
        tiers = requests.request("GET", tierURL, headers=headers).json()
        tiers.sort(key=getName)
        return tiers

    def getNodes(self, app,tier=None,timeRange=None):
        '''
        getNodes:
        returns a list of nodes for a specific application or app/tier.  Optionally, will use a timeframe and return only nodes
        are active during the specified time frame.
        '''
        headers = self.getAuthHeader()
        if tier != None:
            nodeURL = f"{self.controller}{self.url}/{app['id']}/tiers/{tier['name']}/nodes?output=JSON"
        else:
            nodeURL = f"{self.controller}{self.url}/{app['id']}/nodes?output=JSON"
        if timeRange != None:
            nodeURL += f"&time-range-type=BEFORE_NOW&duration-in-mins={timeRange}"
        # todo Log nodeURL
        nodes = requests.request("GET", nodeURL, headers=headers).json()
        #todo log status
        return nodes
    
    #getJVMDetailsForNode
    def getJVMDetailsForNode(self, node, timeRange=None):
        headers = self.getAuthHeader()
        nodeURL = f"{self.controller}/controller/restui/nodeUiService/appAgentByNodeId/{node['id']}"
        if timeRange != None:
            nodeURL += f"&time-range-type=BEFORE_NOW&duration-in-mins={timeRange}"
        # todo Log nodeURL
        nodeJVMDetail = requests.request("GET", nodeURL, headers=headers).json()
        #todo log status
        return nodeJVMDetail    
    
    
    #getEvents
    def getEvents(self, app, eventTypes, timeRange=1440):
        headers = self.getAuthHeader()
        url = f"{self.controller}{self.url}/{app['id']}/events?output=JSON"
        url += f"&event-types={eventTypes}"
        url += f"&severities=WARN,ERROR"
        if timeRange != None:
            url += f"&time-range-type=BEFORE_NOW&duration-in-mins={timeRange}"
        events = requests.request("GET", url, headers=headers)
        #todo log status
        return events