PRODUCTION = 'production'
DEVELOPMENT = 'development'


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '5f352388884c22463451387a0aec5d2f'
    SERVICE_SLUG = 'portal'
    OIDC_REQUIRE_VERIFIED_EMAIL = False
    OIDC_USER_INFO_ENABLED = True
    OIDC_SCOPES = ['openid', 'email', 'profile']
    OIDC_INTROSPECTION_AUTH_METHOD = 'client_secret_post'
    SWAGGER_DOCS = 'docs'
    SWAGGER_SPEC = 'spec'


class ProductionConfig(Config):
    OIDC_CLIENT_SECRETS = 'config/client_secrets_prod.json'
    OIDC_OPENID_REALM = 'flask-demo'
    OIDC_ID_TOKEN_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    ENV = DEVELOPMENT
    OIDC_CLIENT_SECRETS = 'config/client_secrets_dev.json'
    OIDC_OPENID_REALM = 'flask-demo'
    OIDC_ID_TOKEN_COOKIE_SECURE = False
