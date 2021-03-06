POSTGRES_PARAMS = {
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'database': 'tb_tonya',
    'port': '5432'
}

TELEGRAM_BOT_TOKEN = 'postgresql://{}:{}@{}:{}/{}'.format(
    POSTGRES_PARAMS['user'],
    POSTGRES_PARAMS['password'],
    POSTGRES_PARAMS['host'],
    POSTGRES_PARAMS['port'],
    POSTGRES_PARAMS['database']
)

ROUTES_API_PREFIX = 'api'
