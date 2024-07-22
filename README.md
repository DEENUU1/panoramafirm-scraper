[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<br />
<div align="center">
  <h3 align="center">Panoramafirm Scraper</h3>
  <strong align="center">
    Scrape all companies from <a href="https://panoramafirm.pl/">panoramafirm.pl</a>
    <br />
    <br />
    <a href="https://github.com/DEENUU1/panoramafirm-scraper/issues">Report Bug</a>
    ·
    <a href="https://github.com/DEENUU1/panoramafirm-scraper/issues">Request Feature</a>
  </strong>
</div>


## About the project
This project is a CLI application build with Python which allows to scrape all companies from <a href="https://panoramafirm.pl/">panoramafirm.pl</a> website.
For each company you can get data like:
- industry
- category
- company name
- phone number
- email address
- company website
- image url
- rate value
- number of rates
- street name
- postal code
- region name
- city name
- NIP
- description

## Technologies:
- Python
  - click
  - aiosqlite
  - httpx
  - requests
  - beautifulsoup4
  - asyncio
- SQLite

## Installation

```bash
git clone https://github.com/DEENUU1/panoramafirm-scraper.git
```

```bash
python -m venv .venv
```

```bash
.\.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
python main.py --process companies  # scrape list of companies from all categories
python main.py --process details  # scrape details for each company from database
```
## Authors

- [@DEENUU1](https://www.github.com/DEENUU1)

<!-- LICENSE -->

## License

See `LICENSE.txt` for more information.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/DEENUU1/panoramafirm-scraper.svg?style=for-the-badge

[contributors-url]: https://github.com/DEENUU1/panoramafirm-scraper/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/DEENUU1/panoramafirm-scraper.svg?style=for-the-badge

[forks-url]: https://github.com/DEENUU1/panoramafirm-scraper/network/members

[stars-shield]: https://img.shields.io/github/stars/DEENUU1/panoramafirm-scraper.svg?style=for-the-badge

[stars-url]: https://github.com/DEENUU1/panoramafirm-scraper/stargazers

[issues-shield]: https://img.shields.io/github/issues/DEENUU1/panoramafirm-scraper.svg?style=for-the-badge

[issues-url]: https://github.com/DEENUU1/panoramafirm-scraper/issues

[license-shield]: https://img.shields.io/github/license/DEENUU1/panoramafirm-scraper.svg?style=for-the-badge

[license-url]: https://github.com/DEENUU1/panoramafirm-scraper/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin-url]: https://linkedin.com/in/kacper-wlodarczyk

[basic]: https://github.com/DEENUU1/panoramafirm-scraper/blob/main/assets/v1_2/basic.gif?raw=true

[full]: https://github.com/DEENUU1/panoramafirm-scraper/blob/main/assets/v1_2/full.gif?raw=true

[search]: https://github.com/DEENUU1/panoramafirm-scraper/blob/main/assets/v1_2/search.gif?raw=true
