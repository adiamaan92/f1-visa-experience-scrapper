# F1 Interview Experience Scrapper

[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](#supported-python-versions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](https://github.com/artefactory-global/streamlit_prophet/blob/main/.pre-commit-config.yaml)
[![License](https://img.shields.io/badge/License-MIT-informational.svg)](https://github.com/artefactory-global/streamlit_prophet/blob/main/LICENSE)

## Context
F1-Visa is a type of non-immigrant visa provided by the US Government to allow students to temporarily live in the US for a defined period of time while studying at a school. It is the 3rd most applied visa in the whole world. For many students, it is the culmination of years of hard work and dedication.

![F1 interview experience](https://images.livemint.com/img/2021/08/23/1600x900/20210608071L_1629715737391_1629715753280.jpg)

After appearing for TOEFL/IELTS, GRE and applying for schools of interest, and getting an admit, attending the Visa Interview is the next step, which arguably is also the toughest. It is a subjective process, where a Visa officer asks a serious of question to the prospective student and arrives at a conclusion deeming his fitness.

An example for the denial could be,

1. Signs of family ties already present in the US (makes a student highly unlikely to return back to home country)
2. Lack of funds for education
3. No ties between experience and the major chosen
4. Questionable universities and academic performances

> The data comes from a telegram channel and all the visa experiences mainly are from India. I am working on adding more sources. So watch out!

## Dataset:
Dataset is hosted here, https://www.kaggle.com/adiamaan/f1-visa-experiences

> The scrapper is scheduled to run every day at 8 AM using a Github Action workflow.

## Acknowledgements
A huge thanks to the mods of the Telegram channel, t.me/f1interviewreviews for moderating the community and pushing out new experiences frequently.

## Data description:
The dataset contains the following columns,

| Syntax  | Description                                                                                                                         |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| msg_id  | Message Unique ID                                                                                                                   |
| date    | Date the message was posted. Not necessarily the interview date                                                                     |
| message | Message detailing the visa interview experience of a student, usually in a chat format between the Visa interviewer and the student |


