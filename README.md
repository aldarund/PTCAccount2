# Pokemon Trainer Club Account Creator 2
Script heavily based on the original [PTCAccount](https://github.com/jepayne1138/PTCAccount), by [jepayne1138](https://github.com/jepayne1138).

Modified from [Kitryn](https://github.com/Kitryn/PTCAccount2).
## Description
Semi-automatic creation of PTC accounts, with manual user intervention required for CAPTCHA input. This script is built on Selenium, which utilises a browser for automation rather than pure HTTP requests.

It also runs off the ability to add a '+' in an email to create alternate emails. EX: test+123@gmail.com

If you're using Gmail and want to automatically verify all accounts, use this gist: [Here](https://gist.github.com/sebastienvercammen/e7e0e9e57db246d7f941b789d8508186 or https://github.com/FrostTheFox/ptc-acc-gen/blob/master/gmailverify.js)
I also added it to the files for convince

## Installation

This script runs on Selenium using ChromeDriver. See the [Google documentation](https://sites.google.com/a/chromium.org/chromedriver/downloads) for platform specific installation.

OSX Installation: `brew install chromedriver`

Once ChromeDriver is installed, install PTCAccount2 from Github using pip (Run in either `Git Bash`, `CMD` on Winodws, or `Terminal` on Linux/MacOS):

`pip install git+https://github.com/Chris221/PTCAccount2.git`

## Installation

To upgrade run in either `Git Bash`, `CMD` on Winodws, or `Terminal` on Linux/MacOS:

`pip install git+https://github.com/Chris221/PTCAccount2.git --upgrade`

## Use

### Command line interface:

After installing the package run 'ptc2' from the terminal to create a new account. Optional parameters include --username, --password, and --email. Use --help for more commands and command line interface help.

Example 1 (Create entirely random new account):

```
> ptc2
Account successfully created.
  Username:  BcZvTnlTMwHsa6v
  Password:  WgZApVU5edTBMCs
  Email   :  test@gmail.com
```

Example 2 (Create a new account with specified parameters):

```
> ptc2 --username=foo --password=bar --email=test@gmail.com
Account successfully created.
  Username:  foo
  Password:  bar
  Email   :  test+foo@gmail.com
```

Extra options:

* `--birthday`: Specify a birthday. Must be between 1910 and 2002. Must be in YYYY-MM-DD format.
* `--compact`: Compact the output to "username:password"


**As package:**

import the _ptcaccount2_ package to create new accounts in your own scripts:

```python
>>> import ptcaccount2
>>> ptcaccount2.random_account()
{"username": "BcZvTnlTMwHsa6v", "password": "WgZApVU5edTBMCs", "email": "test@gmail.com"}
```

**Specifying your own data:**
```python
>>> ptcaccount2.random_account(username=<your data>, password=<your data>, email=<your data>, birthday=<your data>)
```

Note: `birthday` must be a string in YYYY-MM-DD format.

## Troubleshooting

### OSX installation

Some OSX users may run into an issue which points to an error occurring in line: `create_account driver = webdriver.Chrome()` This may be related to `brew install chromedriver` installing a 32bit version rather than 64bit version.

To fix, see [this issue](https://github.com/Kitryn/PTCAccount2/issues/1) to make brew install the 64bit version of ChromeDriver.
