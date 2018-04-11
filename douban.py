import re
import requests
import chardet
from PIL import Image
from requests.exceptions import ConnectionError


class Douban(object):


    def __init__(self,url):
        self.headers =  {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"}
        self.url = url
        self.session = requests.session()


    def get_html(self):
        try:
            response = self.session.get(self.url,headers=self.headers)
            if response.status_code == 200:
                response.encoding = chardet.detect(response.content)['encoding']
                html = response.text
                return html
            return None
        except ConnectionError:
            print('请求初始页失败')
            return None


    def get_captcha(self):
        data = self.get_html()
        if data and "captcha_image" in data:
            reg = r'<img id="captcha_image" src="(.*?)" alt="captcha"'
            pattern = re.compile(reg)
            captcha_url = re.findall(pattern,data)[0].replace('amp;','')
            reg = r'<input type="hidden" name="captcha-id" value="(.*?)"/>'
            captcha_id = re.search(reg,data).group(1)
            image_data = self.session.get(url=captcha_url,headers=self.headers)
            if image_data:
                with open('captcha.jpg','wb') as f:
                    f.write(image_data.content)
                    f.close()
                image = Image.open('captcha.jpg')
                image.show()
                captcha = input('请输入验证码:')
                return captcha_id,captcha


    def login(self,username,password):
        try:
            captcha_id,captcha = self.get_captcha()
            from_data = {
                'captcha-id':captcha_id,
                'captcha-solution':captcha,
                'form_email':username,
                'form_password':password,
                'login':'登录',
                'redir':'https://www.douban.com/',
                'source	':'None'
                }
            res = self.session.post(url=self.url,data=from_data,headers=self.headers)
            if res.status_code == 200:
                res.encoding = chardet.detect(res.content)['encoding']
                if "南在南方" in res.text:
                    print('登陆成功')
            return None
        except ConnectionError:
            print('登陆失败')
            return None


if __name__ == '__main__':
    url = 'https://accounts.douban.com/login'
    douban = Douban(url)
    username = 用户名
    password = 密码
    captcha = douban.login(username,password)
