from flask import Blueprint, request, redirect, url_for

from app import oidc

from flask import current_app


view = Blueprint('view', __name__)

import datetime

@view.route('/')
def index():
    if oidc.user_loggedin:
        return 'Logged In Home Page. <a href="/logout">Logout</a>'
    else:
        return redirect(url_for('view.login'))

@view.route('/login')
@oidc.require_login
def login():
    current_app.logger.info('%s logged in successfully', oidc.user_getfield('email'))
    return redirect(url_for('view.index'))

@view.route('/logout')
@oidc.require_login
def logout():
    email = oidc.user_getfield('email')
    oidc.logout()
    redirect_url = request.url_root.strip('/')
    keycloak_issuer = oidc.client_secrets.get('issuer')
    keycloak_logout_url = '{}/protocol/openid-connect/logout'.format(
        keycloak_issuer
    )
    current_app.logger.info('%s logged out', email)

    return redirect('{}?redirect_uri={}'.format(
        keycloak_logout_url,
        redirect_url)
    )
