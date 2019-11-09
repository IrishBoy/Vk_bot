from test import Bot


def main():
    with open('completed.txt', 'r') as f:
        s = f.read()
        completed_id = eval(s)
    bot = Bot(completed_id)
    bot.work()


if __name__ == '__main__':
    main()