USER_BASIC = dict(username='test', email='test@test.com', password='test')
USER_INVALID_STRUCTURE = dict(email='test@test.com')
USER_NO_USERNAME = dict(username='', email='test@test.com', password='test')
USER_NO_EMAIL = dict(username='test', email='', password='test')
USER_NO_PASSWORD = dict(username='test', email='test@test.com', password='')
USER_DUPLICATE_USERNAME = dict(username='test', email='test2@test.com', password='test')
USER_DUPLICATE_EMAIL = dict(username='test2', email='test@test.com', password='test')