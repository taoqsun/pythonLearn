inputFile = open("inputFile.txt", "r")
print ("Name of the input file: ", inputFile.name);

outputFile = open("outputFile.txt", "a");
print ("Name of the output file: ", outputFile.name);

allLines = inputFile.readlines();
for eachLine in allLines:
    eachLine.replace("测试环境", "zjl");
    print ("current line content: %s" % (eachLine));
    
     
    #append into output file
    outputFile.write(eachLine);
outputFile.close();
inputFile.close();    
