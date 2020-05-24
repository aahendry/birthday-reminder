# Send yourself a daily birthday reminder email with Python and Github Actions

After forgetting yet another birthday, I decided to set up a simple daily email reminder system.  It consists of a Python program that is scheduled to run daily using GitHub Actions. All the birthdays and other anniversaries are maintained in a `csv` file and the daily email is send using Sendgrid API.  Due to the low volumes, all the services used - are on FREE plans.

Since setting it up, I have included some forex and stock price information into the daily mail.  The code is included in this program but can be commented out if not used as shown further below.

## Tools and API's used

- Birthday list and Python program is on GitHub
- Github Actions trigger the daily email
- [SendGrid](https://sendgrid.com/) API to send emails

Optional
- [IEX Cloud](https://iexcloud.io/) API for get stock prices
- [Finnhub](https://finnhub.io/) API for get forex rates

## Local install

1. Clone this GitHub Repository
2. If you don't want to include stock prices and forex info, comment out `get_forex_html()` and `get_stock_html()` in `main()` 
   - If you want to include forex info, get an API key from [Finnhub](https://finnhub.io/). It is free for basic quotes
   - For stock quotes, get a key from [IEX Cloud](https://iexcloud.io/). It is free for low volume, basic info

```python
def main():
    html_content = \
#       get_forex_html() + \
#       get_stock_html() + \
        get_birthday_html()
```
3. Install Python dependancies with `pip install environs requests sendgrid`. 
4. Get a [SendGrid](https://sendgrid.com/) API key.  It is free if you sent a low volume of emails per day
5. Update the key info in the `.env` file
6. Run with `python daily_email.py`


## GitHub Actions

1. Ensure GitHub Actions is Enabled within Settings of your repository
2. Change the scheduled time in file `.github/workflows/pythonapp.yml`. Use [crontab guru](https://crontab.guru/) as guide if you are not to speed with cron settings
3. To track status or re-run an Action, see details under the `Actions` 

![GitHub Actions](/images/github-actions-list.png)

Runtime is under 1 minute. On the GitHub free plan, you have 2,000 Actions minutes/month available.  So no problem there.


![workflow](/images/github-actions-workflow.png)


## Birthdays

**Maintaining the birthday file**

I used csv format rather than yaml, json or other format. This is so that I can maintain the list easily on my local machine using Excel.  It also displays [nicely](https://github.com/whoek/birthday-reminder/blob/master/birthdays.csv) on GitHub.

Sample file
```csv
birthday,age,name,note
2020-06-21,once,Father's Day,Ireland
2021-06-20,once,Father's Day,Ireland
2022-06-19,once,Father's Day,Ireland
2020-05-26,45,Adrian Bruce,birthday
1964-05-27,0,Alexander MacDonald,birthday
```

- `birthday` - Must be in `yyyy-mm-dd` format 
- `age` - You can enter the age of the person on the spesified date/ This is 0 if date of birth was entered. This is used to show the calculated age of the person in the email.  If age of person is known, leave it blank. In this case, the year field of birthday is ignored.   For once-off reminders, add the word `once` in the `ae` field. The reminder will only be shown on exact date indicated. 

**Daily email**

![workflow](/images/daily-email.png)

