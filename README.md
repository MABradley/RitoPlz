# SUMMARY

## There are Two Primary Purposes to This Project
* To Explore Python and QT Functionality and Grow as a Developer
* To Analyze Personal League of Legends Game Data

Python Version: 3.4.3+
 *Feel free to execute using later versions of Python, but it must execute in 3.4.3*

# STATUS

## 06/04/16
* Optional Columns With Toggle

## 06/02/16
* Frequent Item and Champion Choices
* Restructured Resources by Version for Latest Data and Lazy Load
* Static Champion Data
* Updated to Python 3.5.1 and PyQt 5.5.6

## 05/30/16
* Tracked Summoners Window
* Profile Icon Fetching
* Summoner Requests in Separate Thread

## 05/28/2016
* Basic Classes and Methods for Data Access

## 05/25/2016
* Proof of Concept Methods

# SETUP
## Windows Set Up Instructions
1. Install [Python 3.4.3](https://www.python.org/downloads/release/python-343/)
2. Install the IDE of your choice
   * I recommend [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows)
3. Clone the repository
   * GitHub has [Setup Help](https://help.github.com/articles/set-up-git/)
   * PyCharm has [Git Integration](https://www.jetbrains.com/help/pycharm/2016.1/using-git-integration.html)
4. Install [PyQt5](https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.4.1/)
   * This one is a bit tricky, I found it easiest to use the installer provided above.
5. Install the [Requests Library](http://docs.python-requests.org/en/master/)
   * In the command prompt navigate to *C:/Python34/Scripts* (By default)
   * Execute:  **pip install requests**

## Linux Set Up Instructions
Coming Soon!

We are currently reviewing the universal packaging [Flatpak](http://flatpak.org/) and [Snap](https://developer.ubuntu.com/en/snappy/build-apps/).

## Getting Started
Input a [Riot Games Developer Key](https://developer.riotgames.com)
   * If you have a [League of Legends](http://na.leagueoflegends.com/) account, use those credentials to retrieve a key
   * If not, contact someone who does. (I would be happy to send you mine for development purposes)
   * Run "Main.py" under */reposoitoryDirectory/project* and input the key when prompted

# CONVENTIONS
* Property names and local variables should be camel case
* Class and method names should be pascal case
* SQL keywords should be uppercase
* Commented code should be correctly indented after un-commenting

# COPYRIGHT
[License](https://github.com/MABradley/RitoPlz/blob/master/LICENSE.txt)
