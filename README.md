
# Introduction
This project is to take an input file that lists campaign contributions by individual donors and distill it into two output files:

medianvals_by_zip.txt: contains a calculated running median, total dollar amount and total number of contributions by recipient and zip code

medianvals_by_date.txt: has the calculated median, total dollar amount and total number of contributions by recipient and date.

# Programming Language
This project is implemented in Python3. 

# Dependancies 
* sys
* heapq

# Execution:
Execute with Python3

To execute this program, please run ./run.sh file.

command: python ./src/find_political_donors.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt
format: python execute_file  [arg1]input_file [arg2]outputt_file1 [arg3]output_file2 

# Data structure
This project used python dictionary to store the data.

First dictionary is dict_zip, key is string type: key = cmte_id + '|' + zip_code.
Second dictionary is dict_date, key is string type: key = cmte_id + '|' + transanction_date.
For both dictionaries, use object of DonationValue as value.

DonationValue has three entries: 2 heaps(one minHeap and one is maxHeap) and the sum.
Use these two heaps to store all the donation numbers.
When there are even numbers, len(minHeap) == len(maxHeap). When there are odd numbers,len(maxHeap) = len(minHeap) + 1.
All the numbers in maxHeap is less or equal to the numbers in minHeap.
When a new number comes, the insertion and rebalancing takes O(lgn) time complexity. While in calculating median, it takes O(1) time.

# Process flow
Step1. Read one line from input file

Step2. Analysize this record 

Step3. If the zip related data is valid, store the data into dict_zip and write this record into medianvals_by_zip.txt.

Step4. If the date related data is valid, store the data into dict_date and write this record into medianvals_by_date.txt.

Step5. Repeat from step2 to step5 until finish all the records in input file.

Step6. Write all the records in dict_date into output file:./output/medianvals_by_date.txt

# Details about input data
CMTE_ID : discard in case of empty

ZIP_CODE: for the zip code of the contributor, first remove the leading white space,  take the first characters and then check whether it is valid or not.

TRANSACTION_DT: check whether it is a valid date, and change the order to store it as YYYYMMDD format for sorting purpose. 

TRANSACTION_AMT: discard if it is empty. Besides these empty records, I noticed there are quite a few negative values. Instead of 

discarding this data, or use as it is, I choose to remove the '-' and treat it as a positive number. Because that makes most sense.

