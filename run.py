#!venv/bin/python

from creamcrape import cli

if __name__ == '__main__':
    cli.runserver(host='0.0.0.0',
                  port=5050,
                  threaded=False,
                  processes=1,
                  passthrough_errors=True,
                  debug=True,
                  reload=True
        )
