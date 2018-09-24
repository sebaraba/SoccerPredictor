import csv, ast, sys
from itertools import islice

class buildStatistics(object):


    def __init__(self, data_set, weeks_wait):
        self.csv_file = csv.reader(open(data_set))
        next(self.csv_file)
        self.match_data = list(islice(self.csv_file, None, weeks_wait * 10))
        self.dict = {}
        self.weeks_wait = weeks_wait

    def methodCalls(self):
        self.buildTeamList()
        dict = self.buildTeamDictionary()
        return dict

    # BUILD UP A LEAST OF ALL TEAMS
    def buildTeamList(self):
        team_list = []
        for row in self.match_data:
            if row[2] not in team_list:
                team_list.append(row[2])
            if row[3] not in team_list:
                team_list.append(row[3])
        team_list.sort()
        # WRITE UP A FILE WITH THE DATA MODEL
        teams_file = open('../output/team_list.txt', 'w')
        teams_file.write("""{
        """)
        for team in team_list:
            teams_file.write("""	'%s': 
            {'home_goals': 0, 'away_goals': 0, 
            'home_conceded': 0, 'away_conceded': 0, 
            'home_games': 0, 'away_games': 0, 
            'alpha_h': 0, 'beta_h': 0, 
            'alpha_a': 0, 'beta_a': 0},
            """ % (team))
        teams_file.write("}")
        teams_file.close()

    # FIND ATTACK/DEFENSE STRENGTH PER SEASON
    def findAvgAttDefStrength(self):
        avg_away_attack_strength = 0
        avg_home_attack_strength = 0
        avg_away_defense_strength = 0
        avg_home_defense_strength = 0
        league_home_goals = 0.0
        league_away_goals = 0.0
        league_total_matches = 0.0
        for row in self.match_data:
            league_home_goals += float(row[4])
            league_away_goals += float(row[5])
            league_total_matches += 1.0
        avg_home_attack_strength = float(league_away_goals/league_total_matches)
        avg_away_attack_strength = float(league_home_goals/league_total_matches)
        avg_away_defense_strength = float(avg_home_attack_strength)
        avg_home_defense_strength = float(avg_away_attack_strength)

        return (avg_away_attack_strength, avg_home_attack_strength, avg_away_defense_strength, avg_home_defense_strength)



    # FILL THE DATA MODEL WITH ONE SEASONS DATA
    def buildTeamDictionary(self):
        s = open('../output/team_list.txt', 'r').read()
        self.dict = ast.literal_eval(s)
        alpha_a, alpha_h, beta_a, beta_h = self.findAvgAttDefStrength()
        for team in self.dict:
            for match in self.match_data:
                if team in match[2]:
                    self.dict[team]['home_goals'] += float(match[4])
                    self.dict[team]['home_conceded'] += float(match[5])
                    self.dict[team]['home_games'] += 1
                elif team in match[3]:
                    self.dict[team]['away_goals'] += float(match[5])
                    self.dict[team]['away_conceded'] += float(match[4])
                    self.dict[team]['away_games'] += 1
            self.dict[team]['alpha_h'] = float((self.dict[team]['home_goals'] / self.dict[team]['home_games']) / alpha_h)
            self.dict[team]['alpha_a'] = float((self.dict[team]['away_goals'] / self.dict[team]['away_games']) / alpha_a)
            self.dict[team]['beta_a'] = float((self.dict[team]['away_conceded'] / self.dict[team]['away_games']) / beta_a)
            self.dict[team]['beta_h'] = float((self.dict[team]['home_conceded'] / self.dict[team]['home_games']) / beta_h)

        return self.dict
