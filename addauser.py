#!/usr/bin/env python
# Script to add users easily

import sys
import os
import subprocess
import pwd
import grp
import getpass
import time
import shutil
import re
from time import strftime

# Line length
lineLength = 80

# Users setup
minUID = 1000
minGID = 1000
passfile = "/etc/passwd"
shadowfile = "/etc/shadow"
groupfile = "/etc/group"

# Colors for status messages
red = "\033[91m"
green = "\033[92m"
bold = "\033[1m"
end = "\033[0m"

# Error reading


def killTask(msg):
    print >>sys.stderr, msg
    os._exit(1)


def checkUser(name):
    try:
        return pwd.getpwnam(name)
    except KeyError:
        return None


def checkGroup(group):
    try:
        return grp.getgrnam(group)
    except KeyError:
        return None


def getFirstName():
    fn = ""
    try:
        while len(fn) == 0:
            fn = raw_input('First Name: ')
    except KeyboardInterrupt:
        killTask("Interrupt detected, exiting.")
    return fn


def getLastName():
    ln = ""
    try:
        while len(ln) == 0:
            ln = raw_input('Last Name: ')
    except KeyboardInterrupt:
        killTask("Interrupt detected, exiting.")
    return ln


def getUserName(fn, ln):
    username = ""
    firstInital = fn[0:1].lower()
    ln = ln.replace(" ", "")
    lastNameTrunc = ln[0:7].lower()
    userJoined = firstInital + lastNameTrunc
    try:
        while len(username) == 0:
            username = raw_input(
                'Username [' + green + '%s' % userJoined + end + ']: ')
            if len(username) == 0:
                username = userJoined
            if checkUser(username):
                print red + "Username %s already exists." % username + end
                username = ""
    except KeyboardInterrupt:
        killTask("Interrupt detected, exiting.")
    return username


def getGroup(user):
    groupName = ""
    groupRec = user
    try:
        while len(groupName) == 0:
            groupName = raw_input(
                'Group [' + green + '%s' % groupRec + end + ']: ')
            if len(groupName) == 0:
                groupName = groupRec
            if checkGroup(groupName):
                print red + "Group %s already exists!" % groupName + end
                groupName = ""
    except KeyboardInterrupt:
        killTask("Interrupt detected, exiting.")
    return groupName


def getHomeDir(user):
    homeDir = ""
    homeDirRec = "/home/" + user
    try:
        while len(homeDir) == 0:
        homeDir = raw_input('Home Dir [' + green + '%s' % homeDirRec+end+']: ')
        if len(homeDir) == 0:
            homeDir = homeDirRec
        if os.path.exists(homeDir):
            print red + "Directory %s already exists!" % homeDir + end
            homeDir = ""
    except KeyboardInterrupt:
        killTask("Interrupt detected, exiting.")
    return homeDir


def getPasswd():
    passwd = ""
    passwdvrfy = ""
    try:
        while True:
            while len(passwd) == 0:
                passwd = getpass.getpass()
            while len(passwdvrfy) == 0:
                passwdvrfy = getpass.getpass(prompt='Verify Password: ')
            if not passwd == passwdvrfy:
                print red + "Password does not match!" + end
                passwd = ""
                passwdvrfy = ""
            else:
                break
    except KeyboardInterrupt:
        killTask("Interrupt detected, exiting.")
    return passwd


def getUID(user):
    myUID = minUID
    uidList = []
    fh = open(pasfile, 'r')
    lineLength = fh.readlines()
    fh. close()

    # read file, extract UIDs and sort them.
    for line in lineLength:
        uid = line.split(':')[2]
        uidList.append(int(uid))

    # Check for next available UID
    for uid in sorted(uidList):
        if uid >= minUID:
            if uid == myUID:
                myUID = myUID + 1
            else:
                break
    return myUID


def getGID(group):
    myGID = minGID
    gidList = []
    fh = open(grpfile, 'r')
    lineLength = fh.readlines()
    fh.close()

    for line in lineLength:
        gid = line.split(':')[2]
        gidList.append(int(gid))

    for gid in sorted(gidList):
        if gid >= minGID:
            if gid == myGID:
                myGID = myGID + 1
            else:
                break
    return myGID


def createGroup(group):
    gid = getGID(group)
    s = "group add -g %s %s 1> /dev/null 2>&1" % (gid, group)
    result = subprocess.call(s, shell=True)

    if not result == 0:
        print red + "Error in creating group %s" % group + end
    else:
        print green + "Created group %s" % group + end
    return result


def createUser(firstName, lastName, userName, group, homeDir):
    timeStamp = strftime("%Y.%m.%d %H:%M:%S")
    shutil.copy2(pasfile, pasfile + "." + timeStamp)
    shutil.copy2(shafile, shafile + "." + timeStamp)
    uid = getUID(userName)
    s = ' '.join(["useradd -c \"%s %s\" -m -d %s" % (firstName, lastName, homeDir),
                  "-u %s -g %s %s 1> /dev/null 2>&1" % (uid, group, userName)])
    result = subprocess.call(s, shell=True)
    if not result == 0:
        print red + "Error in creating user %s" % user + end
        os.remove(pasfile + "." + ts)
        os.remove(shafile + "." + ts)
    else:
        print green + "Created user %s" % user + end
    return result
