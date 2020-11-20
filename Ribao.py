from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1291655921:AAEe_7Pvk7vpshDU1i4F_4em3ryjdYr6qag'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


a = ''
b = ''

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
    text = f"""
    后台手动加值金额: {result[0]}
    强的交易： {result[1]} 次
    新雨交易： {result[2]} 次
    异常交易：{result[3]}
    正常交易：{result[4]}
    
共计: {((summ - result[0]))/10} 元
    """

    await message.answer(f'金额：{summ}')
    await message.answer(text)
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

@dp.message_handler(commands=['clean'])
async def extract_ids(message: types.Message):
    global b
    selected_lines = []
    all_lines = b.split('\n')
    text = ''
    print(all_lines)
    for line in all_lines:
        if "人气奖励" in line:
            print("I stop here")
            break
        elif "周榜人气奖励" in line:
            break
        else:
            try:
                int(line[0])
                print(f"I add {line} to selected_lines")
                selected_lines.append(line)
            except:
                print(line)
                print("I skip this line")
                continue
    for line in selected_lines:
        text += line.strip() + "\n"
        print(text)
    await message.answer(text)
    b = ""

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
     await message.reply("你好！请发 /help 指令为了学会 Ribao 使用")


#Get a peace of info
@dp.message_handler(content_types = types.ContentTypes.TEXT)
async def add_data(message: types.Message):
    if "第一名" in message.text[:30]:
        global b
        b = message.text
    else:
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

def check_xin(data):
    possible_values = [106000, 212000, 318000, 424000, 530000,
                       636000, 742000, 848000, 954000, 1060000]
    if data in possible_values:
        print(possible_values.index(data))
        return possible_values.index(data)+1


def check_qiang(data):
    possible_values = [108000, 214000, 324000, 432000, 540000,
                       648000, 756000, 846000, 972000, 1080000]
    if data in possible_values:
        print(possible_values.index(data))
        return possible_values.index(data)+1

# Count all the elements, adds Qiangs operations to the summ. Returns summ and number of Qiangs transactions
def handle_data(data: list):
    xin_transactions = 0
    qiang_transactions = 0
    big_transactions = []
    normal_transactions = []
    for line in data:
        if check_xin(line):
            xin_transactions += check_xin(line)
            continue
        elif check_qiang(line):
            qiang_transactions += check_qiang(line)
            continue
        elif line > 324000:
            big_transactions.append(line)
            continue
        else:
            normal_transactions.append(line)
    print(f'Qiang: {qiang_transactions}')
    print(f'Xin: {xin_transactions}')
    print(f'Weird: {big_transactions}')
    print(f'Normal: {normal_transactions}')

    normal_transactions_summ = sum(normal_transactions)
    overall_summ = (qiang_transactions * 8000) + (xin_transactions * 6000) + normal_transactions_summ
    print(f"""Normal_transactions: {normal_transactions_summ}
Overall summ: {overall_summ}""")

    return overall_summ, qiang_transactions, xin_transactions, big_transactions, normal_transactions_summ

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