msgraph-utility-cli
#############################


.. image:: https://travis-ci.org/hpnguyen123/msgraph-utility-cli.svg?branch=master
   :target: https://travis-ci.org/hpnguyen123/msgraph-utility-cli

Requirements
-------
1. Python3
2. Pip
3. VirtualEnv
4. Microsoft Business Account

Application Setup
-------
This console application is built upon [python-sample-console-app](https://github.com/microsoftgraph/python-sample-console-app).
Register a new native as instructed by this sample application.


Build
-------
1. Git Clone https://github.com/hpnguyen123/msgraph-utility-cli.git
2. cd msgraph-utility-cli
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. pip install -e .

Run
-------
li-msgraph-utility authenticate --client-id [YOUR_CLIENT_ID]

Commands
-------
1. authenticate - Invoke authentication workflow
2. get-content - Get content of a file from OneDrive
3. put-content - Put content of a file to OneDrive
4. show - Show the configuration property

License
-------

This code is licensed under the `MIT License`_.

.. _`MIT License`: https://github.com/hpnguyen123/msgraph-utility-cli/blob/master/LICENSE
