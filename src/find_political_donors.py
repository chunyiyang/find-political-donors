
import sys
from heapq import *

class DonationValue: 

    def __init__(self):
        ''' this class is used as value in dict_zip and dict_date
        store the amount data into two heaps: small and large
        store the total amount data in variable amount
        median is calculated based upon the heaps
        '''

        self.heaps = [],[]
        self.amount = 0

    def findMedian(self):
        ''' if there are odd numbers, we pick top of large heap as median value
        otherwise there are even numbers in total, we pick (large[0] - small[0])/2.0 as median value
        '''
        def roundMedian(x):
            return int(x + 0.5) if x > 0 else int(x - 0.5)

        small, large = self.heaps
        if len(large) > len(small):
            return roundMedian(large[0])
        return roundMedian((large[0] - small[0])/2.0)
    
    def findAmount(self):
        ''' return total donation amount 
        '''      
        return int(round(self.amount))
    
    def findCount(self):
        ''' return total donation count 
        '''          
        small, large = self.heaps
        return len(large) + len(small)

    def addNum(self, num):
        ''' insert new data into heaps
        large is a max_heap, small is a min_heap and len(large) == len(small) or len(large) == len(small) + 1
        when insert, we push num * -1 into small, so the smallest num is on top
        when a new number comes, we insert it into large heap first,
        then insert the top of large heap into small heap
        if that makes len(large) less than len(small), we move the top of small heap to large heap
        '''          
        small, large = self.heaps
        heappush(small, -heappushpop(large, num))
        if len(large) < len(small):
            heappush(large, -heappop(small))
        self.amount += num
            

def checkInputdata(line): 
    ''' param line: string 
        strip and analyze data record
    '''      

    data = line.strip().split('|')

    # is_zip_OK: boolean, whether we need to write this record into zip file
    # is_date_OK: boolean, whether we need to write this record into date file

    is_zip_OK = False
    is_date_OK = False
    key_zip = None
    key_date = None
    transanction_amount = None

    #if OTHER_ID is not empty, return 
    if len(data[15]) != 0:
        return is_zip_OK, is_date_OK, key_zip, key_date, transanction_amount

    cmte_id = data[0]
    zip_code = getZipcode(data[10])
    transanction_date = getDate(data[13])
    transanction_amount = getAmount(data[14])

    if (len(cmte_id) != 0 ) and (transanction_amount is not None):
        if zip_code is not None:
            is_zip_OK = True
        if transanction_date is not None:
            is_date_OK = True

    # use string cmte_id + '|' + zip_code as key in dict_zip
    if is_zip_OK:
        key_zip = cmte_id + '|' + zip_code

    # use string cmte_id + '|' + transanction_date as key in dict_zip    
    if is_date_OK:
        key_date = cmte_id + '|' + transanction_date
 
    return is_zip_OK, is_date_OK, key_zip, key_date, transanction_amount

def getZipcode(zip_code):
    ''' param zip_code: string
    return None if zip_code is empty or malformatted
    otherwise return zip_code[:5]
    '''      
    return_value  = None
    zip_code = zip_code.lstrip()
    if len(zip_code) >= 5 and zip_code[:5].isdigit():
        return_value = zip_code[:5]
    return return_value

def getAmount(transaction_amount):
    ''' param transaction_amount: string
    return None if transaction_amount is empty or malformatted
    otherwise return float(transaction_amount)
    '''      
    try:
        float(transaction_amount)
        return_value = float(transaction_amount)
    except:
        return_value = None
    return return_value 

def getDate(transaction_date):
    ''' param transaction_date: string
    return None if transaction_date is empty or malformatted
    otherwise return transaction_date as YYYYMMDD for sorting purpose
    '''      
    if len(transaction_date) != 8 or not transaction_date.isdigit():
        return None
    month = int(transaction_date[0:2])
    day = int(transaction_date[2:4])
    year = int(transaction_date[4:8])
    if month == 0 or month > 12: 
        return None
    if day == 0 or day > 31 or year < 1800:
        return None
    if month in [4, 6, 9, 11] and day == 31:
        return None
    if (month == 2 and day >= 30) or ((year % 4 != 0) and month == 2 and day >= 29):
        return None
    return_value = transaction_date[4:8] + transaction_date[0:4]
    return return_value 

def writeZipInfo(key_zip, transaction_amount, output_file, dict_zip):
    ''' param key_zip: string
    transaction_amount: float
    output_file: file handler
    dict_zip: dictionary

    if key_zip exsits in dict_zip, add this new amount into record
    otherwise create a new object of class DonationValue() 
    add add this new pair (key, value)  into dict_zip
    '''     
    if key_zip in dict_zip:
        dict_zip[key_zip].addNum(transaction_amount)
    else:     
        newdata = DonationValue()
        newdata.addNum(transaction_amount)
        dict_zip[key_zip] = newdata

    # get running median, totalcount, totalamount value of key_zip from dict_zip 
    # write this record into output_file (medianvals_by_zip.txt)
         
    median = dict_zip.get(key_zip).findMedian()
    totalamount = dict_zip.get(key_zip).findAmount()
    totalcount = dict_zip.get(key_zip).findCount()
    
    zip_output = key_zip + '|'+ str(median) + '|' + str(totalcount) + '|' + str(totalamount) + '\n'
    output_file.write(zip_output)


def storeDateInfo(key_date, transaction_amount, dict_date):
    ''' param key_date: string
    transaction_amount: float
    dict_date: dictionary

    if key_date exsits in dict_date, add this new amount into record
    otherwise create a new object of class DonationValue() as the value of new record
    add add this pair (key, value)  into dict_date
    '''  
    if key_date in dict_date:
        dict_date[key_date].addNum(transaction_amount)
    else:     
        newdata = DonationValue()
        newdata.addNum(transaction_amount)
        dict_date[key_date] = newdata

def writeDateInfo(output_date_file_path, dict_date):
    ''' param output_date_file_path: string (path of medianvals_by_date.txt)
    dict_date: dictionary
    
    sort keys in dict_date first, then write all records information into output_date_file_path
    '''  

    output_date_file = open(output_date_file_path, 'w')
    for key in sorted(dict_date.keys()):
        value = dict_date[key]
        median = value.findMedian()
        count = value.findCount()
        totalamount = value.findAmount()
        key = key[:-8] + key[-4:] + key[-8:-4]
        date_output = key + '|'+ str(median) + '|' + str(count) + '|' + str(totalamount) + '\n'
        output_date_file.write(date_output)
    output_date_file.close()

def dataProcess(input_file_path, output_zip_file_path, output_date_file_path):
    ''' param input_file_path: string (path of input file)
    output_zip_file_path: string (path of medianvals_by_zip.txt)
    output_date_file_path: string (path of medianvals_by_date.txt)
    ''' 
    dict_zip = {}
    dict_date = {}
    input_file = open(input_file_path, 'r')
    output_zip_file = open(output_zip_file_path, 'w')
    for line in input_file:

        # check each record whether they are valid or not
        is_zip_OK, is_date_OK, key_zip, key_date, transaction_amount =  checkInputdata(line)
        if is_zip_OK:
            # if the record is qualified for zip file, write it into zip file 
            writeZipInfo(key_zip, transaction_amount, output_zip_file, dict_zip)
        if is_date_OK:
            # if the record is qualified for date file, store it into dict_date
            storeDateInfo(key_date, transaction_amount, dict_date )

    input_file.close()
    output_zip_file.close() 
    del dict_zip
    # write dict_date into file
    writeDateInfo(output_date_file_path, dict_date)


if __name__ == "__main__":

    argv = sys.argv
    input_file_path = argv[1]
    output_zip_file_path = argv[2]
    output_date_file_path = argv[3]

    dataProcess(input_file_path, output_zip_file_path, output_date_file_path)
    
    

 



