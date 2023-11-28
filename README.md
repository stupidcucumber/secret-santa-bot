# Introduction
This bot is intended to serve as a SecretSanta randomizer to bring people around the world! It's idea is very simple: user can create a group and get special id of that group. After obtaining Id user automatically joins the initiated group and can share this id with others.

While creating group, admin specifies time for the timer. When time passed all members of the group who specified the valid information about their interests will get information about a person to whome they will give present!

Merry X-mas!

# Setting up
First you will need to install all required packages. We strongly advise to do it in a newly created environment using conda/virtualenv. To to this run the following command:
```
python3 -m pip install -r requirements.txt
```

# Implementation

## Database
For storing information about customers we use SQLite.  