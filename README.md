# Canvas IP Filter Changer
This IP filter changer maintains a configuration file populated with the quiz and assessment ids, room names for each section, and ips for each room. When executing this program the user specifies a quiz type (i.e. quiz or assessment) and a section number (e.g 1 - 8). The program will do the relevant look-ups and set the IP for that room and section on the quiz for that day.

*Important* This program does *NOT* manage the times of its own execution. For this I've normally used cron, usually available on UNIX systems or Task Scheduler available on Windows. Using whichever scheduler, I set up task to execute this program a few minutes before each section on both Wednesdays and Fridays.

For example on Wednesday at 8:00 a.m  the scheduler will run `python3 main.py quiz 1` and each 50 minutes will run changing the last argument to the corresponding section. On Fridays its the same, but instead of `quiz` the argument would be `assessment`.

## Setup 
   1. Make sure python 3 is available on the machine which will run this application.
   2. Clone this repository with `git clone
      https://github.com/adammohammed/CMPSC200IPFilter.git` or download the zip
      file and extract it to a directory of your choosing.
   3. Create a API token by logging in to canvas and following [these instructions](https://community.canvaslms.com/docs/DOC-10806-4214724194).
   4. Create a file named `token` in the application directory and paste your token.
   5. Configure the `quizzes.json` file, explanations are in the next section.
   6. Set up a job to run this program at the times necessary

## Quizzes json file

   This file handles most of the configuration. It does take a bit of time to
   get set up, but once you fill it in, no more manual work is required. An
   example `quizzes.json` is provided, but it **must** be changed each semester.

### Information needed to fill in JSON file
+ Course ID
+ List of rooms
+ IP filter associated with those rooms
+ Quiz IDs
+ Assessment ID pairs (one for automated and one for open-ended)
    
### JSON keys
+ **courseID** - This should be the number which shows in the URL following the
  /courses/ part `https://psu.instructure.com/courses/<courseID>`

+ **lastAssessment** - Set this to *0* at the start of each semester, this is
  how the program identifies the correct module and IP filter to modify.

+ **lastQuiz** - Set this to *0* at the start of each semester. Same as above,
  chooses the correct quiz for the day.

+ **quizIDList** - This is an array or all the quiz ID numbers which can be
  found in the URL `https://psu.instructure.com/courses/<courseId>/quizzes/<quizID>`

+ **assessmentIDList** - An array of 2 element arrays where the first element is
  the automated quiz id, and the second element is the open-ended quiz id.
  These are found just like the quiz ids.

+ **room** - An array of the rooms associated with each section, the elements at
  position 1 will be the key read when finding the IP filter. I.e. `room[0] = "Keller210"` , so the program will look at the entry `"Keller210": "128.118.160.0/25"` when adjusting the IP filter. Entries in the room
  array, must also have an entry in the JSON file, with the *same* name as
  the key and the value should be the IP filter associated with that room as
  shown below.

```javascript
[
"Keller115": "192.168.1.0/25",
"Keller210": "128.118.160.0/25",
"Keller211": "192.168.1.0/25",
"Westgate": "192.168.1.0/25",
"Willard": "192.168.1.0/25",
"room": [
    "Keller210",
    "Keller210",
    "Keller115",
    "Keller115",   
    "Willard",
    "Keller115",
    "Keller211",
    "Keller211"
]
```

## Additional Documentation

The code is documented with Doxygen comments, to build additional documentation just perform, `doxygen doxygen.cfg`. This will create a docs folder with additional function/variable/parameter level comments which may be useful if extending or modifying the code. 
