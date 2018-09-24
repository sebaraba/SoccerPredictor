import csv, math, ast, numpy as np
from buildStatistics import buildStatistics as bS

class poissonDistribution():

	def __init__(self, data_set, weeks_wait):
		self.csvRead = csv.reader(open(data_set))
		self.weeks_wait = weeks_wait
		self.games_played = 0
		self.total_value = 0
		next(self.csvRead)
		temp = bS(data_set, weeks_wait)
		self.dict = temp.methodCalls()

	def poisson(self, actual, mean):
		return math.pow(mean, actual) * math.exp(-mean) / math.factorial(actual)

	def mainMethod(self):
		for game in self.csvRead:
			home_team = game[2]
			away_team = game[3]

			home_goals = int(game[4])
			away_goals = int(game[5])

			home_win_prob = 0
			draw_win_prob = 0
			away_win_prob = 0
			
			curr_home_goals = 0
			curr_away_goals = 0
			avg_home_goals = 1
			avg_away_goals = 1
			
			team_bet = ''
			ev_bet = ''
			
			# GETTING UPDATED VARIABLES
			if self.games_played > (self.weeks_wait * 10):
				for key in self.dict:
					curr_home_goals += self.dict[key]['home_goals']
					curr_away_goals += self.dict[key]['away_goals']
					avg_home_goals = curr_home_goals / (self.games_played)
					avg_away_goals = curr_away_goals / (self.games_played)
				home_team_a = (self.dict[home_team]['alpha_h'] + self.dict[home_team]['alpha_a']) / 2
				away_team_a = (self.dict[away_team]['alpha_h'] + self.dict[away_team]['alpha_a']) / 2
				
				home_team_d = (self.dict[home_team]['beta_h'] + self.dict[home_team]['beta_a']) / 2
				away_team_d = (self.dict[away_team]['beta_h'] + self.dict[away_team]['beta_a']) / 2
				
				# home_team_a = self.dict[home_team]['alpha_a']
				# away_team_a = self.dict[away_team]['alpha_h']
				
				# home_team_d = self.dict[home_team]['beta_h']
				# away_team_d = self.dict[away_team]['beta_a']

				home_team_exp = avg_home_goals * home_team_a * away_team_d
				away_team_exp = avg_away_goals * away_team_a * home_team_d

			# RUNNING POISSON	
				l = open('../output/poisson.txt', 'w')
				
				for i in range(5):
					for j in range(5):
						prob = self.poisson(i, home_team_exp) * self.poisson(j, away_team_exp)
						l.write("Prob%s%s = %s\n" % (i, j, prob))
				
				l.close()
				
				with open('../output/poisson.txt') as f:
					for line in f:
						
						home_goals_m = int(line.split(' = ')[0][4])
						away_goals_m = int(line.split(' = ')[0][5])
						
						prob = float(line.split(' = ')[1])
						
						if home_goals_m > away_goals_m:
							home_win_prob += prob
						elif home_goals_m == away_goals_m:
							draw_win_prob += prob
						elif home_goals_m < away_goals_m:
							away_win_prob += prob

			#CALCULATE VALUE
				bet365odds_h, bet365odds_d, bet365odds_a = float(game[23]), float(game[24]), float(game[25])
				
				ev_h = (home_win_prob * (bet365odds_h - 1)) - (1 - home_win_prob)
				ev_d = (draw_win_prob * (bet365odds_d - 1)) - (1 - draw_win_prob)
				ev_a = (away_win_prob * (bet365odds_a - 1)) - (1 - away_win_prob)
				
				highestEV = max(ev_h, ev_d, ev_a)
				if (highestEV >= 0):
					if (ev_h == highestEV) and (ev_h > 0):
						team_bet = home_team
						ev_bet = ev_h
						if home_goals > away_goals:
							self.total_value += 2 * (bet365odds_h - 1)
						else:
							self.total_value -= 2
							
					elif (ev_d == highestEV) and (ev_d > 0):
						team_bet = 'Draw'
						ev_bet = ev_d
						if home_goals == away_goals:
							self.total_value += 2 * (bet365odds_d - 1)
						else:
							self.total_value -= 2
					elif (ev_a == highestEV) and (ev_a > 0):
						team_bet = away_team
						ev_bet = ev_a
						if home_goals < away_goals:
							self.total_value += 2* (bet365odds_a - 1)
						else:
							self.total_value -= 2
				
				if (team_bet != '') and (ev_bet != ''):
					print ("Bet on '%s' (EV = %s)" % (team_bet, ev_bet))	
					print (self.total_value)
					# raw_input()
				
			# UPDATE VARIABLES AFTER MATCH HAS BEEN PLAYED
				self.dict[home_team]['home_goals'] += home_goals
				self.dict[home_team]['home_conceded'] += away_goals
				self.dict[home_team]['home_games'] += 1
				
				self.dict[away_team]['away_goals'] += away_goals
				self.dict[away_team]['away_conceded'] += home_goals
				self.dict[away_team]['away_games'] += 1
			
			self.games_played += 1
			