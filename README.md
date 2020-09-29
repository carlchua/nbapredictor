<br />
<p align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/bball.png" alt="Logo" width="750" height="333">
  </a>

  <h3 align="center">NBA Predictor & Webscraper</h3>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

According to _The Success Equation_ (Michael Mauboussin), compared to Football (American and actual), Hockey, and Baseball, Basketball is the most 'skill-based' sport.

Outcomes and victories in Basketball are more representative of the difference between the skills and talents of the winners and the losers. This project
seeks to accurately predict NBA championships using Neural Net(s). It also includes a webscraper .py file, which can be used to change the training & test datasets. Currently, there is no functionality for 
players whose names have special characters not contained in ASCII.


***TODO:***
* Implement Neural Network


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

The following Python libraries must be installed:
* Pandas
* BeautifulSoup
* Selenium

Aside from these libraries, ChromeDriver (WebDriver for Chrome) must be installed. The executable (chromedriver.exe) should be placed in the nbapredictor file directory.

Clone the repo
```sh
git clone https://github.com/carlchua/nbapredictor.git
```



<!-- USAGE EXAMPLES -->
## Usage
#### Webscraper

```sh
py webscraper.py rsg 2016 2019
```
The above code will return regular season game data from 2016 to 2019. winner.txt records the N, T1, T2, where N is the winning team (1 or 2 - this is redundant), and T1 and T2 are the scores for teams 1 and 2. 

```sh
py webscraper.py szn 2018
```
The above code will return player data for the 2018 season.

```sh
py webscraper.py train 2015 2019
```
The above code returns the necessary data to train the neural network model. This encompasses monthly advanced team stats from the 2015-2019 regular seasons. The data is also cleaned and organized properly for the neural network.
This command was used to generate the data currently in training_data.


<!-- CONTACT -->
## Contact

Carl Chua - carlchua@berkeley.edu

Project Link: [https://github.com/carlchua/nbapredictor](https://github.com/carlchua/nbapredictor)





