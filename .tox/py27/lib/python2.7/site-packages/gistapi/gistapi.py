# coding=utf-8
"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""
from bson.json_util import loads, dumps
import requests, re, json
from flask import Flask, jsonify, request, abort
from pymongo import MongoClient

# *The* app object
app = Flask(__name__)

def pagenate(items, page = 0, per_page = 2):
    try:
        return items[(page*per_page):(page*per_page + per_page)]
    except:
        return items

@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"

@app.errorhandler(404)
def user_not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route("/users/<username>")
def gists_for_user(username):
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    gists_url = 'https://api.github.com/users/{username}/gists'.format(
            username=username)
    # print gists_url
    response = requests.get(gists_url)
    gist_list = json.loads(response.content)
    print "gist length",len(gist_list)
    # print response.content
    # BONUS: What failures could happen?
    # BONUS: Paging? How does this work for users with tons of gists?
    if response.status_code==200:
        page = int(request.args.get('page') or 0)
        per_page = int(request.args.get('per_page') or 5)
        resutls = pagenate(json.loads(response.content), page=page, per_page=per_page)
        return json.dumps(resutls)
    else:
        return abort(404)


@app.route("/api/v1/search", methods=['POST'])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data = request.get_json()
    # BONUS: Validate the arguments?
    if not post_data or not 'username' in post_data or not 'pattern' in post_data:
        print "this is invalid arguments test"
        abort(400)

    username = post_data['username']
    pattern = post_data['pattern']

    result = {}
    gists =json.loads(gists_for_user(username))
    matche_result=[]
    # BONUS: Handle invalid users?

    for gist in gists:
            for file_name,file_dict in gist['files'].iteritems():
                gistfile_raw_url = file_dict['raw_url']
                print "######", gistfile_raw_url
                m = re.search(r""+pattern, requests.get(gistfile_raw_url).text)
                if m is not None:
                    matche_result.append(gist['html_url'])                 
                              
        # REQUIRED: Fetch each gist and check for the pattern
        # BONUS: What about huge gists?
        # BONUS: Can we cache results in a datastore/db?
        #pass
    
    result['status'] = 'success'
    result['username'] = username
    result['pattern'] = pattern
    result['matches'] = matche_result

    #the follow code is used to store the match result into MongoDB,
    #if you want to test this, make sure MongoDB has been installed
    # and MongoDB service is running

    # client = MongoClient("mongodb://localhost:27017")
    # db = client.python_test
    # db.match_result.insert_one(loads(dumps(result))).inserted_id
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
