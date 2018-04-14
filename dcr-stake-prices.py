import sys
import datetime
import csv
import pytz
import dateutil.parser

print "Running Decred Stake Price Calculator..."

# Validate input
if len(sys.argv) != 3:
	print "Missing correct number of arguments.\n"
	print "Usage:"
	print "python dcr-stake-prices.py [original_filename.csv] [new_filename.csv]\n"
	sys.exit()


# Settings
voting_filename = sys.argv[1]
new_voting_filename = sys.argv[2]
dcr_filename = "dcr.csv" # This data comes from coinmetrics.io


# Get the DCR values
prices = {}
with open(dcr_filename, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',')
	next(csvreader, None) # Ignore the header
	for row in csvreader:
		prices[row[0]] = row[4]


# Get the dates to pull
with open(new_voting_filename, 'w') as newcsvfile:
	with open(voting_filename, 'rb') as csvfile:
		csvwriter = csv.writer(newcsvfile, delimiter=',')
		csvreader = csv.reader(csvfile, delimiter=',')

		# Ignore the header, pull into new csv file
		header = next(csvreader, None)
		header.append("Total DCR Staked")
		header.append("Unix Epoch Time")
		csvwriter.writerow(header)

		for row in csvreader:
			if row[1] == "":
				csvwriter.writerow(row)
				continue

			# Get date
			date = dateutil.parser.parse(row[1])

			# Pull the year, month and day
			date_formatted = date.strftime("%Y-%m-%d")
			row[-1] = prices[date_formatted]
			row.append(float(prices[date_formatted]) * float(row[-2]))

			epoch = datetime.datetime(1970,1,1).replace(tzinfo=pytz.UTC)
			t = (date - epoch).total_seconds()
			row.append(t)

			# Add next row
			csvwriter.writerow(row)

