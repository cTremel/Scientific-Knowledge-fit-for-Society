#!/usr/bin/env python
# author: r4isstatic Initial commit
#import the CSV module for dealing with CSV files
import csv

#create a 'reader' variable, which allows us to play with the contents of the CSV file
#in order to do that, we create the ifile variable, open the CSV file into that, then pass its' contents into the reader variable.
""" ifile = open('very short example.csv', 'rb')
reader = csv.reader(ifile) """

#create a new variable called 'outfile' (could be any name), which we'll use to create a new file that we'll pass our TTL into.
outfile = open('climate.ttl', 'a')

with open('very short example.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	rownum = 0
	for row in spamreader:
		if rownum == 0: # if it's the first row, then ignore it, move on to the next one.
			categories = row
			pass
		else: # if it's not the first row, place the contents of the row into the 'c' variable, then create a 'd' variable with the stuff we want in the file.
			print(categories)
			c = row
			
			#maybe find out what class corresponds to triple
			subject_class = c[0] 

			while subject_class == c[0]:
				#d = '<' + c[0] + c[1] + '> a pol:Council ;\n core:preferredLabel "' + c[2] + '" ;\n core:sameAs <' + c[3] + '> .\n \n'
				if categories[0] == "subject" & categories[1] == "object" & categories[2] == "predicate":
					d = '<' + c[0] 
				else:
					print("csv categories 0,1,2 need to be subject,object,predicate")
					exit()
				outfile.write(d)	# now write the d variable into the file
		rownum += 1 # advance the row number so we can loop through again with the next row
	
# finish off by closing the two files we created

outfile.close()



#get python to loop through each row in the CSV, and ignore the first row.



	