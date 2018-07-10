#!/usr/bin/env python3
## @package main
#
# This program is to be executed as part of a scheduled group of jobs to update
# the IPs for each section on the specific days. The program itself does not manage
# the times that the program is launched.
#
# Setup: Before running this program, make sure you've grabbed all relevant course
# and quiz/assessment ID's as detailed in the README.
#
# On Unix Systems, set up cron jobs for each section.
# On Windows systems, use the Task scheduler to schedule the execution.
#
# Usage: python main.py \<quiz/assessment\> \<section number\>
#
# ### Configure your preferred scheduler to launch the scripts as follows.
#
# At 7:55 on Wednesdays launch the script: python main.py quiz 1
#
# At 9:00 on Wednesdays launch the script: python main.py quiz 2
#
# At 10:05 on Wednesdays launch the script: python main.py quiz 3
#
# ...
#
# At 4:20 on Wednesdays launch the script: python main.py quiz 8
#
# ### Similarly for Assessments
#
# At 7:55 on Fridays launch the script: python main.py assessment 1
#
# At 9:00 on Fridays launch the script: python main.py assessment 2
#
# At 10:05 on Fridays launch the script: python main.py assessment 3
#
# ...
#
# At 4:20 on Fridays launch the script: python main.py assessment 8
#
# Once the scheduler and configuration JSON files are set up, you shouldn't need
# to touch this anymore. Make SURE(!) that the station that is launching the
# program will be ON and connected to the internet, otherwise you'll have to deal
# with make-ups.
#
# # The first time you try this I suggest double checking before each section to ensure that it has been setup properly.
#
import sys
from ipchanger import *

if __name__ == '__main__':
    with open('token', 'r') as f:
        ## @var token
        # This is the token string used to authenticate with the Canvas API
        token = f.readline()

    if len(sys.argv) != 3:
        print("You need to enter a section number!")
        print("USAGE: python {} type section#".format(sys.argv[0]))

    ## @var datafile
    # This is the name of the configuration json file.
    datafile = 'quizzes.json'

    ## @var test_type
    # This is either quiz or assessment to set the IP for that module
    test_type = sys.argv[1]

    ## @var section
    # This number determines the IP and room that are indexed for the update
    section = int(sys.argv[2])

    # Only update lastQuiz/Assessment when running script for section 1
    if section == 1:
        write_new_json(test_type, datafile)


    if test_type == 'quiz':
        print(set_quiz(datafile, section, token))
    elif test_type == 'assessment':
        set_assessment(datafile, section, token)
