import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import pylab


def get_team_info(url, major, gender):
    # get team information from the given url
    wb_data = requests.get(url)
    wb_data.encoding = 'gb2312'
    soup = BeautifulSoup(wb_data.text, 'lxml')
    table = soup.find(name='table', attrs={'width': "670"})
    elements = table.find_all(name='tr')
    info = list()
    for element in elements:
        l = []
        td_list = element.find_all(name='td')
        for each_td in td_list:
            l.append(each_td.text.strip())
        info.append(l)

    info.remove(info[0])

    for item in info:
        if len(item) > 20:
            prize = item[20]  # get the prize
            for i in (5, 11, 17):
                major_name = item[i]
                if major_name == '':
                    continue
                prize_list = major.setdefault(major_name, [0, 0, 0, 0])
                if '特' in prize:
                    prize_list[0] += 1
                elif '一' in prize:
                    prize_list[1] += 1
                elif '二' in prize:
                    prize_list[2] += 1
                else:
                    prize_list[3] += 1
                major[major_name] = prize_list
                # Gender part
            team_gender = 0
            for i in (3, 9, 15):  # calculate the gender info
                if item[i] == '男':
                    team_gender += 1
                else:  # '女'
                    pass
            prize = item[20]
            if '特' in prize:
                gender[str(team_gender)][0] += 1
            elif '一' in prize:
                gender[str(team_gender)][1] += 1
            elif '二' in prize:
                gender[str(team_gender)][2] += 1
            else:
                gender[str(team_gender)][3] += 1


if __name__ == '__main__':
    urls = ['http://www.math.zju.edu.cn/mmb/news.asp?newsid={}&tabname=%D0%C2%CE%C5%B6%AF%CC%AC'.format(str(i)) for i in
            range(70, 61, -2)]

    dict_major = {}
    dict_gender = {'0': [0, 0, 0, 0], '1': [0, 0, 0, 0], '2': [0, 0, 0, 0], '3': [0, 0, 0, 0]}

    for one_url in urls:
        get_team_info(one_url, dict_major, dict_gender)

    print('MAJOR:')
    for key, value in dict_major.items():
        print(key, value, sep='                     ,')
    print('----------------------')
    print('GENDER:')
    for key, value in dict_gender.items():
        print(key, value, sep=':')

    n_groups = 4
    prizes = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            prizes[i].append(dict_gender[str(j)][i])

    pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']  # default font

    pylab.mpl.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.3
    opacity = 0.4

    rects1 = plt.bar(index, prizes[0], bar_width / 2, alpha=opacity, color='r', label='特等奖')
    rects2 = plt.bar(index + bar_width / 2, prizes[1], bar_width / 2, alpha=opacity, color='g', label='一等奖')

    rects3 = plt.bar(index + bar_width, prizes[2], bar_width / 2, alpha=opacity, color='c', label='二等奖')
    rects4 = plt.bar(index + 1.5 * bar_width, prizes[3], bar_width / 2, alpha=opacity, color='m', label='参赛奖')

    plt.xlabel('性别组合')
    plt.ylabel('获奖次数')
    plt.title('近5年美赛中不同性别组合队伍的获奖情况')

    plt.xticks(index - 0.2 + 2 * bar_width, ('3女', '2女1男', '1女2男', '3男'), fontsize=16)

    plt.yticks(fontsize=16)  # change the num axis size

    plt.ylim(0, 40)  # The ceil
    plt.legend(bbox_to_anchor=(0.2, 1))
    plt.tight_layout()
    plt.show()
