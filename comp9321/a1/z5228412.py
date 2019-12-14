import matplotlib.pyplot as plt
import pandas as pd
import re

def question_1(file_name_1, file_name_2):
    print("--------------- question_1 ---------------")
    df1 = pd.read_csv(file_name_1)
    df2 = pd.read_csv(file_name_2)
    df1.drop(index = 0, inplace = True)
    df2.drop(index = 0, inplace = True)
    df2.drop(df2.columns[len(df2.columns)-5 : ], axis=1, inplace = True)
    df1_col = ['Country', 'summer_rubbish', 'summer_participation', 'summer_gold', 'summer_silver', 'summer_bronze', 'summer_total']
    df2_col = ['Country', 'winter_participation' , 'winter_gold', 'winter_silver', 'winter_bronze', 'winter_total']
    df1.columns = df1_col
    df2.columns = df2_col
    df = pd.merge(df1, df2, how='left', left_on=['Country'], right_on=['Country'])
    df.drop(index = len(df)-1, inplace = True)
    df_print = df.drop(df.index[5:])
    print(df_print.to_string())
    return df


def question_2(df_name):
    print("--------------- question_2 ---------------")
    for i in range(len(df_name['Country'])):
        col_name = df_name['Country'][i]
        df_name['Country'][i] = re.sub(u" \\(.*?\\)| \\[.*?\\]", "", col_name)
    df_name.set_index('Country', inplace = True)
    drop_list = ['summer_rubbish', 'summer_total', 'winter_total']
    df_name.drop(columns = drop_list, inplace = True)
    df_print = df_name.drop(df_name.index[5:])
    print(df_print.to_string())
    return df_name



def question_3(df_name):
    print("--------------- question_3 ---------------")
    df_name.dropna(axis = 0, how = 'any', inplace = True)
    df_print = df_name.drop(df_name.index[:len(df_name)-10])
    print(df_print.to_string())
    return df_name


def question_4(df_name):
    print("--------------- question_4 ---------------")
    max_s_gold = 0
    for each in df_name['summer_gold']:
        if int(each.replace(',','')) > max_s_gold:
            max_s_gold = int(each.replace(',',''))
    max_list = []
    for each in df_name['summer_gold']:
        if int(each.replace(',','')) == max_s_gold:
            max_list.append(df_name[df_name.summer_gold == each].index.tolist()[0])
    for each in max_list:
        print(each)


def question_5(df_name):
    print("--------------- question_5 ---------------")
    diff_dic = {}
    for index, row in df_name.iterrows():
        diff_dic[index] = abs(int(row['summer_gold'].replace(',','')) - int(row['winter_gold'].replace(',','')))
    max_diff = max(diff_dic.values())
    country = [k for k, v in diff_dic.items() if v == max_diff]
    for each in country:
        print(f'country:{each}\ndifference: {diff_dic[each]}')

def question_6(df_name):
    print("--------------- question_6 ---------------")
    total = [0 for i in range(len(df_name))]
    total_list = ['summer_gold', 'summer_silver', 'summer_bronze', 'winter_gold', 'winter_silver', 'winter_bronze']
    for each_medal in total_list:
        for i in range(len(df_name)):
            total[i] += int(df_name[each_medal][i].replace(',',''))
    df_name['total'] = total
    df_name.sort_values(by = ['total'], ascending  = False, inplace = True )
    df_print = df_name.drop(df_name.index[5:len(df_name)-5])
    print(df_print.to_string())

def add_column(df_name, total, total_list, col_name):
    for each_medal in total_list:
        for i in range(len(df_name)):
            total[i] += int(df_name[each_medal][i].replace(',',''))
    df_name[col_name] = total

def question_7(df_name):
    print("--------------- question_7 ---------------")
    total = [0 for i in range(len(df_name))]
    summer_total = [0 for i in range(len(df_name))]
    winter_total = [0 for i in range(len(df_name))]
    total_list = ['summer_gold', 'summer_silver', 'summer_bronze', 'winter_gold', 'winter_silver', 'winter_bronze']
    summer_total_list = ['summer_gold', 'summer_silver', 'summer_bronze']
    winter_total_list = ['winter_gold', 'winter_silver', 'winter_bronze']
    add_column(df_name, total, total_list, 'total')
    add_column(df_name, summer_total, summer_total_list, 'summer_total')
    add_column(df_name, winter_total, winter_total_list, 'winter_total')
    df_name.sort_values(by = ['total'], ascending  = False, inplace = True )
    drop_list = ['summer_participation', 'summer_gold', 'summer_silver', 'summer_bronze', 'winter_participation', 'winter_gold', 'winter_silver', 'winter_bronze']
    df_plot = df_name.drop(columns = drop_list)
    df_plot.drop(df_plot.index[10:], inplace = True)
    df_plot.sort_values(by = ['total'], ascending  = True, inplace = True )
    country = df_plot.index.tolist()
    summer = df_plot.total.tolist()
    winter = df_plot.winter_total.tolist()

    plt.barh(country,summer, color = 'darkorange')
    plt.barh(country,winter, color = 'royalblue')
    plt.title('Medals for Winter and Summer Games')
    plt.legend(['Summer Games', 'Winter Games'])
    plt.show()



def question_8(df_name):
    print("--------------- question_8 ---------------")
    country_list = [' United States', ' Australia', ' Great Britain', ' Japan', ' New Zealand']
    winter_list = ['winter_gold', 'winter_silver', 'winter_bronze']
    df_5c = df_name.loc[country_list]
    temp = df_5c[winter_list]
    df_5c_w = temp.copy()
    for each_w in winter_list:
        for i in range(5):
            df_5c_w[each_w][i] = int(df_5c_w[each_w][i].replace(',',''))
    df_5c_w.plot.bar()
    plt.title('Winter Games')
    plt.xticks(rotation=0)
    plt.show()


def question_9(df_name):
    print("--------------- question_9 ---------------")
    value = [5, 3, 1]
    summer_list = ['summer_gold', 'summer_silver', 'summer_bronze']
    points = [0 for i in range(len(df_name))]
    rates = [0 for i in range(len(df_name))]
    for i in range(3):
        for j in range(len(df_name)):
            points[j] += int(df_name[summer_list[i]][j].replace(',','')) * value[i]
    for i in range(len(df_name)):
        if int(df_name['summer_participation'][i].replace(',','')):
            rates[i] = points[i] / int(df_name['summer_participation'][i].replace(',',''))
        else:
            rates[i] = 0
    df_name['rates'] = rates
    df_name.sort_values(by = ['rates'], ascending  = False, inplace = True )
    df_print = df_name.drop(df_name.index[5:])
    print(df_print[['rates']])

def add_rates(df_name, season_list, season_participation, season_rates):
    value = [5, 3, 1]
    points = [0 for i in range(len(df_name))]
    rates = [0 for i in range(len(df_name))]
    for i in range(3):
        for j in range(len(df_name)):
            points[j] += int(df_name[season_list[i]][j].replace(',','')) * value[i]
    for i in range(len(df_name)):
        if int(df_name[season_participation][i].replace(',','')):
            rates[i] = points[i] / int(df_name[season_participation][i].replace(',',''))
        else:
            rates[i] = 0
    df_name[season_rates] = rates

def add_annotate(Default_c, Default_df, ax):
    for i,txt in enumerate(Default_c):
        ax.annotate(txt,(Default_df['summer_rates'].tolist()[i],Default_df['winter_rates'].tolist()[i]), fontsize = 6)

def question_10(df_name):
    print("--------------- question_10 ---------------")
    df_country = pd.read_csv('Countries-Continents.csv')
    summer_list = ['summer_gold', 'summer_silver', 'summer_bronze']
    winter_list = ['winter_gold', 'winter_silver', 'winter_bronze']
    add_rates(df_name, summer_list, 'summer_participation', 'summer_rates')
    add_rates(df_name, winter_list, 'winter_participation', 'winter_rates')
    drop_list = ['summer_participation', 'summer_gold', 'summer_silver', 'summer_bronze', 'winter_participation', 'winter_gold', \
                'winter_silver', 'winter_bronze', 'total', 'summer_total', 'winter_total', 'rates']
    df_plot = df_name.drop(columns = drop_list)
    index_list = df_plot.index.tolist()
    index_list = [each[1:] for each in index_list]
    df_plot.index = index_list
    df_plot.reset_index(inplace = True)
    df_plot.rename(columns={'index':'Country'}, inplace = True)
    df_plot = pd.merge(df_plot, df_country, how='left', left_on=['Country'], right_on=['Country'])
    df_plot = df_plot.where(df_plot.notnull(), 'Default')

    Africa_df = df_plot.query('Continent == "Africa"')
    Asia_df = df_plot.query('Continent == "Asia"')
    Europe_df = df_plot.query('Continent == "Europe"')
    North_America_df = df_plot.query('Continent == "North America"')
    Oceania_df = df_plot.query('Continent == "Oceania"')
    South_America_df = df_plot.query('Continent == "South America"')
    Default_df = df_plot.query('Continent == "Default"')

    Africa_c = Africa_df['Country'].tolist()
    Asia_c = Asia_df['Country'].tolist()
    Europe_c = Europe_df['Country'].tolist()
    North_America_c = North_America_df['Country'].tolist()
    Oceania_c = Oceania_df['Country'].tolist()
    South_America_c = South_America_df['Country'].tolist()
    Default_c = Default_df['Country'].tolist()

    ax = Default_df.plot.scatter(x = 'summer_rates', y = 'winter_rates', color = 'grey')
    ax = Africa_df.plot.scatter(x = 'summer_rates', y = 'winter_rates', color = 'black', ax = ax)
    ax = Asia_df.plot.scatter(x = 'summer_rates', y = 'winter_rates', color = 'yellow' , ax = ax)
    ax = Europe_df.plot.scatter(x = 'summer_rates', y = 'winter_rates', color = 'blue', ax = ax)
    ax = North_America_df.plot.scatter(x = 'summer_rates', y = 'winter_rates', color = 'green', ax = ax)
    ax = Oceania_df.plot.scatter(x = 'summer_rates', y = 'winter_rates', color = 'orange', ax = ax)
    ax = South_America_df.plot.scatter(x = 'summer_rates', y = 'winter_rates', color = 'red', ax = ax)
    add_annotate(Default_c, Default_df, ax)
    add_annotate(Africa_c, Africa_df, ax)
    add_annotate(Asia_c, Asia_df, ax)
    add_annotate(Europe_c, Europe_df, ax)
    add_annotate(North_America_c, North_America_df, ax)
    add_annotate(Oceania_c, Oceania_df, ax)
    add_annotate(South_America_c, South_America_df, ax)
    plt.xlabel('Summer Rates')
    plt.ylabel('Winter Rates')
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.legend(['Default', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'])
    plt.grid()
    plt.show()




if __name__ == "__main__":
    csv_name_1 = 'Olympics_dataset1.csv'
    csv_name_2 = 'Olympics_dataset2.csv'
    df_q1 = question_1(csv_name_1, csv_name_2)
    df_q2 = question_2(df_q1)
    df_q3 = question_3(df_q2)
    question_4(df_q3)
    question_5(df_q3)
    question_6(df_q3)
    question_7(df_q3)
    question_8(df_q3)
    question_9(df_q3)
    question_10(df_q3)
