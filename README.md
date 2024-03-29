[![Telegram Product Hunt Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/ProductHuntTelegramBot)
[![GitHub Actions](https://github.com/Crazy-Marvin/ProductHuntTelegramBot/actions/workflows/ci.yml/badge.svg)](https://github.com/Crazy-Marvin/ProductHuntTelegramBot/actions/workflows/ci.yml)
![healthchecks.io](https://img.shields.io/endpoint?url=https%3A%2F%2Fhealthchecks.io%2Fbadge%2F396c7d03-faf7-4562-9f83-1194d0%2Fn-TwoPva%2FProductHunt.shields)
[![License](https://img.shields.io/github/license/Crazy-Marvin/ProductHuntTelegramBot)](https://github.com/Crazy-Marvin/ProductHuntTelegramBot/blob/trunk/LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/Crazy-Marvin/ProductHuntTelegramBot.svg?style=flat)](https://github.com/Crazy-Marvin/ProductHuntTelegramBot/commits)
[![Releases](https://img.shields.io/github/downloads/Crazy-Marvin/ProductHuntTelegramBot/total.svg?style=flat)](https://github.com/Crazy-Marvin/ProductHuntTelegramBot/releases)
[![Latest tag](https://img.shields.io/github/tag/Crazy-Marvin/ProductHuntTelegramBot.svg?style=flat)](https://github.com/Crazy-Marvin/ProductHuntTelegramBot/tags)
[![Issues](https://img.shields.io/github/issues/Crazy-Marvin/ProductHuntTelegramBot.svg?style=flat)](https://github.com/Crazy-Marvin/ProductHuntTelegramBot/issues)
[![Pull requests](https://img.shields.io/github/issues-pr/Crazy-Marvin/ProductHuntTelegramBot.svg?style=flat)](https://github.com/Crazy-Marvin/ProductHuntTelegramBot/pulls)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/d6eb9ee5488548dca0536ecd93e16ae0)](https://www.codacy.com/gh/Crazy-Marvin/ProductHuntTelegramBot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Crazy-Marvin/ProductHuntTelegramBot&amp;utm_campaign=Badge_Grade)
[![Dependabot](https://badgen.net/badge/icon/dependabot?icon=dependabot&label)](https://python.org/)
[![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/Crazy-Marvin/ProductHuntTelegramBot)](https://app.snyk.io/org/crazymarvin/project/e58b3418-2609-4731-b629-6812069fdb73)
[![Telegram Product Hunt Bot](https://img.shields.io/badge/Python-yellow?logo=python)](https://t.me/ProductHuntTelegramBot)

# Product Hunt Telegram Bot

This [bot](http://t.me/ProductHuntTelegramBot) shows you today's posts from [Product Hunt](https://www.producthunt.com/). 

![Product Hunt Telegram Bot Preview](https://user-images.githubusercontent.com/15004217/188268836-ef691e4b-e8bc-4410-8bb6-a5e72ba90388.PNG)

#### Commands

start - This starts the bot 🚀   
daily - This sends all products of the day 🗣  
monthly - This sends all products of the month 🗣  
schedule - This lets you choose a schedule for automatic updates 🕰   
help - This sends you a help text 🆘   
contact - This allows contact ✍️   
feedback - This lets you give feedback 👺    

### Requirements

- Token from [@Botfather](https://telegram.me/botfather)
- SSL certificate (I recommend [Let's Encrypt](https://letsencrypt.org/))
- Webserver running [Python](https://www.python.org) (tested with [Apache](https://httpd.apache.org/) & [NGINX](https://www.nginx.com/) but others should work too)
- API key from Product Hunt
- Google Cloud service account credentials (JSON) for accessing Google Sheets API & Google Drive API
- [Sentry](https://docs.sentry.io/platforms/python/) key (optional)
- [Healthchecks](https://healthchecks.io/#php) URL (optional)

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.
More details may be found in the [CONTRIUBTING.md](https://github.com/Crazy-Marvin/ProductHuntTelegramBot/tree/trunk/.github/CONTRIBUTING.md).

### License

[MIT](https://choosealicense.com/licenses/mit/)
