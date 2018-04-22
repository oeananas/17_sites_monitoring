# Sites Monitoring Utility

Script for monitoring the health of sites.
As an argument when starting the script, you need to transfer a text file, in which URLs are written for verification.
The script checks the site according to two criteria: the server's response status and the domain's validity period.
If the server response code does not contain an error and the domain's validity period is more than a month at the time of verification, the script displays the check status: OK !, if there are problems, then check status: FAILED!

# How to install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```
Remember, it is recommended to use virtualenv/venv for better isolation.

# QuickStart

Example of script launch on Linux, Python 3.5
```bash
python3 check_sites_health.py urls.txt
for domain *stepik.org*  :  check status: OK!
for domain *www.coursera.org*  :  check status: OK!
for domain *geekbrains.ru*  :  check status: OK!
for domain *htmlacademy.ru*  :  check status: OK!
for domain *devman.org*  :  check status: OK!
for domain *ru.wikipedia.org*  :  check status: OK!
for domain *github.com*  :  check status: OK!
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
