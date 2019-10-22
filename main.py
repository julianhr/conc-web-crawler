import logging
from app.welcome import Welcome
from app.loggers import Loggers


def main():
    loggers = Loggers()
    loggers.setup(logging.INFO)

    welcome = Welcome(debug=True)
    welcome.interactive()

    scraper = welcome.scraper
    scraper.run()


if __name__ == "__main__":
    main()
