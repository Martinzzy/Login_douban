import requests
import re

def login():
    headers = {'Referer':'https://www.douban.com/',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
    session = requests.Session()
    response = session.get('https://accounts.douban.com/login',headers=headers)
    result = response.text
    reg = r'<input type="hidden" name="captcha-id" value="(.*?)"/>'
    captcha_id = re.findall(reg,result)
    reg = '<img id="captcha_image" src="(.*?)"'
    imgurl = re.findall(reg,result)[0]
    response = session.get(imgurl,headers=headers)
    result = response.content
    with open('pic.jpg','wb') as f:
        f.write(result)
    data = {
        'captcha-id':captcha_id,
        'captcha-solution':input('请输入验证码:'),
        'form_email':input('请输入账号：'),
        'form_password':input('请输入密码：'),
        'login':'登录',
        'redir':'https://www.douban.com/',
        'source':'index_nav'
        }
    response = session.post('https://accounts.douban.com/login',headers=headers,data=data)
    if '南在南方' in response.text:
        print('登陆成功')
    else:
        print('登陆失败，请重新登陆！')
        return login()


if __name__ == '__main__':
    login()
