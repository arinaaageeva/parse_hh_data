#!/bin/bash

PYTHON=python
SRC_PATH=/Users/a17795890/PycharmProjects/ParseHHData/src/python
DATA_PATH=/Users/a17795890/hh-data

current_date=$(date +'%Y-%m-%d')

echo "Download specializations"
$PYTHON $SRC_PATH/download/download_specializations.py $DATA_PATH/specializations
echo "Download resumes that are relevant for ${current_date}"
mkdir $DATA_PATH/resumes/raw/${current_date}
$PYTHON $SRC_PATH/download/download_resumes.py $DATA_PATH/resumes/raw ${current_date} $DATA_PATH/specializations
echo "Download vacancies that are relevant for ${current_date}"
mkdir $DATA_PATH/vacancies/raw/${current_date}
$PYTHON $SRC_PATH/download/download_vacancies.py $DATA_PATH/vacancies/raw ${current_date} $DATA_PATH/specializations