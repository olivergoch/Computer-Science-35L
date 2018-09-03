#!/usr/bin/python
#Oliver Goch
import sys, string, locale
from optparse import OptionParser

class comm:
    def __init__(self, filename1, filename2):
        #open and read the files, self.lines1/2 are arrays of lines in the file
        if(filename1 == "-"):
            f1 = sys.stdin
            f2 = open(filename2, 'r')
        elif(filename2 == "-"):
            f1 = open(filename1, 'r')
            f2 = sys.stdin
        else:
            f1 = open(filename1, 'r')
            f2 = open(filename2, 'r')
        self.lines1 = f1.readlines()
        self.lines2 = f2.readlines()
        f1.close()
        f2.close()
        #declare an array to hold the outputs
        #I was originally only going to do one, but I have to surpress the outputs so oh wellllll
        self.columns1 = []
        self.columns2 = []
        self.columns3 = []

    def getmin(self, num1, num2):
        if(num1 < num2):
            return num1
        else:
            return num2

    def sortedCompareLines(self):
        len1 = len(self.lines1)
        len2 = len(self.lines2)
        #if the first file is empty, just fill up the second column
        if(len1 == 0):
            for k in range(len(self.lines2)):
                self.columns1.append('\t')
                self.columns2.append(self.lines2[k])
                self.columns3.append("")
            return
        
        #if the second file is empty, just fill up the second column
        if(len2 == 0):
            for k in range(len(self.lines1)):
                self.columns1.append(self.lines1[k])
                self.columns2.append("")
                self.columns3.append("")
            return
        #find the min of the two lengths and use that as boundary in for
        min = self.getmin(len1, len2)
        for i in range(min):
            if(self.lines1[i] == self.lines2[i]):
                self.columns1.append('\t')
                self.columns2.append('\t')
                self.columns3.append(self.lines1[i])
            #if one is less than the other (comes first alphabetically), have that one come first
            elif(self.lines1[i] > self.lines2[i]):
                self.columns1.append('\t')
                self.columns2.append(self.lines2[i])
                self.columns3.append("")
                self.columns1.append(self.lines1[i])
                self.columns2.append("")
                self.columns3.append("")
            elif(self.lines1[i] < self.lines2[i]):
                self.columns1.append(self.lines1[i])
                self.columns2.append("")
                self.columns3.append("")
                self.columns1.append('\t')
                self.columns2.append(self.lines2[i])
                self.columns3.append("")
                    
            #if length of file1 is less than file2
        if(min == len1 and min != len2):
            #append the rest of file2 to columns1
            j = min
            while j < len(self.lines2):
                self.columns1.append('\t')
                self.columns2.append(self.lines2[j])
                self.columns3.append("")
                j+=1
            #if lenght of file2 is less than file1
        if(min == len2 and min != len1):
            #append the rest of file1 to columns2
            j=min
            while j < len(self.lines1):
                self.columns1.append(self.lines1[j])
                self.columns2.append("")
                self.columns3.append("")
                j+=1

    def unsortedCompareLines(self):
        for i in range(len(self.lines1)):
            for j in range(len(self.lines2)):
                #sys.stdout.write("i=" + str(i) + "j=" + str(j))
                if(self.lines1[i] == self.lines2[j]):
                    self.columns1.append('\t')
                    self.columns2.append('\t')
                    self.columns3.append(self.lines1[i])
                    self.lines2[j] = ""
                    break
                elif(j==len(self.lines2)-1):
                    self.columns1.append(self.lines1[i])
                    self.columns2.append("")
                    self.columns3.append("")

        for k in range(len(self.lines2)):
            if(self.lines2[k] != ""):
                self.columns1.append('\t')
                self.columns2.append(self.lines2[k])
                self.columns3.append("")

    def printTheStuff(self, op1, op2, op3):
        #suppress column 1
        if(op1):
            self.columns1 = ['' for x in self.columns1]
        
        #suppress column 2
        if(op2):
            self.columns1 = ['' if x=='\t' else x for x in self.columns1]
            self.columns2 = ['' for x in self.columns2]
            #I do this so it has the nice formatting still, making sure it still has tabs for column three
            for i in range(len(self.columns3)):
                if(self.columns3[i] != '' and not op1):
                    self.columns1[i] = '\t'
        #suppress column 3
        if(op3):
            #once again, make sure it has the nice formatting, keeping the tabs when needed for column two, but getting rid of them for column three, which will not appear
            for i in range(len(self.columns3)):
                if(self.columns3[i] != ''):
                    self.columns1[i] = ''
            self.columns2 = ['' if x=='\t' else x for x in self.columns2]
            self.columns3 = ['' for x in self.columns3]
        
        
        for i in range(len(self.columns1)):
            #concatenate it and print it out
            sys.stdout.write(self.columns1[i] + self.columns2[i] + self.columns3[i])



def main():
    version_msg = "%prog 1.0"
    usage_msg = """%prog [-123u] FILE1 FILE2
compare lines of a file and optionally supress columns1"""

    parser = OptionParser(version=version_msg, usage=usage_msg)
    parser.add_option("-1", action="store_true", dest="no1", default=False, help="supress column one")
    parser.add_option("-2", action="store_true", dest="no2", default=False, help="supress column two")
    parser.add_option("-3", action="store_true", dest="no3", default=False, help="supress column three")
    parser.add_option("-u", action="store_true", dest="nosort", default=False, help="deal with unsorted files")
    options, args = parser.parse_args(sys.argv[1:])
    
    noshow1 = bool(options.no1)
    noshow2 = bool(options.no2)
    noshow3 = bool(options.no3)
    unsorted = bool(options.nosort)
    
    if len(args) != 2:
        parser.error("wrong number of operands")
    
    input_file1 = args[0]
    input_file2 = args[1]
    try:
        comparing = comm(input_file1, input_file2)
        if(unsorted):
            comparing.unsortedCompareLines()
        else:
            comparing.sortedCompareLines()
        comparing.printTheStuff(noshow1, noshow2, noshow3)
    except IOError as (errno, strerror):
        parser.error("I/O error({0}): {1}".
                     format(errno, strerror))

if __name__ == "__main__":
    main()
