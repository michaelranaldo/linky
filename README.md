<p align="center">
  <img alt="Linky" src="https://i.imgur.com/ozdWSxP.jpg" height="140" />
  <p align="center">
    <a href="https://github.com/mez0cc/linky/releases/latest"><img alt="Release" src="https://img.shields.io/github/release/mez0cc/linky.svg?style=flat-square"></a>
    <a href="https://github.com/mez0cc/linky/blob/master/LICENSE"><img alt="Software License" src="https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square"></a>
    <a href="https://github.com/mez0cc/linky/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/mez0cc/linky.svg?style=flat-square"></a>
    </p>
</p>

<h5 align="center"><i>Yet another LinkedIn Scraper...</i></h5>

Linky is a *another* LinkedIn scraper. Inspired by [vysecurity](https://twitter.com/vysecurity) and his [LinkedInt](https://github.com/vysecurity/LinkedInt) project.

Currently, this method of extracting data from LinkedIn is limited to 1000 users at a time. So, Linky's HTML output has a small table at the bottom of the page which calculates the top 5 most common occupations that occur. This way, if the company has a weird naming scheme for devs, then Linky should be able to spot it and report it back. With these new found data points, the `--keywords` flag can be used to attempt to filter the output.

I will open to issues for the new features I'm working on implementing:

1. [Bypassing the 1000 limit](https://github.com/mez0cc/linky/issues/1)

2. [Additional mode to read and extract technical details from users LinkedIn bios](https://github.com/mez0cc/linky/issues/2)

***

Installing
==========

```pip3 -r install requirements.txt```


Help Page
========

```

 ▄█        ▄█  ███▄▄▄▄      ▄█   ▄█▄ ▄██   ▄   
███       ███  ███▀▀▀██▄   ███ ▄███▀ ███   ██▄ 
███       ███▌ ███   ███   ███▐██▀   ███▄▄▄███ 
███       ███▌ ███   ███  ▄█████▀    ▀▀▀▀▀▀███ 
███       ███▌ ███   ███ ▀▀█████▄    ▄██   ███ 
███       ███  ███   ███   ███▐██▄   ███   ███ 
███▌    ▄ ███  ███   ███   ███ ▀███▄ ███   ███  @mez0cc
█████▄▄██ █▀    ▀█   █▀    ███   ▀█▀  ▀█████▀   0.1
▀                          ▀                   
	<<<Yet another LinkedIn scraper>>>

usage: linky.py [-h] -c  [-i] [-k] [-d] [-o] [-f]

Yet another LinkedIn scraper.

optional arguments:
  -h, --help          show this help message and exit
  -c , --cookie       Cookie to authenticate to LinkedIn with [li_at]
  -i , --company-id   Company ID number
  -k , --keyword      Keyword for searches
  -d , --domain       Company domain name
  -o , --output       File to output to: Writes CSV, JSON and HTML.
  -f , --format       Format for email addresses

```

Usage
=====

#### Get Employees

```python3 --cookie cookie.txt --company-id 1441 --domain google.com --output google_employees  --format 'firstname.surname'```

#### Get Employees with keyword

```python3 --cookie cookie.txt --company-id 1441 --domain google.com --output google_employees  --format 'firstname.surname' --keyword developer```

Supported email formats
========================

Currently, there is  no support for middle names but its on the to-do list. Here are the current naming schemes:

```
firstname.surname
f.surname
firstnamesurname
fsurname
surname.firstname
s.firstname
surnamefirstname
sfirstname
```
They can all be referenced in ```--format```, E.G:

***f.surname***: ```--format f.surname```