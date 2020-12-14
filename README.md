[![MIT License][license-badge]][license]

## ~~ PLEAEE DON'T USE THIS. NOT BEING MAINTAINED ANYMORE, IN FAVOR OF THIS REPO: https://github.com/verdan/flaskoidc ~~

# Flask Keycloak
Minimal Flask-Keycloak application, built using the modular approach. 

## Features:
- Modular architecture
- Authentication using keycloak
- Separate production and development configurations and clients' secrets files

Getting Started
---------------

I'm assuming you have Python installed. It is preferable to have a virtual environment for the project libraries.
Also assuming you've git setup on your system.

Setting Up the Keycloak Server
------------------------------
Refer to the following documentation to create the Keycloak client. [OIDC Clients](https://www.keycloak.org/docs/3.0/server_admin/topics/clients/client-oidc.html)
By default this template uses the following values:

- Realm Name: flask-demo
- Client Name: flask-client
- Client Secret: '0a55e3fd-5c30-44ec-b623-26b69ff23f45' (this is auto-generated, please change it in `config/client_secrets_[dev/prod].json` accordingly)

Please make sure to update the configurations if you are not using the above mentioned values (and for production)

`1: config/client_secrets_dev.json or/and config/client_secrets_prod.json`

`2: config/configurations.py`


Setting Up the Virtual Environment
----------------------------------

If you're using pip to install packages (and I can't see why you wouldn't), you can get both virtualenv and virtualenvwrapper by simply installing the latter.

            pip install virtualenvwrapper

After it's installed, add the following lines to your shell's start-up file (.zshrc, .bashrc, .profile, etc).

            export WORKON_HOME=$HOME/.virtualenvs
            export PROJECT_HOME=$HOME/directory-you-do-development-in
            source /usr/local/bin/virtualenvwrapper.sh

Reload your start up file (e.g. source .bashrc) and you're ready to go.

Creating a virtual environment is simple. Just type

            mkvirtualenv flask-keycloak

or If already created the Virtual Environment, just start the environment by typing

            workon flask-keycloak
            

Getting the App Running
-----------------------

Installing Python Packages and getting the app running is just like eating chocolate.

            cd /path/where/you/want/your/project
            git clone git@github.com:verdan/flask-keycloak.git
            cd flask-keycloak/
            
Packages can be installed using pip command.
This command installs the packages in the requirement file.
            
            pip install -r requirements.txt
            
Start the Server
            
            flask run


API URLs
-----------------------
            
            http://localhost:5000/portal/api/docs
            http://localhost:5000/portal/api/spec


[license-badge]: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
[license]: https://github.com/verdan/service-catalog/blob/master/LICENSE
