import requests


"""
This piece of code was provided by Valerij. It takes two lists of results (random, ai) and prints
statistics and scores based on those results.
"""
def welch(list1, list2):
    params = {"results": str(list1) + " " + str(list2), "raw": "1"}
    resp = requests.post('http://folk.ntnu.no/valerijf/6/', data=params)
    return resp.text
