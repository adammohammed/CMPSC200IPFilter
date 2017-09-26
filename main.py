"""IPChanger - an ip changer for canvas IP filters
This program will automatically change the IP to the corresponding classes
after the time has passed.
"""
import sys
import json
from selenium.webdriver import *


def navigate_to_canvas(driver, user_name, passwd):
    ''' Logs the user in to Canvas and waits for success '''
    url = 'https://psu.instructure.com/login/saml/1080'
    driver.get(url)

    user = driver.find_element_by_id('login')
    pswd = driver.find_element_by_id('password')
    sub_div = driver.find_element_by_class_name('button')
    sub_button = sub_div.find_element_by_tag_name('input')

    user.send_keys(user_name)
    pswd.send_keys(passwd)
    sub_button.click()

    success_url = 'https://psu.instructure.com/?login_success=1'
    print('Waiting for page')

    while driver.current_url != success_url:
        pass

    print('Done waiting for page')
    return

def set_ip_to_item(driver, courseid, quizid, ip):
    ''' Navigates to the quiz for that course and sets ip filter'''
    url = 'https://psu.instructure.com/courses/{}/quizzes/{}/edit'
    url = url.format(courseid, quizid)
    driver.get(url)

    filter_ip = driver.find_element_by_id('enable_quiz_ip_filter')
    if filter_ip.is_selected:
        ip_box = driver.find_element_by_id('quiz_ip_filter')
        ip_box.clear()
        ip_box.send_keys(ip)

    save_button = driver.find_element_by_class_name('save_quiz_button')
    save_button.click()

    quiz_edit_url = driver.current_url
    print("Waiting for quiz to save")
    while driver.current_url == quiz_edit_url:
        pass
    print("Done waiting for quiz to save")
    return

def main():
    """This script can be used to set the appropriate ip filter for each class
       To use it, you just enter your username, password, quiz number, and
       section. The program will look up the corresponding times and ip's and
       set them for the quiz indicated.

       E.g. python main.py xyz1238 superpassword 7 1

       This will log in as user xyz1238 and set Quiz 7 to have the ip for
       section 1.
    """

    if len(sys.argv) != 5:
        print("Usage: python {} username password quiz_num section".format(sys.argv[0]))
        return -1

    user = sys.argv[1]
    passwd = sys.argv[2]
    quiz_num = int(sys.argv[3])
    section = int(sys.argv[4])

    with open('quizzes.json', 'r') as f:
        course_info = json.load(f)
    courseID = course_info["courseID"]
    quizID = course_info["quizIDList"][quiz_num] # gets quiz url id
    room_name = course_info["room"][section]     # gets room for that section
    ip = course_info[room_name]                  # gets ip for that room

    driver = Firefox()
    navigate_to_canvas(driver, user, passwd)
    set_ip_to_item(driver, courseID, quizID, ip)

    driver.quit()
if __name__ == '__main__':
    main()
