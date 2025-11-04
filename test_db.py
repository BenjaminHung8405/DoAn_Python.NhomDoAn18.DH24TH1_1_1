"""Small helper to test DATABASE_URL and connectivity using Database.config.test_connection

Run this after creating a `.env` file or exporting DATABASE_URL in your environment.
"""
from Database import config
import os

def main():
    print('DATABASE_URL (env):', os.getenv('DATABASE_URL'))
    print('DATABASE_URL (config):', config.DATABASE_URL)
    ok, err = config.test_connection()
    if ok:
        print('✅ Database connection test: OK')
    else:
        print('❌ Database connection test failed:')
        print(err)

if __name__ == '__main__':
    main()
