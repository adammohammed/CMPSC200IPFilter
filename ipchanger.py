##
# @package ipchanger
#
# This is a set of functions which can be used to update existing quiz and
# assessments IP filters based on the section.
#

from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json

## Sets the IP filter for the section specified based on the lastQuiz value from the JSON.
#
# Function itself makes a PUT request to the canvas api ( THIS MAY CHANGE IN THE FUTURE )
# @param filename is the configuration JSON filename in which the quiz data can be found.
# @param section is the number of the section (i.e. 1 - 8). This will be used to set the IP.
# @param token is the string of characters given to you by Canvas for development.
#
def set_quiz(filename, section, token):
    (url, quizID, IP) = get_quiz_data(filename, 'Quiz', section)
    newdata={"quiz[notify_of_update]": 0, "quiz[ip_filter]":"{}".format(IP)}
    req = Request('{}/{}?access_token={}'.format(url,quizID,token), method='PUT')

    with urlopen(req, urlencode(newdata).encode('utf-8')) as resp:
        return resp.getcode()

## Returns the base URL, quiz id, and IP corresponding to the section and quiz type specified.
#
#  This function will open and read the contents of the file specified for the quiz information
#  @param filename is the name of the JSON configuration file with the quiz information.
#  @param quiz_type is specified as either "quiz" or "assessment" to determine which IDs to scan through.
#  @param section is the number of the section to be used to identify the corresponding IP for the location.
#
def get_quiz_data(filename, quiz_type, section):
    with open(filename,'r') as f:
        data = json.load(f)

    url = 'https://psu.instructure.com/api/v1/courses/{}/quizzes/'.format(data['courseID'])

    idx = 'last{}'.format(quiz_type)
    quiznum= data[idx]
    idlist='{}IDList'.format(quiz_type.lower())
    quizID = data[idlist][quiznum-1]

    print("Setting quiz {}".format(quizID))
    IP = get_room_ip(data, section)

    return (url, quizID, IP)

## Sets the IP filter for the section specified, as defined by lastAssessment in JSON.
#
# Function itself makes a PUT request to the canvas api ( THIS MAY CHANGE IN THE FUTURE )
# @param filename is the configuration JSON filename in which the quiz data can be found.
# @param section is the number of the section (i.e. 1 - 8). This will be used to set the IP.
# @param token is the string of characters given to you by Canvas for development.
#
def set_assessment(filename, section, token):
    (url, assessmentIDs, IP) = get_quiz_data(filename, 'Assessment', section)

    for quizID in assessmentIDs:
        newdata={"quiz[notify_of_update]": 0, "quiz[ip_filter]":"{}".format(IP)}
        req = Request('{}/{}?access_token={}'.format(url,quizID,token), method='PUT')

        with urlopen(req, urlencode(newdata).encode('utf-8')) as resp:
            print(resp.getcode())


## Extracts the IP for that room/section combination from the in-memory JSON object
#
def get_room_ip(data,section):
    room_name = data['room'][section-1]
    IP = data[room_name]
    return IP

## Updates the configuration JSON file
#  Depending on the quiz_type the script was called with, updates either the
#  lastQuiz or lastAssessment variables from the JSON file
#  @param quiz_type is specified as either "quiz" or "assessment" to determine which IDs to update.
#  @param filename is the configuration JSON filename in which the quiz data can be found.
#
def write_new_json(quiz_type, filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    if quiz_type == 'quiz':
        data['lastQuiz'] = data['lastQuiz'] + 1
    elif quiz_type == 'assessment':
        data['lastAssessment'] = data['lastAssessment'] + 1
    with open(filename, 'w') as f:
        json.dump(data,f, indent=4)
    return
