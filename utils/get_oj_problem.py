# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import html5lib
import requests
import re
from problem.models import Problem
from django.utils.html import format_html


def get_hdu_info(problem_id):
    base_url = 'http://acm.hdu.edu.cn/showproblem.php?pid='
    url = base_url + str(problem_id)

    html = requests.get(url).content.decode('gbk')

    if 'No such problem' in html:
        ots = str(problem_id)+' : No such problem'
        print(ots)
        return False
    if 'System Message' in html:
        ots = str(problem_id) + ' : System error'
        print(ots)
        return False

    soup = BeautifulSoup(html, 'html5lib')
    title = soup.find('h1').string

    limit_text = soup.find('span').get_text()
    limit = re.findall(r"\d+\.?\d*", limit_text)
    # time limit(java/others) | memory limit(java/others) | submission | accepted submission |
    #  1 3 4 5
    time_limit = int(limit[1])
    memory_limit = int(limit[3])
    submission = int(limit[4])
    accepted_submission = int(limit[5])


    # 0 1 2 3 4分别是描述，输入，输出,样例输入，样例输出
    description = {}
    # if len(description) <= 4:# 因为某些题目缺少某些区域,所以只能一个个爬取判断
    # print(str(ProblemID)+" "+str(len(description)))
    reg = "Problem Description</div> <div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[0] = tmp[0] if tmp else "None"

    reg = "Input</div> <div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[1] = tmp[0] if tmp else "None"

    reg = "Output</div> <div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    description[2] = tmp[0] if tmp else "None"

    reg = "Sample Input</div><div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    if tmp:
        reg = 'space;">(.*?)</div></pre>'
        description[3] = re.findall(reg, tmp[0], re.S)[0].replace(' ', '&nbsp;').replace('\n', '<br>')
    else:
        description[3] = "None"

    reg = "Sample Output</div><div class=panel_content>(.*?)</div><div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    if tmp:
        reg = 'space;">(.*?)</div></pre>'
        description[4] = re.findall(reg, tmp[0], re.S)[0].replace(' ', '&nbsp;').replace('\n', '<br>')
    else:
        description[4] = "None"

    reg = "Source</div>\s<div class=panel_content>(.*?)</div>\s<div class=panel_bottom>"
    tmp = re.findall(reg, html, re.S)
    source = ''
    if tmp:
        soup = BeautifulSoup(tmp[0], 'html5lib')
        for string in soup.stripped_strings:
            source = string

    base_img_url = 'http://acm.hdu.edu.cn/'
    for i in range(0, 5):
        if description[i] == 'None':
            raw_input('press enter to continue...')
        if 'src=' in description[i]:
            if "../../" in description[i]:
                description[i] = description[i].replace("../../data/images/", base_img_url + "data/images/")
            else:
                description[i] = description[i].replace("/data/images/", base_img_url + "data/images/")

    return {'title': title, 'time_limit': time_limit, 'memory_limit': memory_limit,
            'description': description[0], 'source': source,
            'input_description': description[1], 'output_description': description[2],
            'input_sample': [description[3]], 'output_sample': [description[4]],
            'submission': submission, 'accepted_submission': accepted_submission}


#  print(get_hdu_info(6010))
def import_hdu_problem(problem_id):
    oj_name = 'HDU'
    res = get_hdu_info(problem_id)
    if not res:
        return False

    _input_sample = ''
    _output_sample = ''
    if len(res['input_sample']) == 1:
        _input_sample = str(res['input_sample'][0])
    else:
        cnt = 0
        for ins in res['input_sample']:
            cnt += 1
            _input_sample += "样例 " + str(cnt) + " : <br>"
            _input_sample += str(ins)

    if len(res['output_sample']) == 1:
        _output_sample = str(res['output_sample'][0])
    else:
        cnt = 0
        for ous in res['output_sample']:
            cnt += 1
            _output_sample += "样例 " + str(cnt) + " : <br>"
            _output_sample += str(ous)

    Problem.objects.update_or_create(
        oj_name=oj_name,
        virtual_id=problem_id,
        defaults={'title': res['title'],
                  'source': res['source'],
                  'os': 'Windows',
                  'time_limit': res['time_limit'],
                  'memory_limit': res['memory_limit'],
                  'description': res['description'],
                  'input_description': res['input_description'],
                  'output_description': res['output_description'],
                  'input_sample': _input_sample,
                  'output_sample': _output_sample,
                  'remote_submission_user_number': res['submission'],
                  'remote_accepted_user_number': res['accepted_submission'],
                  'hint': 'auto import',
                  },
    )
    print(oj_name + str(problem_id) + " : success!")
    return True
