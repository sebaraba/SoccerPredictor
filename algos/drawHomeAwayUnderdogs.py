import csv

csv_file = csv.reader(open('../data/E1617.csv'))
next(csv_file)

upsets = 0
non_upsets = 0	

starting_bankroll = 100	
wagering_size = 5

bankroll = starting_bankroll

for game in csv_file:
	print(game)
	home_team = game[2]
	away_team = game[3]

	home_goals = int(game[4])
	away_goals = int(game[5])

	home_odds = float(game[23])
	draw_odds = float(game[24])
	away_odds = float(game[25])

	if home_odds > away_odds:
		if home_goals > away_goals:
			upsets += 1
			bankroll += wagering_size * (home_odds - 1)
		else:
			non_upsets += 1
			bankroll -= wagering_size

ROI = ((bankroll - starting_bankroll) / (wagering_size * (upsets + non_upsets))) * 100		

print ("There were '%s' upsets out of '%s' total matches" % (upsets, upsets + non_upsets))
print ("Starting bankroll = '%s'" % (starting_bankroll))
print ("Finishing bankroll = '%s' | ROI = '%s'" % (bankroll, ROI))