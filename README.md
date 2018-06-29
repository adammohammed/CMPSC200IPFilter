# Canvas IP Filter Changer.

## Setup 
   1. Make sure python 3 is available on the machine which will run this application.
   2. Clone this repository with `git clone
      https://github.com/adammohammed/CMPSC200IPFilter.git` or download the zip
      file and extract it to a directory of your choosing.
   3. Create a API token by logging in to canvas and following [[https://community.canvaslms.com/docs/DOC-10806-4214724194][these instructions]].
   4. Create a file named /token/ in the application directory and paste your token.
   5. Configure the =quizzes.json= file, explanations are in the next section.
   6. Set up a job to run this program at the times necessary

## Quizzes json file

   This file handles most of the configuration. It does take a bit of time to
   get set up, but once you fill it in, no more manual work is required. An
   example =quizzes.json= is provided, but it **must** be changed each semester.

### Information needed to fill in JSON file
+ Course ID
+ List of rooms
+ IP filter associated with those rooms
+ Quiz IDs
+ Assessment ID pairs (one for automated and one for open-ended)
    
### JSON keys
+ courseID - This should be the number which shows in the URL following the
  /courses/ part `https://psu.instructure.com/courses/<courseID>`

+ lastAssessment - Set this to *-1* at the start of each semester, this is
  how the program identifies the correct module and IP filter to modify.

+ lastQuiz - Set this to *-1* at the start of each semester. Same as above,
  chooses the correct quiz for the day.

+ quizIDList - This is an array or all the quiz ID numbers which can be
  found in the URL `https://psu.instructure.com/courses/<courseId>/quizzes/<quizID>`

+ assessmentIDList - An array of 2 element arrays where the first element is
  the automated quiz id, and the second element is the open-ended quiz id.
  These are found just like the quiz ids.

+ room - An array of the rooms associated with each section, the elements at
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

