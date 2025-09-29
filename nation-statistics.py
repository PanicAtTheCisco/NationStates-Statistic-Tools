import requests
import json
import xml.etree.ElementTree as ET

def main():
    nation_name = input("Enter the nation name: ").lower()

    config = {}
    with open('config.json', 'r') as f:
        config = json.load(f)

    stat_IDs = {}
    with open('stat_IDs.json', 'r') as f:
        stat_IDs = json.load(f)

    data = fetch_nation_stats(nation_name, config)
    if data:
        processed_stats = process_data(data, stat_IDs)
    else:
        print(f"Failed to fetch ${nation_name} statistics.")
    
    sorted_data = sort_processed_data(processed_stats, "rank")
    print_data(sorted_data)

def fetch_nation_stats(nation_name, config):
    api_url = "https://www.nationstates.net/cgi-bin/api.cgi?nation=${nation_name};q=census;scale=all;mode=score+rank+rrank"
    headers = {'user-agent': config['user-agent']}
    response = requests.get(api_url.replace("${nation_name}", nation_name), headers=headers)
    if response.status_code == 200:
        data = response.text
        return data
    
def process_data(data, stat_IDs):
    processed_stats = []
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    census = root.find('CENSUS')
    if census is not None:
        for stat in census.findall('SCALE'):
            id = stat.get('id')
            score = stat.find('SCORE').text
            rank = stat.find('RANK').text
            rrank = stat.find('RRANK').text
            stat_name = ""
            if id in stat_IDs:
                stat_name = stat_IDs[id]
            else:
                stat_name = "Unknown Stat"
            processed_stats.append({
                'id': id,
                'name': stat_name,
                'score': score,
                'rank': rank,
                'rrank': rrank
            })
    return processed_stats

def sort_processed_data(processed_stats, sort_by):
    return sorted(processed_stats, key=lambda x: int(x[sort_by]))

def print_data(data):
    for stat in data:
        print(f"Stat Name: {stat['name']}, Score: {stat['score']}, World Rank: {stat['rank']}, Region Rank: {stat['rrank']}")

main()