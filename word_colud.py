from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from difflib import SequenceMatcher
import time
from bs4 import BeautifulSoup
import re
import sys

driver = webdriver.Chrome() #또는 chromedriver.exe
driver_options = webdriver.ChromeOptions()
driver_options.add_argument("headless")
driver = webdriver.Chrome(options=driver_options)
driver.implicitly_wait(15) # 묵시적 대기, 활성화를 최대 15초가지 기다린다.
# 페이지 가져오기(이동)
driver.get('https://www.google.com/search?q=%ED%85%8C%EC%8A%A4%ED%8A%B8&oq=%ED%85%8C%EC%8A%A4%ED%8A%B8&gs_lcrp=EgZjaHJvbWUyDAgAEEUYORixAxiABDIQCAEQLhjHARixAxjRAxiABDIKCAIQABixAxiABDINCAMQABiDARixAxiABDIKCAQQABixAxiABDIKCAUQABixAxiABDINCAYQABiDARixAxiABDINCAcQABiDARixAxiABDIHCAgQABiABNIBCDExNThqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8')
result_html = driver.page_source

time.sleep(5)

input_keyword = '''테스트잇 test it!'''
split_keyword = input_keyword.split()
soup = BeautifulSoup(result_html, 'html.parser')

def find_parent_list_tag(data):
    target_tags = []
    extract_text = []
    last_text = str(data.find_parent())
    last_tag = data.find_parent().name
    list_data = data
    if list_data.find_parent('li') != None:
        while list_data:
            list_data = list_data.find_parent()
            # print(data)
            # print('qqqqqqqqqqqqqqqqqqq')
            for i, val in enumerate(list_data.find_all(last_tag)):
                if str(val) == last_text:
                    target_tags.append({'tag' : val.name, 'idx':i })
                    print(target_tags)

            last_tag = list_data.name
            last_text = str(list_data)
            if list_data.name == 'li':
                break
        # 데이터가 리스트로 되어 있을 경우
        for child_tags in list_data.find_parent().find_all('li'):
            target_data = child_tags
            for i in range(len(target_tags)):
                tag_data = target_tags[len(target_tags) -1 - i]
                if len(target_data.find_all(tag_data.get('tag'))) - 1 >= int(tag_data.get('idx')):
                    target_data = target_data.find_all(tag_data.get('tag'))[int(tag_data.get('idx'))]
            extract_text.append(re.sub(r'[\t\n\r\f\v\xa0]+', '',target_data.text))
        return extract_text
    # 자신과 같은 구조의 tag를 찾을때까지 반복
    else:
        while data:
            data = data.find_parent()
            for i, val in enumerate(data.find_all(last_tag)):
                print(str(val) == last_text)
                if str(val) == last_text:
                    target_tags.append({'tag' : val.name, 'idx':i })
                    print(target_tags)
            if data == None:
                break
            for i, val in enumerate(data.find_all(last_tag)):
                if str(val) == last_text:
                    target_tags.append({'tag' : val.name, 'idx':i })
                    print(target_tags)
            if data.find_parent() != None:
                if len(data.find_parent().find_all(target_tags)) > 1:
                    print(target_tags)

            last_tag = list_data.name
            last_text = str(list_data)
            if list_data.name == 'li':
                break
        


test = soup.find_all(string=re.compile('|'.join(split_keyword)), recursive=True)
# print(test)
t = ''
for i, val in enumerate(test):
    # print(val.split())
    t+=''.join(val.split())+ '#idx{}#'.format(str(i))
# print(t)
make_pattern = '(#idx\d+#)?'.join([re.escape(keyword) for keyword in split_keyword]) + '(#idx\d+#)?'
# print('sadasdasdt',t)
pattern = re.compile(make_pattern)

# 문자열에서 패턴 검색
match = pattern.search(t)



if match:
    # input_keyword랑 정확하게 일치할 시
    full_match = match.group(0)
    last_pattern_match = re.search(r'#idx(\d+)#$', full_match)
    if last_pattern_match:
        # 숫자 부분 추출
        number = last_pattern_match.group(1)
        data = test[int(number)]
        text = find_parent_list_tag(data)
        print(text)
        

        # test[int(number)].find_parent('li').children()
        
    else:
        # 일치하는게 없다면 input_keyword와 가장 유사도가 높은 데이털르 가진 tag를 찾는다
        max_similarity = 0
        data = ''
        # print('1', test)
        for i, val in enumerate(test):
            similarity =  SequenceMatcher(None, val, input_keyword).ratio()
            if similarity > max_similarity:
                max_similarity = similarity
                data = val
        text = find_parent_list_tag(data)
        print(text)
else:
    print("패턴과 일치하는 부분이 없습니다.")
# print(t.find(''.join(split_keyword)))
# match_data = pattern.findall(''.join(split_keyword))
# matching_idx = None
# for idx, content in matches:
#     if match_data in content:
#         matching_idx = idx
#         break
# print(matching_idx)
# print(test[5].find_parent())
# # for i in test:
# #     print(i,'asdas')
#     if i.split() == split_keyword:
#         i.find_parent()
# print(test)
# print(text)
# driver.quit() # 웹 브라우저 종료. driver.close()는 탭 종료
# print(soup.p.contents)
# list_of_strings = [print(s) for s in soup.stripped_strings]
# print(list_of_strings[0])

# '<a></a>'.replace()
