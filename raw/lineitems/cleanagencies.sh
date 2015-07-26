#!/bin/bash

pwd 

for file in Agencies/Agencies/*
do
        echo $file
        name=`echo $file | cut -d . -f 1`
        ./postclean.pl $file >  $name-FY14Base.csv
done
