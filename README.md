# Optimal Shift Scheduling Demo

This program takes a set of available shifts (pre-provided), and a set of user-submitted shift availability, and provides a mathemtically optimal matching between the two, such that each person is matched to the maximal number of shifts for which they are availabile. This solves the problem where inefficient scheduling results in some people not receiving what they wanted.

The program is intended to be run using the "availability.html" page front-end. Files are not modified by users directly.

## Important files:
- algorithm/index.html - Slideshow demo of the program.
- availability.html - Main survey page.
- **sched.py - Program logic.**
- shifts.csv - The mapping of available shifts at each location.
- avail.csv - Availability data collected from user submissions.
- submit.php - Simple parser to save survey data.
