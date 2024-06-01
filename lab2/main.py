import pandas
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor

def Get_data():

    users_df=pandas.read_csv('users.csv',delimiter=',', names=['Date', 'Users'])
    users_df['Users'] = users_df['Users'].astype(int)
    users_df['Date'] = pandas.to_datetime(users_df['Date'], format="%d.%m.%y")
    print(users_df)

    time_df = pandas.read_csv("time.csv",delimiter=',', names=['Date', 'Duration'])
    time_df['Date'] = pandas.to_datetime(time_df['Date'], format="%d.%m.%y")
    time_df['Duration'] = pandas.to_datetime(time_df['Duration'], format='%H:%M:%S')
    time_df['Duration'] =time_df['Duration'].dt.hour * 3600 + time_df['Duration'].dt.minute * 60 + time_df['Duration'].dt.second
    print(time_df)


    pages_df = pandas.read_csv("pages.csv",delimiter=',', names=['Date', 'Pages'])
    pages_df['Date'] = pandas.to_datetime(pages_df['Date'], format="%d.%m.%y")
    pages_df['Pages'] = pages_df['Pages'].astype(float)
    print(pages_df)

    return (users_df,time_df,pages_df)

def Show_plot(df_anomalies,df,title,color):
    size = len(df_anomalies)
    plt.figure(figsize=(10, 6))
    plt.plot(df.iloc[:, 0], df.iloc[:, 1],color=color)
    plt.scatter(df_anomalies.iloc[:, 0], df_anomalies.iloc[:, 1], color='red')
    plt.xlabel(df.columns[0])
    plt.ylabel(df.columns[1])
    plt.title(title+f' ({size} anomalies)')
    #plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



# Local Outlier Factor (LOF)
def Calculate_LOF(df):
    X = df.iloc[:, 1].values.reshape(-1, 1)
    lof = LocalOutlierFactor(n_neighbors = 19)
    anomaly_scores = lof.fit_predict(X)
    df['LOF_score'] = anomaly_scores
    return df

def Calculate_z_score(df):
    mean_val = df.iloc[:, 1].mean()
    std_dev = df.iloc[:, 1].std()
    df['Z_score'] = (df.iloc[:, 1] - mean_val) / std_dev
    return df

def Calculate_IQR(df):
    a = 1.2
    q1 = df.iloc[:, 1].quantile(0.25)
    q3 = df.iloc[:, 1].quantile(0.75)
    iqr=q3-q1
    lower_bound = q1 - (a * iqr)
    upper_bound = q3 + (a * iqr)
    print(lower_bound)
    print(upper_bound)
    df_anomalies = df[(df.iloc[:, 1] < lower_bound)| (df.iloc[:, 1] > upper_bound)]
    return df_anomalies




users_df,time_df,pages_df=Get_data()


df=Calculate_z_score(users_df)
df_filtered = df[df['Z_score'] > 2]
Show_plot(df_filtered,df,'Z-score',"green")

df=Calculate_z_score(time_df)
df_filtered = df[df['Z_score'] > 2]
Show_plot(df_filtered,df,'Z-score',"blue")

df=Calculate_z_score(pages_df)
df_filtered = df[df['Z_score'] > 2]
Show_plot(df_filtered,df,'Z-score',"black")
# Виведення даних на графік

df=Calculate_LOF(users_df)
df_filtered = df[df['LOF_score'] == -1]
Show_plot(df_filtered,df,'LOF-score',"green")

df=Calculate_LOF(time_df)
df_filtered = df[df['LOF_score'] == -1]
Show_plot(df_filtered,df,'LOF-score',"blue")

df=Calculate_LOF(pages_df)
df_filtered = df[df['LOF_score'] == -1]
Show_plot(df_filtered,df,'LOF-score',"black")

df=Calculate_IQR(users_df)
Show_plot(df,users_df,'IQR-score',"green")

df=Calculate_IQR(time_df)
Show_plot(df,time_df,'IQR-score',"blue")

df=Calculate_IQR(pages_df)
Show_plot(df,pages_df,'IQR-score',"black")