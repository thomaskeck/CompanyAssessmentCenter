# Company Assessment Center

** This project is a toy-project to learn django and bootstrap **

An assessment center for companies.
The user can define **benchmarks** like
 - salary
 - working hours
 - vacation
 - business trips frequency
 - work climate
 - distance to work
 - housing situation
 - tools (programming languages, os)
 - personal interest in this field

Each **benchmark** can have an assoicate weight.

Job Offers from Companies can be rated on a scale from 0 to 4, and
compared to each other using these benchmarks.

# Usage
 * pip3 install django
 * python manage.py makemigrations assessmentcenter
 * python3 manage.py migrate
 * python3 manage.py createsuperuser
 * python3 manage.py runserver
 * Visit http://localhost:8000/assessmentcenter/
