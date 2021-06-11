import requests
import json
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup
import base64
import re
import argparse
import subprocess
import time
from threading import Thread
# import random 


class cowin():

    def __init__(self,mobile,dose,dist,mode,test,verbose,vaccine_type,preferences,time,people,booking_dates,pincode):
        self.mobile = mobile
        self.dose = dose
        self.session = requests.Session()
        self.token = None
        self.date = datetime.now().strftime("%d-%m-%Y")
        self.data = None
        self.dist_id = 1 if test else  dist
        self.beneficiaries = None
        self.slots = None
        self.mode = mode
        self.success_rate = 0
        self.test = test
        self.efficiency = False
        self.verbose = verbose
        self.status = []
        self.vaccine_type = vaccine_type
        self.preferences = preferences
        self.time = time
        self.txn_id = None
        self.people = people
        self.booking_dates = booking_dates
        self.pincode = pincode
        self.otp = None
        self.start = False
        self.hybrid = True               # hybrid state polls two different api endpoints for same data sequentially (used by default when filtering by dates option is  choosen)
                                         # hybrid mode balances token banning time and accuracy of data
        self.apis = {
        'generateOtp':'https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP',
        'confirmOtp':'https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp',
        'beneficiaries':'https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries',
        'centers':f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={self.dist_id}&date={self.date}',
        'centers_pincode':f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode={self.pincode}&date={self.date}',
        'recaptcha':'https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha',
        'shedule':'https://cdn-api.co-vin.in/api/v2/appointment/schedule'
        }
        self.session.headers.update({
        'Host': 'cdn-api.co-vin.in',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin':'https://selfregistration.cowin.gov.in',
        'Connection': 'keep-alive',
        'Referer': 'https://selfregistration.cowin.gov.in/',
        'TE': 'Trailers'
        })


    def generate_otp(self):              #otp generation

        self.data = {
         "secret":"U2FsdGVkX1/v/ULtE0/WYbelFEvbha4gZNXtBWNc5qle8pbpTnfQBC6jBo+15xXw6JDgRqRjQs9CJymrQtBFPA==",
         "mobile":self.mobile
           }

        if self.session.headers.get('Authorization'):
            self.session.headers.pop('Authorization')

        try:
            res = self.session.post(self.apis['generateOtp'], data=json.dumps(self.data))
            self.txn_id = res.json()['txnId']
            self.login()
        except :
            print('[-] login failed')
            exit(0)


    def login(self):                   #fetches auth token

        while not self.otp:

            if self.mode == 'm':
                self.otp = input('otp:')

            else:
                try:
                    old_msg = ''
                    if self.verbose:
                        print('[*] 𝓪𝓬𝓬𝓮𝓼𝓼𝓲𝓷𝓰 𝓸𝓽𝓹..')

                    msg = subprocess.Popen('termux-sms-list -l 1',stdout=subprocess.PIPE,shell=True).communicate()[0].decode()
                    msg = json.loads(msg)[0]['body']

                    if "cowin" in msg.lower() and old_msg != msg:
                        self.otp = re.findall("(\d{6})",msg)[0]
                        old_msg = msg
                except :
                    print('[-] 𝕥𝕖𝕣𝕞𝕦𝕩 𝕒𝕡𝕚 𝕞𝕚𝕤𝕤𝕚𝕟𝕘..')
                    exit(0)



            if self.otp:

                self.data = {
                    'otp':hashlib.sha256(self.otp.encode()).hexdigest(),
                    'txnId':self.txn_id
                    }

                res = self.session.post(self.apis['confirmOtp'], data=json.dumps(self.data))

                if res.status_code == 400:
                    print('[*] 𝓪𝓬𝓮𝓼𝓼𝓲𝓷𝓰 𝓸𝓽𝓹 𝓪𝓰𝓪𝓲𝓷!!') if self.mode == 'a' else print('𝔂𝓸𝓾 𝓱𝓪𝓿𝓮 𝓰𝓲𝓿𝓮𝓷 𝓪 𝔀𝓻𝓸𝓷𝓰 𝓸𝓽𝓹!!..')
                    self.otp = None
                else:
                    self.token = res.json()['token']

                    self.session.headers.update(
                        {
                        'Authorization': f'Bearer {self.token}'
                        })

                    with open('token.txt' ,'w') as f:
                        f.write(self.token)
                    print('[+] 𝓵𝓸𝓰𝓲𝓷 𝓼𝓾𝓬𝓮𝓼𝓼...\n')

            time.sleep(2)

        self.otp = None


    def get_details(self):              #gets the beneficiaries data associated with the given mobile number

        beneficiaries = []
        self.start = False

        if self.token == None:
            with open('token.txt','r') as f:
                self.token = f.read()

            self.session.headers.update(
            {
            'Authorization': f'Bearer {self.token}'
            })

        try:
            if not self.efficiency:
                print('[*] 𝓯𝓮𝓽𝓬𝓱𝓲𝓷𝓰 𝓫𝓮𝓷𝓮𝓯𝓲𝓬𝓲𝓪𝓻𝓲𝓮𝓼...\n')

                res = self.session.get(self.apis['beneficiaries'])
                if res.ok:
                    print('[+] 𝓼𝓾𝓬𝓮𝓼𝓼𝓯𝓾𝓵𝓵𝔂 𝓯𝓮𝓽𝓬𝓱𝓮𝓭 𝓫𝓮𝓷𝓮𝓯𝓲𝓬𝓲𝓪𝓻𝓲𝓮𝓼!! ')

                for beneficiary in res.json()['beneficiaries']:
                    if not beneficiary['appointments']:
                        beneficiaries.append(
                        {'id':beneficiary['beneficiary_reference_id'],
                        'name':beneficiary['name'],
                        'age':2021 - int(beneficiary['birth_year'])
                        })

                self.efficiency = True
                self.beneficiaries =  [list(filter(lambda x:x['age']>=45,beneficiaries))[0]] if self.test else beneficiaries
                self.success_rate = len(self.beneficiaries)

            if self.verbose:
                print(f'[+] {json.dumps(self.beneficiaries, indent=4)}')


            if self.beneficiaries:
                return  self.check_slot()
            else:
                print('[-] 𝕖𝕧𝕖𝕣𝕪𝕠𝕟𝕖 𝕚𝕤 𝕧𝕒𝕔𝕔𝕚𝕟𝕒𝕥𝕖𝕕/𝕓𝕠𝕠𝕜𝕖𝕕 ,𝕖𝕞𝕡𝕥𝕪 𝕝𝕚𝕤𝕥!!')
                exit(code=0)


        except (json.decoder.JSONDecodeError,ValueError):
             print('[*] 𝕗𝕚𝕩𝕚𝕟𝕘 𝕖𝕣𝕣𝕠𝕣𝕤... ')
             self.start = True
             self.generate_otp()


        except Exception as e:
            print(f'[-] {e} \n[-] exiting program!!')
            exit(0)


    def check_slot(self):               # polls for vaccination sessions by pincode/district or in hybrid mode

        print('\n[*] 𝓯𝓮𝓽𝓬𝓱𝓲𝓷𝓰 𝓿𝓪𝓬𝓬𝓲𝓷𝓮 𝓼𝓵𝓸𝓽𝓼')
        slots = []

        try:

            if self.booking_dates and  self.hybrid:

                self.hybrid = not self.hybrid

                for date in self.booking_dates:

                    date = re.sub("^\d{2}",str(date),self.date)
                    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/findByPin?pincode={self.pincode}&date={date}' if self.pincode  else f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/findByDistrict?district_id={self.dist_id}&date={date}'
                    res = self.session.get(url)

                    if res.ok:
                        for session in res.json()['sessions']:
                            if session['fee'] == "0" and session[f'available_capacity_dose{self.dose}'] != 0 :
                                slots.append({
                                'id':session['center_id'],
                                'session_id':session['session_id'],
                                'name':session['name'],
                                'age_limit':session['min_age_limit'],
                                'vaccine':session['vaccine'].lower(),
                                f'dose{self.dose}':session[f'available_capacity_dose{self.dose}'],
                                'slot':session['slots'][self.time],
                                'date':session['date']
                                })

            else:

                self.hybrid = not self.hybrid

                res = self.session.get(self.apis['centers_pincode']) if self.pincode else  self.session.get(self.apis['centers'])

                if res.ok:
                    for center in res.json()['centers']:
                        if center['fee_type'] == 'Free':
                            for session in center['sessions']:
                                if session[f'available_capacity_dose{self.dose}'] != 0 :
                                    slots.append({
                                    'id':center['center_id'],
                                    'session_id':session['session_id'],
                                    'name':center['name'],
                                    'age_limit':session['min_age_limit'],
                                    'vaccine':session['vaccine'].lower(),
                                    f'dose{self.dose}':session[f'available_capacity_dose{self.dose}'],
                                    'slot':session['slots'][self.time],
                                    'date':session['date']
                                    })


            if res.status_code != 200:
                if res.status_code == 204:
                    print('[*] 𝖘𝖊𝖗𝖛𝖊𝖗 𝖒𝖎𝖌𝖍𝖙 𝖍𝖆𝖛𝖘𝖊𝖗𝖛𝖊𝖗 𝖒𝖎𝖌𝖍𝖙 𝖍𝖆𝖛𝖊 𝖉𝖊𝖙𝖊𝖈𝖙𝖊𝖉 𝖇𝖔𝖙 𝖆𝖈𝖙𝖎𝖛𝖎𝖙𝖞.. 𝖘𝖑𝖊𝖊𝖕𝖎𝖓𝖌 𝖋𝖔𝖗 յշօ 𝖘𝖊𝖈𝖔𝖓𝖉𝖘𝖊 𝖉𝖊𝖙𝖊𝖈𝖙𝖊𝖉 𝖇𝖔𝖙 𝖆𝖈𝖙𝖎𝖛𝖎𝖙𝖞.. 𝖘𝖑𝖊𝖊𝖕𝖎𝖓𝖌 𝖋𝖔𝖗 յշօ 𝖘𝖊𝖈𝖔𝖓𝖉𝖘')
                    time.sleep(120)
                    print('[*] 𝖙𝖗𝖞𝖎𝖓𝖌 𝖆𝖌𝖆𝖎𝖓 ...')
                    res = self.session.get(self.apis['centers'])

                    if res.status_code == 204:
                        print('[*] 𝓯𝓻𝓮𝓼𝓱 𝓼𝓽𝓪𝓻𝓽!!')
                        raise json.decoder.JSONDecodeError('bot detecetd error','403',0)
                else:
                    raise json.decoder.JSONDecodeError('bot detecetd error','403',0)


            with open('log.txt','a') as f:
                f.write(f'[*] looking for  slots at => {datetime.now().strftime("%d-%m-%Y => %H:%M:%S")}\n')    #logging date and time when vaccine slots were polled for


            if self.verbose:
                print('[*] availbale slots are :: \n')
                print(f'[+] {json.dumps(slots, indent=4)}')

            self.slots =  slots

            if self.slots:
                return True
            else:
                print('\n[-] 𝓷𝓸 𝓼𝓵𝓸𝓽𝓼 𝓪𝓿𝓪𝓲𝓵𝓪𝓫𝓵𝓮...')
                return 0

        except json.decoder.JSONDecodeError:
            print('[-] 𝕖𝕣𝕣𝕠𝕣 𝕚𝕟 𝕗𝕖𝕥𝕔𝕙𝕚𝕟𝕘 𝕤𝕝𝕠𝕥𝕤')
            self.generate_otp()


    def solve_captcha(self):   #solves captcha

        print('[*] 𝓼𝓸𝓵𝓿𝓲𝓷𝓰 𝓬𝓪𝓹𝓽𝓬𝓱𝓪...')

        data = '{}'

        res = self.session.post(self.apis['recaptcha'],data = data)

        if res.status_code != 200:
            self.generate_otp()
            res = self.session.post(self.apis['recaptcha'],data = data)

        captcha = res.json()['captcha']

        captcha_dict = {'MLLQLLQLLQLLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLLQLLQZMLLQLLQLLQLLQZ': '0', 'MLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLZ': '1', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQLLLQLLQZ': '2', 'MLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLLQLLQLLQLLQLLQLLQLLLLQLLQLLQLLQLLQLLQLLLLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': '3', 'MLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLQLLLQLLLQLLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQZMLLQLLQLLQLLQLLQZ': '4', 'MLLQLLQLLQLLQLLQLLQLLQLLLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLLLLQLLLQLLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLLQLLQLLQLLQLLQZ': '5', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQZ': '6', 'MLLQLLQLLLQLLQLLQLLQLLQLLLQLLQLLLQLLQLLQLLLQLLQLLQLLQLLQZMLLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLLLQLLQLLQLLQLLQLLLQLLLQLLQLLQLLLQZ': '7', 'MLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQZMLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLLQLLQLLQLLQLLLLLQLLQLLQLLQLLLLQLLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLQZ': '8', 'MLLLQLLQLLQLLQLLQLLQLLQLLQZMLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': '9', 'MLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQZMLLLQLLQLLQLLQLLQLLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLLQZ': 'A', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQZMLLQLLQLLQLLQLLLQLLQLLQLLQZMLLLQLLLLLQLLLQLLQLLQLLQLLQLLQZ': 'B', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'C', 'MLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQZ': 'D', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'E', 'MLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQZ': 'F', 'MLLQLLQLLQLLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQZMLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLZ': 'G', 'MLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'H', 'MLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'l', 'MLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'J', 'MLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLLLLQZMLLQLLQLLQLLLQLLQLLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'K', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'L', 'MLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQZ': 'M', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLZMLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'N', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQZ': 'O', 'MLLQLLQLLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQZ': 'P', 'MLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLLQLLLQLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLLLLQLLQLLQZ': 'Q', 'MLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLLQLLQLLQZMLLLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLQLLQZ': 'R', 'MLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLLQLLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'S', 'MLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'T', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'U', 'MLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'V', 'MLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLLQLLQLLQLLQLLQLLQLLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQZ': 'W', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQZ': 'X', 'MLLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLZ': 'Y', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLLQLLQLLQLLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQZ': 'Z', 'MLLQLLQLLQLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQZMLLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQZ': 'a', 'MLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQZ': 'b', 'MLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLLQLLQLLQZ': 'c', 'MLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQZ': 'd', 'MLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLLQZMLLQLLQLLQLLQLLQZMLLQLLLLQLLQLLQZ': 'e', 'MLLQLLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQZMLLQLLQLLLQLLQLLQLLQLLQLLLQLLQLLLQLLLLQLLQLLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQZ': 'f', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLLQLLLQLLQLLQLLLQLLQLLQLLQLLLLQLLQLLQLLQLLQLLLQLLLQLLQLLLQLLLQZMLLQLLQLLQLLQLLQLLQLLQLLQZ': 'g', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQLLQZ': 'h', 'MLLQLLLQLLQLLQLLQZMLLQLLQLLQLLQLZMLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQZMLLLLQLLQLLQLLQLLQLLQLLQZ': 'i', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQZMLLQLLQLLZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLLQLLQLLQLLQLLQLLLQLLLLQLLQZMLLLQLLQLLQLLQLLQLLQLLQZ': 'j', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQZMLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'k', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQLLQLLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLLQLLQZMLLLZ': 'm', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'n', 'MLLQLLQLLQLLQLLQLLQLLQZMLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLLQLLQLLQLLQLLQLLQLLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQZ': 'o', 'MLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLLQLLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLLLLQLLLQLLQLLLQLLQLLQLLLQLLQLLQLLQLLQLZMLLQLLQLLQLLQLLLQLLLQLLLQLLQZ': 'p', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'q', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLZMLLLZ': 'r', 'MLLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLLLQLLQLLQLLLQLLQZ': 's', 'MLLQLLQLLQLLQLLLQLLQLLQLLLQLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLLQLLQLLQLLQLLQLLQLLQLLLQLLLQLLQLLQZ': 't', 'MLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLLLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQZ': 'u', 'MLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLLQLLLQZ': 'v', 'MLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQZMLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLLQLLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLZ': 'w', 'MLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLLQZ': 'x', 'MLLQLLQLLQLLQLLQLLQLLQLLLQLLQZMLLQLLLQLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLQZ': 'y', 'MLLQLLQLLQLLQLLQLLQLLQLLLQLLQLLQLLQLLQLLQZMLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLQLLLQLLLQLLQLLQLLQLLQLLQLLQLLQLLQZ': 'z'}

        soup = BeautifulSoup(captcha,'html.parser')
        captcha_holder = {}

        for path in soup.find_all('path',{"fill" : re.compile('#')}):
        	captcha_holder[int(re.findall('M(\d+)',path.get('d'))[0])] = captcha_dict.get(''.join(re.findall('([A-Z])',path.get('d'))))
                # matches captcha characters from the captcha dictionary to recreate/gusess the captcha

        captcha_string = ''

        for i in sorted(captcha_holder):
        	captcha_string += captcha_holder.get(i)

        if self.verbose:
            print('[+] captcha solved!! ...\n')

        return captcha_string


    def book_vaccine(self,b,s):     # books vaccine for individual beneficiaries

        print(f"[+] 𝙗𝙤𝙤𝙠𝙞𝙣𝙜 𝙫𝙖𝙘𝙘𝙞𝙣𝙚 𝙛𝙤𝙧 {b['name']}")

        self.data = {
        "center_id":s['id'],
        "session_id":s['session_id'],
        "beneficiaries":[b['id']],
        "slot":s['slot'],
        "captcha":self.solve_captcha(),
        "dose": self.dose
                }

        print(f'\n[+]booking detals {json.dumps(self.data, indent=4)}\n\n')

        res = self.session.post(self.apis['shedule'],data = json.dumps(self.data))

        if res.status_code == 200:
            print(f'[+] 𝓫𝓸𝓸𝓴𝓲𝓷𝓰 𝓼𝓾𝓬𝓮𝓼𝓼𝓯𝓾𝓵𝓵 \n {json.dumps(res.json(),indent=4)}')
            try:
                subprocess.call(f'termux-notification -c vaccine sheduled for {b["name"]}!! --sound', shell=True)
            except:
                pass
            self.success_rate -= 1
            self.efficiency = False
            self.status.append({'name':b['name'],'data':self.data,'sucess':True})
            self.create_pdf(res.json()['appointment_confirmation_no'],b['name'])
        else:
            print(f"[-] 𝙛𝙖𝙞𝙡𝙚𝙙 𝙗𝙤𝙤𝙠𝙞𝙣𝙜 𝙫𝙖𝙘𝙘𝙞𝙣𝙚 𝙛𝙤𝙧 {b['name']}")


    def get_successRate(self):              # helper function to keep track of vaccinated beneficiares
            return self.success_rate


    def filter_sessions(self,ar,ar2):       # helper function to sort beneficiares and vaccine slots by age

        slots_45 = list(filter(lambda x:x['age_limit']==45,ar))
        slots_18 = list(filter(lambda x:x['age_limit']==18,ar))
        beneficiaries_45 =list(filter(lambda x:x['age']>=45,ar2))
        beneficiaries_18 = list(filter(lambda x:x['age']>=18,ar2))
        return (slots_45,slots_18,beneficiaries_45,beneficiaries_18)


    def create_pdf(self,appointment_id,name):       # creates the appointment pdf

        try:
            url = f'https://cdn-api.co-vin.in/api/v2/appointment/appointmentslip/download?appointment_id={appointment_id}'
            with open(f'storage/downloads/{name}.pdf', 'wb') as f:
                f.write(self.session.get(url).content)
            print(f'[+] 𝓼𝓪𝓿𝓮𝓭 𝓫𝓸𝓸𝓴𝓲𝓷𝓰 𝓭𝓮𝓽𝓪𝓲𝓵𝓼 𝓹𝓭𝓯 𝓪𝓼 {name}.pdf')
        except :
            print('[-] failed to create booking pdf ')


    def final_listing(self):              # a final list is created using filters from the user for booking vaccines

        print('\n[*] 𝓒𝓻𝓮𝓪𝓽𝓲𝓷𝓰 𝓪 𝓯𝓲𝓷𝓪𝓵 𝓵𝓲𝓼𝓽!!')

        final_list = []

        if self.vaccine_type:      #filters vaccine slots by vaccine type
            if self.verbose:
                print('[*] 𝒻𝒾𝓁𝓉𝑒𝓇𝒾𝓃𝑔 𝓈𝓁𝑜𝓉𝓈 𝒷𝓎 𝓋𝒶𝒸𝒸𝒾𝓃𝑒 𝓅𝓇𝑒𝒻𝑒𝓇𝑒𝓃𝒸𝑒𝓈...')
            self.slots = list(filter(lambda x:x['vaccine'] in self.vaccine_type, self.slots))

        if self.preferences:        #filters vaccine slots by center id
            if self.verbose:
                print('[*] 𝒻𝒾𝓁𝓉𝑒𝓇𝒾𝓃𝑔 𝓈𝓁𝑜𝓉𝓈 𝒷𝓎 𝒸𝑒𝓃𝓉𝑒𝓇 𝒾𝒹...')
            self.slots = list(filter(lambda x:x['id'] in self.preferences, self.slots))

        if self.people:             #filters vaccine slots by beneficiary names
            self.beneficiaries =[ i  for i in self.beneficiaries if list(filter(lambda x:re.findall('^'+x.lower(),i['name'].lower()),self.people))]

        if self.booking_dates and  self.hybrid:     #filters vaccine slots by prefered dates
            if self.verbose:
                print('[*] 𝒻𝒾𝓁𝓉𝑒𝓇𝒾𝓃𝑔 𝓈𝓁𝑜𝓉𝓈 𝒷𝓎 𝒹𝒶𝓉𝑒 𝒶𝓋𝒶𝒾𝓁𝒶𝒷𝒾𝓁𝒾𝓉𝓎...')
            self.slots = list(filter(lambda x: int(x['date'][:2]) in self.booking_dates, self.slots))


        if self.slots:

            slots_45,slots_18,beneficiaries_45,beneficiaries_18 = self.filter_sessions(self.slots,self.beneficiaries)


            filterd_slots_45 =  list(filter(lambda x:x[f'dose{self.dose}'] >= len(beneficiaries_45), slots_45))
            filterd_slots_18 =  list(filter(lambda x:x[f'dose{self.dose}'] >= len(beneficiaries_18), slots_18))

            if filterd_slots_45:
                slots_45 = filterd_slots_45

            if filterd_slots_18:
                slots_18 = filterd_slots_18


            try:
                for s in slots_45:                                                          # tries to book vaccine for beneficiares(age >= 45) at the same center if possible
                    for i in range(s[f'dose{self.dose}']):
                        final_list.append((beneficiaries_45[i],s))
            except:
                pass
            try:
                for s in slots_18:                                                          # tries to book vaccine for beneficiares(age >= 18) at the same center if possible
                    for i in range(s[f'dose{self.dose}']):
                        final_list.append((beneficiaries_18[i],s))
            except:
                pass


        if self.verbose and final_list:
            print(f'{json.dumps(final_list, indent=4)}')

        if not final_list:
            print('[-] 𝕒𝕝𝕝 𝕓𝕖𝕟𝕖𝕗𝕚𝕔𝕚𝕒𝕣𝕚𝕤 𝕒𝕣𝕖 𝕧𝕒𝕔𝕔𝕚𝕟𝕒𝕥𝕖𝕕(𝕓𝕠𝕠𝕜𝕖𝕕) 𝕠𝕣 𝕟𝕠 𝕤𝕝𝕠𝕥𝕤 𝕒𝕧𝕒𝕚𝕝𝕒𝕓𝕝𝕖 𝕟𝕠𝕨..')
            return

        threads =[]
        for b,s in final_list:
            t =Thread(target=self.book_vaccine, args=(b,s))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()



def getDistrictId(state,district,lat,long):      # helper function to create a list of prefered vaccine centers near your place and feed it to the program
                                                                                # latitude and longitude of your place is needed
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    }

    try:
        print('[*] 𝑅𝑒𝓈𝑜𝓁𝓋𝒾𝓃𝑔 𝓈𝓉𝒶𝓉𝑒 𝒾𝒹...')
        url = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
        res = requests.get(url,headers=headers).json()['states']
        state_id = list(filter(lambda x :x['state_name'].lower() == state,res))[0]['state_id']

        print('[*] 𝑅𝑒𝓈𝑜𝓁𝓋𝒾𝓃𝑔 𝒹𝒾𝓈𝓉𝓇𝒾𝒸𝓉 𝒾𝒹...')
        url = f'https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}'
        res = requests.get(url,headers=headers).json()['districts']
        district_id = list(filter(lambda x :x['district_name'].lower() == district,res))[0]['district_id']       # gives the district id of a  state
        print(f'[+] district_id of {district} is {district_id} \n')

        print('[*] 𝒻𝑒𝓉𝒸𝒽𝒾𝓃𝑔 𝓋𝒶𝒸𝒸𝒾𝓃𝒶𝓉𝒾𝑜𝓃 𝒸𝑒𝓃𝓉𝑒𝓇𝓈 𝓃𝑒𝒶𝓇 𝓎𝑜𝓊...')
        url =f'https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong?lat={lat}1&long={long}'
        res = requests.get(url).json()['centers']
        res = list(filter(lambda x:x['district_name'].lower() == district, res))

        print('[+] 𝓋𝒶𝒸𝒸𝒾𝓃𝒶𝓉𝒾𝑜𝓃 𝒸𝑒𝓃𝓉𝑒𝓇𝓈 𝓃𝑒𝒶𝓇 𝓎𝑜𝓊 𝒶𝓇𝑒 ::\n')                                                              # shows a list of vaccination centers near 10 km radius from your place
        print(json.dumps(res,indent=4))
        if res:
            centers_list = [int(id) for id in input('enter preferred center id/s seperated by a space :: ').split(' ') ]
            return {'district_id':district_id, 'centers':centers_list}
        else:
            print('[-] latitude and longitude might be wrong!!')
            return {'district_id':district_id, 'centers':None}


    except :
        pass



def main():
    
    print("""
   

              ██████
            ▒██    ▒
            ░ ▓██▄
              ▒   ██▒
            ▒██████▒▒
            ▒ ▒▓▒ ▒ ░
            ░ ░▒  ░
            ░  ░  ░
                  ░
           """)
    
    
    
    parser = argparse.ArgumentParser()
    parser.usage = '''
        please read the README.MD

        '''
    parser.add_argument( '-m',  dest = 'mobile_no',     help= 'mobile number')
    parser.add_argument( '-o',  dest = 'otp_mode',      help= 'otp mode(a:automatic/m:manual)', default = 'a')
    parser.add_argument( '-d',  dest = 'dose',          help= 'dose num', default = 1)
    parser.add_argument( '-c',  dest = 'dist_id',       help= 'district id', default = 304)
    parser.add_argument( '-t',  dest = 'time',          help= 'time for appointment', type = int, default = 0)
    parser.add_argument( '--t', dest = 'test',          help= 'test run', action = 'store_true')
    parser.add_argument( '-v',  dest = 'verbose',       help= 'verbose output', action = 'store_true')
    parser.add_argument( '-p',  dest = 'preferences',   type= int,help = 'prefered centers(ID)', nargs = '*')
    parser.add_argument( '--v', dest = 'vaccine',       help= 'prefered vaccines', nargs = '*')
    parser.add_argument( '-b',  dest = 'people',        help= 'list of beneficiaries', nargs = '*')
    parser.add_argument( '--d', dest = 'booking_dates', help= 'list of vaccine booking dates', nargs = '*', type = int)
    parser.add_argument( '--l', dest = 'list',          help= 'get district id and vaccine centers near you', nargs = 4)
    parser.add_argument( '-f',  dest = 'file_data',     help= 'load previous data from file', action = 'store_true')
    parser.add_argument( '--p', dest = 'pincode',       help= 'pincode')

    args = parser.parse_args()

    if args.list:

        results = getDistrictId(args.list[0],args.list[1],args.list[2],args.list[3])

        if results:
            args.dist_id = results['district_id']
            args.preferences = results['centers']

    if args.file_data and not args.list:

        try:
            with open('inputData.txt','r') as f:         # feeds the program previous user data
                data = json.loads(f.read())

                args.mobile_no     = data.get('mobile')
                args.dose          = data.get('dose')
                args.dist_id       = data.get('dist_id')
                args.time          = data.get('time')
                args.preferences   = data.get('preferences')
                args.vaccine       = data.get('vaccines')
                args.people        = data.get('people')
                args.booking_dates = data.get('booking_dates')
                args.pincode       = data.get('pincode')
        except:
            print('[-] file couldnt be processesd!!')
            exit(0)

    cli_data ={
        "mobile"        : args.mobile_no,
        "dose"          : args.dose ,
        "dist_id"       : args.dist_id,
        "time"          : args.time,
        "preferences"   : args.preferences,
        "vaccines"      : args.vaccine,
        "people"        : args.people,
        "booking_dates" : args.booking_dates,
        "pincode"       : args.pincode,
        }

    print('filters choosen are:\n')
    print(json.dumps(cli_data,indent=4))
    input('press any key to continue..')
    subprocess.call(['clear'])

    with open('inputData.txt','w') as f:
        print('[+] saving your current input data to file inputData.txt. \n you can use the -f flag to load this data next time as arguments..\n')
        f.write(json.dumps(cli_data,indent=4))


    if not args.mobile_no:
        print(parser.usage)
        exit(0)

    if args.test:                      # test function which will book  vaccine for a random user at random place (for testing only..)
        print('testing mode on..[the first person in the list above age 45 will be booked a vaccine at a random place...]')
        input('press ctrl+c if you wanna exit::')

    c = cowin(args.mobile_no, args.dose, args.dist_id, args.otp_mode,
              args.test, args.verbose, args.vaccine, args.preferences, args.time,args.people,args.booking_dates,args.pincode)


    # delay = [14,18,20,25,30,35,15]   random delays

    sucess = 1

    while sucess:

        if c.get_details():
            c.final_listing()
            sucess = c.get_successRate()

        # sleep_time =random.choice(delay)
        if not c.start:
            print('\n[*] 𝔖𝔠𝔯𝔦𝔭𝔱 𝔴𝔦𝔩𝔩 𝔞𝔲𝔱𝔬𝔪𝔞𝔱𝔦𝔠𝔞𝔩𝔩𝔶 𝔯𝔢𝔰𝔱𝔞𝔯𝔱 𝔞𝔣𝔱𝔢𝔯 շօ 𝔰𝔢𝔠𝔬𝔫𝔡𝔰..')
            time.sleep(20)




if __name__ == '__main__':

    main()
    try:
        main()
    except Exception as e:
        print(f'\nexiting program ... with error message =>{e}')
