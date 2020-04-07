# JJCrawler
>
## A web crawlers collection used to scrap job offers from top websites. Each of them returns data in a json format. 
They are implemented with usage of scrapy and selenium libraries. 
>
Implemented scrapers for:
* [JustJoinIT](https://justjoin.it/) - crawler name: jjcrawler
* [No Fluff Jobs](https://nofluffjobs.com/jobs/) - crawler name: nfjcrawler
>
### How to run:
>
Change your working directory to project directory, and run:
```python
pip install requirements.txt
```
To call specific crawler, in your terminal type:
```python
scrapy crawl CRAWLER_NAME
```
If you want to save crawler output to file, run:
```python
scrapy crawl CRAWLER_NAME -o FILE_NAME
```
