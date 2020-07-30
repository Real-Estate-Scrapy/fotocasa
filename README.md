# Fotocasa

## Description
Scraping property details from https:/fotocasa.es/ and store it in Postgresql database.

### Implementations
1. Webscraping property details from fotocasa website
2. Rotating proxy to bypass antibot mechanism of the websource
3. Scrapy-Splash implementation for javascript content such as infinite scrolling.
4. Model/Pipeline design and development for PostgresQL database.


## Setup Environment Variables
In `settings.py` add the following configuration:
1. Database connection
    ```
    DATABASE = {
        'drivername': 'postgres',
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
        'username': os.environ.get('DB_USERNAME', 'user'),
        'password': os.environ.get('DB_PASSWORD', 'pwd'),
        'database': os.environ.get('DB_NAME', 'mydb')
    }
    ```
2. Database pipeline
    ```
    ITEM_PIPELINES = {
        'fotocasa.pipelines.PostgresDBPipeline': 330,
        

        'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    }
    ```

3. Proxies path
ROTATING_PROXY_LIST_PATH = 'fotocasa/proxies.txt'


## Dependencies
1. Install the following dependencies from requirements.txt
    `pip install -r requirements.txt`
    
    ```buildoutcfg
    sqlalchemy
    psycopg2
    scrapy-rotating-proxies
    ```

## Create eggfile
1. Create `setup.py` file at the same level as `scrapy.cfg` file with content as:
    ```
    from setuptools import setup, find_packages
    setup(
        name='fotocasa',
        version='1.0',
        packages=find_packages(),
        install_requires=[
            'psycopg2',
            'sqlalchemy'
            'scrapy-rotating-proxies'
        ],
        entry_points={'scrapy': ['settings = fotocasa.settings']}
    )
    ```
    
2. Execute `python setup.py bdist_egg` in folder at the same level as `scrapy.cfg` file
3. Upload the eggfile into the scrapyd server using: `curl http://localhost:6800/addversion.json -F project=fotocasa -F version=1.0 -F egg=@dist/fotocasa-1.0-py3.7.egg`
