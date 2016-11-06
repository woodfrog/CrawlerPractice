from bs4 import BeautifulSoup
import requests
import json


def get_espn_league_rank(url):
    data = requests.get(url)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'lxml')
    table = soup.find(id='tables-overall')
    teams = table.find_all('td', class_='team')  # get the team list
    rank = list()
    for team in teams:
        try:
            team_name = team.find('a').text.strip()
        except AttributeError:   # some team may not have official website, so the name would be in a different position
            team_name = team.text.strip()
        rank.append(team_name)
    return rank


if __name__ == '__main__':
    urls = {'Premiere League': 'http://www.espnfc.us/english-premier-league/23/table',
            'Bundesliga': 'http://www.espnfc.us/german-bundesliga/10/table'}
    results = dict()

    for league_name, url in urls.items():
        table_list = get_espn_league_rank(url)
        results[league_name] = table_list
        print('****----------------****')
        print(league_name)
        for index, team in enumerate(table_list):
            print('No{}. {}'.format(index+1, team))

    with open('League_Tables.json', 'w') as fp:
        json.dump(results, fp, ensure_ascii=False)