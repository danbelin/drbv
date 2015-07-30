#!/usr/bin/python

import sys, getopt
import csv
import numpy as np
import json

def read_budget(filename):
    #here we take the csv file and read it into an array to deal with
    with open(filename) as csvfile:
        headings = [item.strip() for item in next(csvfile).split(',')]
    budget = np.genfromtxt(filename, delimiter=',', skiprows=1, dtype=None)
    budget.dtype.names = headings
    return budget

def split_budget(budget, keys, splitter, headers):
#    if isinstance(budget[0], list):
#        print "RECURSING ON " + splitter + "\n"
#        for subbudget in budget:
#            subbudget = split_budget(subbudget, keys, splitter, headers)
#        return budget

    if not isinstance(budget[0], np.ndarray):
  #      print "NOT RECURSING " + splitter + "\n"
        subbudgets = []
        for key in keys:
            group = budget[budget[splitter] == key]
            if len(group) > 0:
                subbudgets.append(group)
        return subbudgets
    else:
 #       print "RECURSING ON " + splitter + "\n"
        subbudgets = []
        for subbudget in budget:
            subbudgets.append(split_budget(subbudget, keys, splitter, headers))
        return subbudgets

def get_total(budget):
    if isinstance(budget, np.ndarray):
        total = 0
        for item in budget:
            total += int(item["Total"])
        return total
    else:
        total = 0
        for subbudget in budget:
            total += int(get_total(subbudget))
        return total
 
fullbudget = read_budget("FY16-Request-AgencySorted.csv")
#print " ".join(map(str, fullbudget.dtype.names)) + "\n"
#split first on orgs
splitfield1 = 'Organization'
orgkeys = np.unique(fullbudget[splitfield1])
budgetbyorgs = split_budget(fullbudget, orgkeys, splitfield1, fullbudget.dtype.names)

#split now on spendingtype
splitfield2 = 'ActivityTitle'
activitykeys = np.unique(fullbudget[splitfield2])
orgsbudgetbyactivities = split_budget(budgetbyorgs, activitykeys, splitfield2, fullbudget.dtype.names)
#testprint

#make this recursive later, as there is no reason it isn't
print "{"

print "\"Name\":\"DoD\","
print "\"Total\":\"" + str(get_total(orgsbudgetbyactivities)) + "\","
print "\"Subdivision\":["
for g, subbudget in enumerate(orgsbudgetbyactivities):
    print "{"
    print "\"Name\":\"" + subbudget[0][0][splitfield1] + "\","
    print "\"Total\":\"" + str(get_total(subbudget)) + "\","
    print "\"Subdivision\":["
    for h, underbudget in enumerate(subbudget):
        print "{"
        print "\"Name\":\"" + underbudget[0][splitfield2] + "\","
        print "\"Total\":\"" + str(get_total(underbudget)) + "\","
        print "\"Subdivision\":["
        for i, item in enumerate(underbudget):
            print "{"
            print "\"Name\":\"" + item["ProgramElementTitle"] + "\","
            print "\"Total\":\"" + str(item["Total"]) + "\""
            if i < len(underbudget) - 1:
                print "},"
            else:
                print "}"
        print "]"
        if h < len(subbudget) - 1:
            print "},"
        else:
            print "}"
    print "]"
    if g < len(orgsbudgetbyactivities) - 1:
        print "},"
    else:
        print "}"
print "]"
print "}"

#for subbudget in orgsbudgetbyactivities:
#    print "\n"
#    if len(subbudget[0]) != 0:
#    print subbudget[0][0][splitfield1] + ":"
#    print "\n"
#    for underbudget in subbudget:
#        print "\t" + underbudget[0][splitfield2] + ":"
#        for item in underbudget:
#            print "\t\t" + ' '.join(map(str, item))   
#
#print json.JSONEncoder().encode(orgsbudgetbyactivities)
#    else:
#        print ' '.join(map(str, subbudget))
#    for underbudget in subbudget:
#        print "\n"
#        print "\t"
#        print underbudget[0][splitfield2]
#        for item in underbudget:
#            print "\t"
#            print ' '.join(map(str, item))
