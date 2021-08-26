import os
import re
import csv
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


###########################################
# Put the Game URL below inside the quotes
###########################################
GAME_URL = 'https://www.whoscored.com/Matches/1549554/Live/England-Premier-League-2021-2022-Liverpool-Burnley'
#############################################
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#############################################

csv_columns = ['minute', 'second', 'teamName', 'x', 'y', 'period', 'type', 'outcome', 'playerId', 'playerName', 'endX', 'endY']

def main():
    try:
        print('\n...\n- Starting the process')
        print('- GAME_URL : {}'.format(GAME_URL))
        print('- Getting data from URL, please wait (might take few seconds)')
        
        options = Options()
        options.headless = True
        
        with webdriver.Firefox(executable_path=r'driver\geckodriver.exe',service_log_path=os.path.devnull, options=options) as driver:
            driver.get(GAME_URL)
            response = driver.page_source
        
        
        if 'formationIdNameMappings' in response:
            pointer = re.search("matchCentreData.*", response)
            if pointer:
                print('- Data gathered successfully')
                print('- Parsing data now')
                
                response = pointer.group()
                response = '{' + response.replace('matchCentreData','"matchCentreData"').rstrip(',') + '}'
                json_data = json.loads(response)
                
                response = ''
                pointer = ''
                
                players = json_data['matchCentreData']['playerIdNameDictionary']
                teams = [{'team_id':json_data['matchCentreData']['home']['teamId'], 'team_name':json_data['matchCentreData']['home']['name']},
                        {'team_id':json_data['matchCentreData']['away']['teamId'], 'team_name':json_data['matchCentreData']['away']['name']}]
                json_data = json_data['matchCentreData']['events']
                
                events = []
                for event in json_data:
                    try:
                        new_event = {}
                        
                        if 'minute' in event:
                            new_event['minute'] = event['minute']
                        else:
                            new_event['minute'] = ''
                            
                        
                        if 'second' in event:
                            new_event['second'] = event['second']
                        else:
                            new_event['second'] = ''
                            
                            
                        if 'teamId' in event:
                            new_event['teamId'] = event['teamId']
                            found = [team for team in teams if team['team_id'].__eq__(new_event['teamId'])]
                            if found:
                                new_event['teamName'] = found[0]['team_name']
                        else:
                            new_event['teamId'] = ''
                            new_event['teamName'] = ''
                        
                        
                        if 'x' in event:
                            new_event['x'] = event['x']
                        else:
                            new_event['x'] = ''
                            
                            
                        if 'y' in event:
                            new_event['y'] = event['y']
                        else:
                            new_event['y'] = ''
                            
                            
                        if 'period' in event:
                            new_event['period'] = event['period']['displayName']
                        else:
                            new_event['period'] = ''
                            
                            
                        if 'type' in event:
                            new_event['type'] = event['type']['displayName']
                        else:
                            new_event['type'] = ''
                            
                        if 'outcomeType' in event:
                            new_event['outcome'] = event['outcomeType']['displayName']
                        else:
                            new_event['outcome']  = ''
                            
                            
                        if 'playerId' in event:
                            new_event['playerId'] = event['playerId']
                            # found = [name for name, pid in players.items() if pid == str(new_event['playerId'])]
                            # if found:
                            #     new_event['players'] = found[0]
                            try:
                                for player in players:
                                    if player == str(new_event['playerId']):
                                        new_event['playerName'] = players[player]
                                        break
                            except Exception as exc:
                                pass
                        else:
                            new_event['playerId'] = ''
                            new_event['playerName'] = ''
                            
                            
                        if 'endX' in event:
                            new_event['endX'] = event['endX']
                        else:
                            new_event['endX'] = ''
                        
                        if 'endY' in event:
                            new_event['endY'] = event['endY']
                        else:
                            new_event['endY'] = ''
                        
                        # print(new_event)
                        events.append(new_event)
                    except Exception as ex:
                        print('########## INSIDE EVENTS LOOP => {}'.format(str(ex)))
                        
                export_to_csv(events)
            else:
                print('No data found')
        else:
            print('No data found')
    except Exception as ex:
        print('Exception occured in main => {}'.format(str(ex)))
    
    print('press any key to close...')
    input()
    

def export_to_csv(results):
    file_name = GAME_URL.split('/')[-1] + '.csv'
    
    print('- Exporting data to file now.')

    try:
        with open(file_name, "a", newline='' , encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            
            for d in results:
                try:
                    data = {'minute': d['minute'], 'second': d['second'], 'teamName': d['teamName'], 'x': d['x'], 'y': d['y'], 'period': d['period'],
                            'type': d['type'], 'outcome': d['outcome'], 'playerId': d['playerId'], 'playerName': d['playerName'], 'endX': d['endX'], 'endY': d['endY'] }
                    writer.writerow(data)
                except Exception as exc:
                    print('exportToCSV()=> '+ str(exc))
                    
        
        
        print('.')    
        print('- Data exported to CSV --> [{}]'.format(file_name))
        print('.')
        print('.')
        print('.')
        print('############ ALL CAUGHT UP ############')
        print('.')
        print('##### Program is terminating Now #####')
        print('######################################')
        
    except Exception as ex:
        print("exportToCSV()=> " + str(ex))
        

if __name__ == '__main__':
    main()