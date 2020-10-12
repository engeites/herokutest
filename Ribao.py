from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1291655921:AAEe_7Pvk7vpshDU1i4F_4em3ryjdYr6qag'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

a = ''


@dp.message_handler(commands=['count'])
async def stop_it(message: types.Message):

    global a
    try:
        clear_data = divide_data(a)
        summ = count_all(clear_data) - 1
    except Exception as e:
        await bot.send_message(1350298316, f"发生了错误：\n{e}")

    numbers = clean_data(clear_data)
    result = handle_data(numbers)


    await message.answer(f'金额：{summ}')
    await message.answer(f'后台手动加值金额: {result[1]}\n强的交易： {result[0]} 次\n此外: {result[2]}\
                         共计: {((summ - result[1]))/10} 元')
    await bot.send_message(1350298316, f"Bot was queried by: {message.from_user.username} \n")
    a = ''


@dp.message_handler(commands=['help'])
async def send_rules(message: types.Message):

    answer_text = """Ribao会帮助超管们计算每日报告里面用的数据


    Ribao的使用很简单:
1. 进代理 ——> 金币账单，然后选操作时间和类型，按搜索。 按 Ctrl-A。
2. 复制。
3. 打开Ribao， 粘贴 —— 发通报。
4. 一般金币账单有两个网页。转到第二页，重复步骤2和3
5. 发送了所有资料的话发给Ribao /count 指令。
恭喜啦! 程序将显示已完成的数据。


UPD. 每日报告是一天一次实现的任务， 所以两个超管不能同时用Ribao！要不然发生错误。"""

    await message.answer(answer_text)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
     await message.reply("你好！请发 /help 指令为了学会 Ribao 使用")


#Get a peace of info
@dp.message_handler(content_types = types.ContentTypes.TEXT)
async def add_data(message: types.Message):
    global a
    a += '\n' + message.text


def clean_data(data):

    daili_list = []
    summ_list = []
    search = '后台手动加值'
    search2 = '金币充值'

    for i in data:
        if search in i:
            daili_list.append(i)

    for i in daili_list:
        coordinates = i.find(search2)
        coordinates2 = i.find(search)
        new_line = i[coordinates + 4:coordinates2].strip()

        data = new_line.split('  ')[0]
        data = int(data)
        summ_list.append(data)
    return summ_list


# transform a big peace of data into a list of lines
def divide_data(data):
    new_data = data.split('\n')
    return new_data


# Count all the elements, adds Qiangs operations to the summ. Returns summ and number of Qiangs transactions
def handle_data(data: list):
    qiangs_transactions = 0
    big_transactions = []
    summ = 0
    for i in data:
        if i == 108000:
            qiangs_transactions += 1
        elif i == 216000:
            qiangs_transactions += 2
        elif i == 324000:
            qiangs_transactions += 3
        elif i > 324000:
            print("BIG TRANSACTION: ", i)
            big_transactions.append(i)

        else:
            print("count this: ", i)
            summ += i

    summ = (summ + (8000 * qiangs_transactions))

    return qiangs_transactions, summ, big_transactions


# Gets the summ of all the transactions having place. Used for checking purposes
def count_all(data):
    listing = []
    number = 0

    for i in data:
        new_line = i[i.find('金币充值')+4:].strip().replace('\t', ' ')
        coordinates = new_line.find(' ')
        new_line2 = new_line[:coordinates]
        try:
            int(new_line2)
            listing.append(int(new_line2))
            number+=1

        except ValueError:
            pass

    return sum(listing)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
