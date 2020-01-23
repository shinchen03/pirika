#!/usr/bin/env python3

from app import create_app

config_name = 'development'
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
