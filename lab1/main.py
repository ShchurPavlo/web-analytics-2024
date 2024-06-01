import re
from user_agents import parse
import pandas
import datetime
import geoip2.database
import matplotlib.pyplot as plt


reader = geoip2.database.Reader('.\GeoLite2\GeoLite2-City.mmdb')
def Parse_line(line):
    pattern = re.compile(r'(\d+),'
                         r'"((?:\d{1,3}\.){3}\d{1,3}) - - \[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] ""([A-Z]+ \/[\w%\-./?=]* HTTP\/\d.\d)"" (\d{3}) (\d+) ""(https?:\/\/[\w\-./?=%]*)"" ""([^""]*)"" ""([^""]*)"""')
    match = pattern.match(line)
    if match:
        parameters = match.groups()
        user_agents_obj=parse(parameters[7])
        datetime_obj = datetime.datetime.strptime(parameters[2], '%d/%b/%Y:%H:%M:%S %z')
        return {
            "IP": parameters[1],
            "Country": Get_country(parameters[1]),
            "Date": datetime_obj.date(),
            "Time": datetime_obj.time(),
            "Request type": parameters[3],
            "Request code": parameters[4],
            "Size": int(parameters[5]),
            "Request url": parameters[6],
            "User_agents": parameters[7],
            "Browser": user_agents_obj.browser,
            "OS": user_agents_obj.os.family
        }
    else:
        return None

def Get_data(path):
    data=[]
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            tmp=Parse_line(line)
            if tmp is not None:
                data.append(tmp)
        df = pandas.DataFrame(data)
        return df

def Get_country(ip):
    try:
        response = reader.city(ip)
        return response.country.name
    except Exception:
        return None

def Calc_unic_users(data):
    print("Users by days:")
    result = data.groupby('Date')['IP'].nunique().sort_values(ascending=False)
    print(result)

def Calc_unic_os(data):
    print("Unique IPs:")
    result = data.groupby('OS')['IP'].nunique().sort_values(ascending=False)
    print(result)

def Calc_unic_browser(data):
    print("Unique browsers:")
    result = data.groupby('Browser')['IP'].nunique().sort_values(ascending=False)
    print(result)

def Calc_unic_contry(data):
    print("Countries:")
    result = data.groupby('Country')['IP'].nunique().sort_values(ascending=False)
    print(result)


def Show_unique_bots(data):
    bots = ['Googlebot', 'Bingbot', 'Yahoo! Slurp', 'DuckDuckBot', 'Baiduspider']
    data['Bot'] = data['User_agents'].apply(lambda x: next(
        (bot for bot in bots if bot in x), None))
    unique_bots = data.groupby('Bot')['IP'].nunique()
    print(unique_bots)

def Calculate_z_score(x, mean_val, std_dev):
    return (x - mean_val) / std_dev

def Detect_anomalies(data):

    mean_val = data['Size'].mean()
    std_dev = data['Size'].std()
    data['Size_Z_Score'] = data['Size'].apply(lambda x: Calculate_z_score(x, mean_val, std_dev))

    print (data['Size_Z_Score'])
    df_zscore = data['Size_Z_Score']

    anomalies = data[data['Size_Z_Score'] > 3]
    print(f"Found {len(anomalies)} anomalies")

    # Plot anomalies
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Size'], label='Size', color="blue", alpha=0.25)
    plt.scatter(anomalies.index, anomalies['Size'], color="green", label= "Anomalies", marker="*")
    plt.title(f"Anomalies")
    plt.ylabel('Size')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


data=Get_data("./logs.log")

Calc_unic_users(data)
Calc_unic_os(data)
Calc_unic_browser(data)
Calc_unic_contry(data)
Show_unique_bots(data)

Detect_anomalies(data)
