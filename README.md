# Nodepay Automate with Proxies
### Tools and components required
1. Nodepay Account| Register: [https://app.nodepay.ai/register](https://app.nodepay.ai/register?ref=ReFitLH5Hn9dxzJ)
2. Proxies Static Residental | [FREE 10 PREMIUM PROXIES](https://www.webshare.io/?referral_code=p7k7whpdu2jg)
3. VPS (OPTIONAL) and Python3
# Installation
- Open [Nodepay](https://app.nodepay.ai/register?ref=ReFitLH5Hn9dxzJ) and login to dashboard
- Press F12 or CTRL + SHIFT + I
- Select Console
- At the console, type ```allow pasting``` and press enter
![0001](https://github.com/im-hanzou/getgrass_bot/blob/main/pasting.JPG)
- Then type ``localStorage.getItem('np_token')`` and press enter
![0002](https://github.com/im-hanzou/getgrass_bot/blob/main/nodepaytoken.png)
- The text that appears is your nodepay token and copy the text
### Component installation
- Install Python For Windows: [Python](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)
- For Unix:
```bash
apt install python3 python3-pip -y
```
- Install requirements: 
```bash
python3 -m pip install -r requirements.txt
```
### Run the Bot
- Run:
```bash
python3 run.py
```
- Press Enter then insert your nodepay token
# Operating status
If the following log appears, it means it is running successfully.
```bash
2024-07-30 04:37:18.263 | INFO     | __main__:ping:110 - Ping successful: {'success': True, 'code': 0, 'msg': 'Success', 'data': {'ip_score': 88}}
2024-07-30 04:37:48.621 | INFO     | __main__:ping:110 - Ping successful: {'success': True, 'code': 0, 'msg': 'Success', 'data': {'ip_score': 90}}
2024-07-30 04:38:18.968 | INFO     | __main__:ping:110 - Ping successful: {'success': True, 'code': 0, 'msg': 'Success', 'data': {'ip_score': 94}}
2024-07-30 04:38:59.338 | INFO     | __main__:ping:110 - Ping successful: {'success': True, 'code': 0, 'msg': 'Success', 'data': {'ip_score': 98}}
```
