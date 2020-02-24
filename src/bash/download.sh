#!/bin/bash

PYTHON=python
SRC_PATH=/Users/a17795890/PycharmProjects/ParseHHData/src/python
DATA_PATH=/Users/a17795890/hh-data

current_date=$(date +'%Y-%m-%d')

echo "Download vacancies that are relevant for ${current_date}"
mkdir $DATA_PATH/vacancies/raw/${current_date}
$PYTHON $SRC_PATH/download.py vacancies $DATA_PATH/vacancies/raw ${current_date} $DATA_PATH/specializations.json --update_specializations
echo "Download resumes that are relevant for ${current_date}"
mkdir $DATA_PATH/resumes/raw/${current_date}
$PYTHON $SRC_PATH/download.py resumes $DATA_PATH/resumes/raw ${current_date} $DATA_PATH/specializations.json
echo "Parse resumes that are relevant for ${current_date}"
mkdir $DATA_PATH/resumes/json/${current_date}
$PYTHON $SRC_PATH/parse.py $DATA_PATH/resumes/raw $DATA_PATH/resumes/json ${current_date} $DATA_PATH/specializations.json
