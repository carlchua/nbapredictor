<br />
<p align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/bball.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">NBA Predictor & Webscraper</h3>

  <p align="center">
    YOUR_SHORT_DESCRIPTION
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Based on Michael Mauboussin's book, The Success Equation, compared to Football (American and actual), Hockey, and Baseball, Basketball is the most 'skill-based'
sport. Outcomes and victories in Basketball are more representative of the difference between the skills and talents of the winners and the losers. This project
seeks to accurately predict NBA championships using Neural Net(s). It also includes a webscraper .py file, which can be used to change the training & test datasets.

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

The following Python libraries must be installed:
* Pandas
* BeautifulSoup

### Installation

1. Clone the repo
```sh
git clone https://github.com/carlchua/nbapredictor.git
```
2. Install NPM packages
```sh
npm install
```



<!-- USAGE EXAMPLES -->
## Usage

```sh
py webscraper.py rsg 2016 2019
```
The above code will return regular season game data from 2016 to 2019. Currently only the final score is returned. Panda DataFrames are created, but they still need to be converted to .csv files.

```sh
py webscraper.py szn 2018
```

The above code will return player data for the 2018 season.

<!-- CONTACT -->
## Contact

Carl Chua - carlchua@berkeley.edu

Project Link: [https://github.com/carlchua/nbapredictor](https://github.com/carlchua/nbapredictor)





