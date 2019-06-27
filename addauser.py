#!/usr/bin/env python
# Script to add users easily

import sys, os, subprocess, pwd, grp, getpass, time, shutil, re
from time import strftime

# Line length
ll = 80

# Users setup
min_uid = 1000
min_gid = 1000
passfile = "/etc/passwd"
shadowfile = "/etc/shadow"
groupfile = "/etc/group"

# Colors for status messages 
red="\033[91m"
green="\033[92m"
bold="\033[1m"
end="\033[0m"

# Error reading
def killTask(msg):
    print >>sys.stderr, msg
    os._exit(1)

def checkUser(name):
    try: return pwd.getpwnam(name)
    except KeyError: return None

def checkGroup(group):
    try: return grp.getgrnam(group)
    except KeyError: return None

def getFirstName():
    fn = ""
    try:
        while len(fn) == 0: fn = raw_input('First Name: ')
    except KeyboardInterrupt: killTask("Interrupt detected, exiting.")
    return fn

def getLastName():
    ln = ""
    try: 
        while len(ln) == 0: ln = raw_input('Last Name: ')
    except KeyboardInterrupt: killTask("Interrupt detected, exiting.")
    return ln

def getUserName(fn, ln):
    username = ""
    firstInital = fn[0:1].lower()
    ln = ln.replace(" ", "")
    lastNameTrunc = ln[0:7].lower()
    userJoined = firstInital + lastNameTrunc
    try: 
        while len(username) == 0:
            username = raw_input('Username [' + green + '%s' % userJoined + end + ']: ')
            if len(username) == 0: username = userJoined
            if checkUser(username):
                print red + "Username %s already exists." % username + end
                username = ""
    except KeyboardInterrupt: killTask("Interrupt detected, exiting.")
    return username

def getGroup(user):
    groupName = ""
    groupRec = user
    try: 
        while len(groupName) == 0:
            groupName = raw_input('Group [' + green + '%s' % groupRec + end + ']: ')
            if len(groupName) == 0: groupName = groupRec
            if checkGroup(groupName):
                print red + "Group %s already exists!" % groupName + end
                groupName = ""
    except KeyboardInterrupt: killTask("Interrupt detected, exiting.")
    return groupName

def getHomeDir(user):
    homeDir = ""
    homeDirRec = "/home/" + user
    try: 
        while len(homeDir) == 0:
        homeDir = raw_input('Home Dir [' + green+ '%s' % homeDirRec+end+']: ')
        if len(homeDir) == 0: homeDir = homeDirRec
        if os.path.exists(homeDir):
            print red + "Directory %s already exists!" % homeDir + end
            homeDir = ""
    except KeyboardInterrupt: killTask("Interrupt detected, exiting.")
    return homeDir

def getPasswd():
    passwd = ""
    passwdvrfy = ""
    try:
        while True:
            while len(passwd) == 0: passwd = getpass.getpass()
            while len(passwdvrfy) == 0: 
                passwdvrfy = getpass.getpass(prompt='Verify Password: ')
            if not passwd == passwdvrfy:
                print red + "Password does not match!" + end
                passwd = ""
                passwdvrfy = ""
            else: break
    except KeyboardInterrupt: killTask("Interrupt detected, exiting."
    return passwd



    