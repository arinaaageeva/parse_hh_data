#!/bin/bash

PYTHON=python
SRC_PATH=/Users/a17795890/PycharmProjects/ParseHHData/src/python
DATA_PATH=/Users/a17795890/hh-data

for dir in $DATA_PATH/resumes/raw/*
do 
  dir=`basename $dir`
  echo "Parse $dir directory"
  mkdir $DATA_PATH/resumes/json/$dir
  $PYTHON $SRC_PATH/parse.py $DATA_PATH/resumes/raw $DATA_PATH/resumes/json $dir $DATA_PATH/specializations.json
done
