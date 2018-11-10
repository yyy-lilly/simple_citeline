import requests
import json
import sys


class Error(Exception):
    """An Error was encounter"""
    pass


class noSchemaFound(Error):
    """Raised when trying to find schema that does not exist"""
    pass


def citelineConnection(citeuser: object, citepass: object, citeauth: object) -> object:

    url = "https://identity.pharmaintelligence.informa.com/connect/token"

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"grant_type\"\r\n\r\npassword\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"username\"\r\n\r\n" + str(citeuser) + "\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"password\"\r\n\r\n" + str(citepass) + "\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"scope\"\r\n\r\ncustomer-api\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Authorization': "Basic " + str(citeauth),
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response)
    return json.loads(response.text)['access_token']

class queryApi:

    avail_schema = ["drug", "trial", "investigator", "organization", "drugevent", "drugcatalyst"]
    trial_search = ["id", "diseasehierachy", "phase", "status", "sponsorname", "sponsorname", "sponsortype",
                    "trialstartdate", "trialstartdatefrom", "trialstartdateto", "protocolid", "source", "country",
                    "region", "trialMeshTerm", "trialTag", "moa", "drugName", "drugid", "trialPrimaryCompletionDate"]

    def checkTerms(schema, search):
        """Return True if passing all tests"""
        if schema not in queryApi.avail_schema:
            return False
        for items in search:
            if items not in queryApi.trial_search:
                return False
        return True

    def makeHeader(citeconn):
        headers = {
            'Accept': "application/json",
            'Authorization': "Bearer " + str(citeconn),
            'Cache-Control': "no-cache"
        }
        return headers

    def citelineGetPermissions(citeconn):
        result = []

        for item in queryApi.avail_schema:
            url = "https://api.pharmaintelligence.informa.com/v1/feed/" + item + "/schema"
            headers = queryApi.makeHeader(citeconn)
            localResponse = json.loads(requests.request("GET", url, headers=headers).text)
            try:
                result.append([item, "Permission Fail", localResponse['meta']['message']])
            except:
                result.append([item, "Permission OK"])

        return result

    def citelineSchema(s_type, citeconn, has_page=0):

        print(s_type)
        if s_type not in queryApi.avail_schema:
            raise noSchemaFound("type not found in schema list")
        if has_page == 0:
            url = "https://api.pharmaintelligence.informa.com/v1/feed/" + str(s_type) + "/schema"
        else:
            url = has_page
        headers = {
            'Accept': "application/json",
            'Authorization': "Bearer " + str(citeconn),
            'Cache-Control': "no-cache"
        }

        localResponse = json.loads(requests.request("GET", url, headers=headers).text)
        return localResponse


    # helpful tip: has_page is a URL that citeline passes back under ['pagination']['nextPage'], it contains
    # all original query parameters

    def citelineFeed(s_type, citeconn, has_page=0):

        print("Getting " + str(s_type) + ", this may take a while")
        if s_type not in queryApi.avail_schema:
            raise noSchemaFound("type not found in schema list")
        if has_page == 0:
            url = "https://api.pharmaintelligence.informa.com/v1/feed/" + str(s_type)
        else:
            url = has_page
        headers = {
            'Accept': "application/json",
            'Authorization': "Bearer " + str(citeconn),
            'Cache-Control': "no-cache"
        }
        localResponse = json.loads(requests.request("GET", url, headers=headers).text)
        print(str(sys.getsizeof(str(localResponse))/1000/1000) + " MB")
        return localResponse

    # Search any asset for a key value pair
    # most improvements will happen here
    def citelineSearch(s_type, search_term, citeconn, has_page=0):

        print("Getting " + str(s_type) + ", this may take a while")
        if s_type not in queryApi.avail_schema:
            raise noSchemaFound("type not found in schema list")
        if has_page == 0:
            url = "https://api.pharmaintelligence.informa.com/v1/search/" + str(s_type)
        else:
            url = has_page

        querystring = search_term

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

        headers = {
            'Accept': "application/json",
            'Authorization': "Bearer " + str(citeconn),
            'Cache-Control': "no-cache"
        }
        localResponse = json.loads(requests.request("GET", url, data=payload, headers=headers, params=querystring).text)
        print(str(sys.getsizeof(str(localResponse))/1000/1000) + " MB")
        return localResponse
