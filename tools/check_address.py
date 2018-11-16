
import time  # for log
import requests  # for http request
import traceback
import json

address_file = 'address.txt'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'


def log(msg: str):
    '''
    print msg as log
    '''
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    line = f'[{time_str}] {msg}'
    print(line)


def get_all_urls() -> [str]:
    '''
    从指定文件中读取所有地址
    '''
    urls = list()
    with open(file=address_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            urls.append(line.split(' ')[0])

    return urls


def get_response_from(url: str) -> requests.Response:
    '''
    使用套路请求指定地址
    '''
    if not url.startswith('http'):
        url = f'http://{url}'
    response = requests.get(url, headers={'User-Agent': UA})
    return response


def check_url(url: str) -> int:
    '''
    向目标地址发送GET请求，返回相应中的http状态码
    '''

    try:
        response = get_response_from(url)
        return response.status_code
    except:
        traceback.print_exc()
    return -1


def get_new_location(url: str) -> str:
    '''
    获取302或者301跳转地址的新地址
    '''
    response = get_response_from(url)
    location = ''
    if response.status_code == 301 or response.status_code == 302:
        location = response.headers.get('location', '')
        if location == '':
            location = response.headers.get('Location', '')
    return location


def main():
    urls = get_all_urls()
    file_lines = list()
    while len(urls) > 0:
        url = urls.pop().strip()
        if url == '':
            continue
        status_code = check_url(url=url)
        log(f'{status_code} - {url}')
        time_str = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        file_lines.append(f'{url} {status_code} {time_str}\n')
        if status_code == 301 or status_code == 302:  # 跳转地址
            new_location = get_new_location(url)  # 提取新地址
            if new_location != '':
                urls.append(new_location)  # 加入url列表
    with open(file=address_file, mode='w', encoding='utf-8') as f:
        f.writelines(file_lines)


if __name__ == '__main__':
    log('Start')
    main()
    log('Finish')

