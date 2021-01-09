from secure import Secure


def main_handler(event, context):
    Secure('04181010', 'test_pwd').login()


if __name__ == '__main__':
    Secure('04181010', 'test_pwd').login()
