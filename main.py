#!/usr/bin/env python
"""CMPSC 200 Quiz/Assesment IP Filter Updater

This program is to be executed as part of a scheduled group of jobs to update
the IPs for each section on the specific days. The program itself does not manage
the times that the program is launched.

Setup: Before running this program, make sure you've grabbed all relevant course
and quiz/assessment ID's as detailed in the README.

On Unix Systems, set up cron jobs for each section.
On Windows systems, use the Task scheduler to schedule the execution.

Usage: python ipchanger.py <quiz/assessment> <section number>

Configure your preferred scheduler to launch the scripts as follows.
At 7:55 on Wednesdays launch the script: python ipchanger.py quiz 1
At 9:00 on Wednesdays launch the script: python ipchanger.py quiz 2
At 10:05 on Wednesdays launch the script: python ipchanger.py quiz 3
...
At 4:20 on Wednesdays launch the script: python ipchanger.py quiz 8

At 7:55 on Fridays launch the script: python ipchanger.py assessment 1
At 9:00 on Fridays launch the script: python ipchanger.py assessment 2
At 10:05 on Fridays launch the script: python ipchanger.py assessment 3
...
At 4:20 on Fridays launch the script: python ipchanger.py assessment 8

Once the scheduler and configuration JSON files are set up, you shouldn't need 
to touch this anymore. Make SURE(!) that the station that is launching the
program will be ON and connected to the internet, otherwise you'll have to deal
with make-ups.

The first time you try this I suggest double checking before each section to
ensure that it has been setup properly. 
"""
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json
import sys


def set_quiz(filename, section, token):
    """Sets the IP filter for the section specified, the quiz id is determined
    by the lastQuiz attribute from the JSON file.

    Function itself makes a PUT request to the canvas api ( THIS MAY CHANGE IN THE FUTURE )
    """
    (url, quizID, IP) = get_quiz_data(filename, 'Quiz', section)
    newdata={"quiz[notify_of_update]": 0, "quiz[ip_filter]":"{}".format(IP)}
    req = Request('{}/{}?access_token={}'.format(url,quizID,token), method='PUT')

    with urlopen(req, urlencode(newdata).encode('utf-8')) as resp:
        return resp.getcode()

def get_quiz_data(filename, quiz_type, section):
    """Returns the base url, quiz id, and IP for the quiz type (meaning
    assessment or quiz) and section.
    """
    with open(filename,'r') as f:
        data = json.load(f)

    url = 'https://psu.instructure.com/api/v1/courses/{}/quizzes/'.format(data['courseID'])

    idx = 'last{}'.format(quiz_type)
    quiznum= data[idx]
    idlist='{}IDList'.format(quiz_type.lower())
    quizID = data[idlist][quiznum]

    print("Setting quiz {}".format(quizID))
    IP = get_room_ip(data, section)

    return (url, quizID, IP)

def set_assessment(filename, section, token):
    """Sets the IP filter for the section specified, the quiz id is determined
    by the lastAssessment attribute from the JSON file.

    Function itself makes a PUT request to the canvas api ( THIS MAY CHANGE IN THE FUTURE )
    """
    (url, assessmentIDs, IP) = get_quiz_data(filename, 'Assessment', section)

    for quizID in assessmentIDs:
        newdata={"quiz[notify_of_update]": 0, "quiz[ip_filter]":"{}".format(IP)}
        req = Request('{}/{}?access_token={}'.format(url,quizID,token), method='PUT')

        with urlopen(req, urlencode(newdata).encode('utf-8')) as resp:
            print(resp.getcode())


def get_room_ip(data,section):
    """ Extracts the IP for that section from the JSON """
    room_name = data['room'][section]
    IP = data[room_name]
    return IP

def write_new_json(quiz_type, filename):
    """Updates the configuration JSON file
    Depending on the quiz_type the script was called with, updates either the
    lastQuiz or lastAssessment variables from the JSON file
    """
    with open(filename, 'r') as f:
        data = json.load(f)

    if test_type == 'quiz':
        data['lastQuiz'] = data['lastQuiz'] + 1
    elif test_type == 'assessment':
        data['lastAssessment'] = data['lastAssessment'] + 1
    with open(filename, 'w') as f:
        json.dump(data,f, indent=4)
    return


if __name__ == '__main__':
    with open('token', 'r') as f:
        token = f.readline()

    if len(sys.argv) != 3:
        print("You need to enter a section number!")
        print("USAGE: python {} type section#".format(sys.argv[0]))

    datafile = 'quizzes.json'
    test_type = sys.argv[1]
    section = int(sys.argv[2])

    # Only update lastQuiz/Assessment when running script for section 1
    if section == 1:
        write_new_json(test_type, datafile)


    if test_type == 'quiz':
        print(set_quiz(datafile, section, token))
    elif test_type == 'assessment':
        set_assessment(datafile, section, token)
