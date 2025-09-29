import requests
import json
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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
    
    #sorted_data = sort_processed_data(processed_stats, "rank")
    #print_data(sorted_data)
    plot_data(nation_name, processed_stats)

def fetch_nation_stats(nation_name, config):
    api_url = "https://www.nationstates.net/cgi-bin/api.cgi?nation=${nation_name};q=census;scale=all;mode=score+rank+rrank"
    headers = {'user-agent': config['user-agent']}
    response = requests.get(api_url.replace("${nation_name}", nation_name), headers=headers)
    if response.status_code == 200:
        data = response.text
        return data
    
def process_data(data, stat_IDs):
    processed_stats = []
    excluded_ids = {'65', '66', '80', '81', '82', '83', '84', '86'}
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    census = root.find('CENSUS')
    if census is not None:
        for stat in census.findall('SCALE'):
            id = stat.get('id')
            if id in excluded_ids:
                continue  # Skip processing for excluded IDs
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

# This part was vibe coded, I am not that good with matplotlib
def plot_data(nation_name, data):
    # x-coordinates of bar centers
    centers = [i * 1.5 for i in range(1, len(data) + 1)]

    # heights of bars (invert the rank so higher values are smaller bars)
    height = [1 / int(stat['rrank']) if int(stat['rrank']) > 0 else 0 for stat in data]

    # labels for bars
    tick_label = [stat['name'] for stat in data]

    # Normalize the rank values to a range of 0 to 1 for coloring
    norm = mcolors.Normalize(vmin=1, vmax=22)
    colors = [mcolors.to_hex(plt.cm.RdYlGn(norm(23 - int(stat['rrank'])))) for stat in data]

    # plotting a bar chart
    fig, ax = plt.subplots(figsize=(16, 9))  # Set figure size for better readability
    fig.patch.set_facecolor('#414141')  # Set background color of the chart
    ax.set_facecolor('#414141')  # Set background color of the plot area

    # Maximize the window
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')  # For TkAgg backend
    except AttributeError:
        mng.full_screen_toggle()  # For other backends

    bars = plt.bar(centers, height, tick_label=None, width=1.0, color=colors)

    # naming the x-axis
    plt.xlabel('Statistic Names'.upper(), color='white')
    # naming the y-axis
    plt.ylabel('Region Rank (Taller bar = better rank)'.upper(), color='white')
    # plot title
    plt.title(nation_name.upper() + ' REGIONAL STATISTIC RANKINGS', color='white')

    # Adjust tick label colors and positions
    ax.tick_params(axis='y', colors='white')
    ax.set_xticks(centers)
    ax.set_xticklabels(tick_label, rotation=45, ha='right')

    # Apply gradient colors to tick labels
    for label, color in zip(ax.get_xticklabels(), colors):
        label.set_color(color)

    # Enable horizontal scrolling if needed
    plt.subplots_adjust(bottom=0.3, left=0.05, right=0.95, top=0.9)  # Adjust margins for better spacing
    ax.set_xlim(left=0, right=max(centers) + 1.5)  # Extend x-axis limits

    # function to show the plot
    plt.show()

main()