import os
import csv
import datetime
import requests
from environs import Env
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

env = Env()
env.read_env() 

DM_BIRTHDAY_FILE = env('DM_BIRTHDAY_FILE')
DM_GITHUB_EDIT = env('DM_GITHUB_EDIT')
DM_SENDGRID_TOKEN = env('DM_SENDGRID_TOKEN') 
DM_FROM_EMAIL = env("DM_FROM_EMAIL")
DM_TO_EMAILS  = env.list("DM_TO_EMAILS")
DM_XDAYS = env.int('DM_XDAYS')

def load_csvfile(filename):
    bd = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bd.append(row)
    return bd

def parse_dates(bd):
    for i, val in enumerate(bd):
        datee = datetime.datetime.strptime(val['birthday'], "%Y-%m-%d")
        bd[i]['day'] = datee.day
        bd[i]['month'] = datee.month
        bd[i]['year'] = datee.year
    return bd
        
def get_birthday_html():
    html = ''
    tmp = load_csvfile(DM_BIRTHDAY_FILE)
    bd_list = parse_dates(tmp)
    today = datetime.datetime.today()
    x_list = [today + datetime.timedelta(days=x) for x in range(DM_XDAYS)]
    for x in x_list:
        html += f'<h4>{x.strftime("%A %#d %b %Y")}</h4>'
        for bd in bd_list:
            if ((bd["age"].lower() == 'once' and 
                 bd["year"] == x.year and
                 bd["month"] == x.month and
                 bd["day"] == x.day) or
                (bd["age"].lower() != 'once' and
                 bd['month'] == x.month and 
                 bd['day'] == x.day)):
                try:
                    age_now = f'({x.year - bd["year"] + int(bd["age"])})'
                except:
                    age_now = ''
                html += f'<li>{bd["name"]} {age_now} - {bd["note"]}</li>'              
    html += f'<br><a href="{DM_GITHUB_EDIT}">Edit</a><br>'
    return html

def main():
    html_content = \
        get_birthday_html()
    
    now = datetime.datetime.now() 
    now_datetime = now.strftime("%A %#d %b %Y, %H:%M:%S GMT")
    message = Mail(
        from_email = DM_FROM_EMAIL,
        to_emails = DM_TO_EMAILS,
        subject = f'DAILY: {now_datetime}',
        html_content = html_content
    )    
    try:
        print('=====send_email====')
        sg = SendGridAPIClient(DM_SENDGRID_TOKEN)
        r = sg.send(message)
        print(r.status_code)
        print(r.body)
        print(r.headers)
    except Exception as e:
        print(e.message)
        
main()
