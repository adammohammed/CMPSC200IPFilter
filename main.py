#!/usr/bin/env python
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json
import sys


def set_quiz(filename, section, token):
    (url, quizID, IP) = get_quiz_data(filename, 'Quiz', section)
    newdata={"quiz[notify_of_update]": 0, "quiz[ip_filter]":"{}".format(IP)}
    req = Request('{}/{}?access_token={}'.format(url,quizID,token), method='PUT')

    with urlopen(req, urlencode(newdata).encode('utf-8')) as resp:
        return resp.getcode()

def get_quiz_data(filename, quiz_type, section):
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
    (url, assessmentIDs, IP) = get_quiz_data(filename, 'Assessment', section)

    for quizID in assessmentIDs:
        newdata={"quiz[notify_of_update]": 0, "quiz[ip_filter]":"{}".format(IP)}
        req = Request('{}/{}?access_token={}'.format(url,quizID,token), method='PUT')

        with urlopen(req, urlencode(newdata).encode('utf-8')) as resp:
            print(resp.getcode())


def get_room_ip(data,section):
    room_name = data['room'][section]
    IP = data[room_name]
    return IP

def write_new_json(quiz_type, filename):
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

    if section == 1:
        write_new_json(test_type, datafile)


    if test_type == 'quiz':
        print(set_quiz(datafile, section, token))
    elif test_type == 'assessment':
        set_assessment(datafile, section, token)
