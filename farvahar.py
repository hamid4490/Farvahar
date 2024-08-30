#import logging
import pandas as pd
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, CallbackContext 

token = "7382150487:AAEBg27yUpiTER4U7X1wh8OPLD5gGU4-jG0"

chats = []
users = []
f_names = []
l_names = []


room=0
roz=0
price=0
keyboard = [
    [InlineKeyboardButton("اتاق 1 نفره", callback_data='1'), InlineKeyboardButton("اتاق 2 نفره", callback_data='2')],
    [InlineKeyboardButton("اتاق 3 نفره", callback_data='3'), InlineKeyboardButton("اتاق 4 نفره", callback_data='4')],
    [InlineKeyboardButton("عکس مکانهای مشترک", callback_data='5')]
]
reply_markup1 = InlineKeyboardMarkup(keyboard)

def price1():
    global reply_markup2
    keyboard1 = [
    [InlineKeyboardButton("روزانه", callback_data='d1'), InlineKeyboardButton("1 هفته", callback_data='d7')],
    [InlineKeyboardButton("2 هفته", callback_data='d14'), InlineKeyboardButton("ماهانه", callback_data='d30')],
    [InlineKeyboardButton("بازگشت", callback_data='d0')],
    [InlineKeyboardButton(" قیمت "+str(price)+" ریال ", callback_data='p0')]
    ]
    reply_markup2 = InlineKeyboardMarkup(keyboard1)

data2 = {
    'تاریخ': [],
    'ساعت': [],
    'آیدی': [],
    'نام کاربری': [],
    'اسم': [],
    'فامیل': []
}

df = pd.DataFrame(data2)
# مسیر فایل مورد نظر
file_path = 'bot.xlsx'
# بررسی وجود فایل
if os.path.isfile(file_path)==False:
   # ذخیره DataFrame به یک فایل اکسل
   df.to_excel('bot.xlsx', index=False, engine='openpyxl')


# تنظیمات لاگینگ
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global pic,photo_paths
    global room,price
    global roz, j
    j=0
    roz=0
    room=-1
    pic =0
    price=0
    now = datetime.now()
    t = (now.time().strftime("%H:%M:%S"))
    d = (now.date())
    photo_paths = {f'photo{i}': f'o{i}.jpg' for i in range(1, 8)}
    
    await update.message.reply_text("به ربات هاستل فروهر خوش آمدید")  
    await update.message.reply_text("تمامی اتاق ها مستر هستند")
    if roz == 0:
        for i in range(1, 8):
            keyboard.insert(0, [InlineKeyboardButton("", callback_data=f'photo{i}')])

        await update.message.reply_text("لطفا یک گزینه را انتخاب کنید", reply_markup=reply_markup1)

    #ثبت اطلاعات کاربری
    username = update.message.from_user.username
    chat = update.message.chat_id
    f_name = update.message.from_user.first_name
    l_name = update.message.from_user.last_name
    df = pd.read_excel('bot.xlsx', engine='openpyxl')
    new_data = {
    'تاریخ': [d],
    'ساعت': [t],
    'آیدی': [chat],
    'نام کاربری': [username],
    'اسم': [f_name],
    'فامیل': [l_name]
    }
    new_df = pd.DataFrame(new_data)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_excel('bot.xlsx', index=False, engine='openpyxl')

    


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global pic, pic1, pic2
    global roz
    global room
    global price
    global reply_markup2
    global reply_markup1,reply_markup1
    global chat_id1, send_photo, pic, j

    query = update.callback_query
    # دریافت داده‌ی callback_data
    data = query.data
    # ارسال پیام بر اساس داده‌ی callback_data   

    #  ارسال اطلاعات برای انتخاب اتاق
#    if room == 0:
#    pic = 0
    if data == "1" :
        room = 1
        pic = 0
    if data == "2" :
        room = 2
        pic = 0
    if data == "3" :
        room = 3
        pic = 0
    if data == "4" :
        room = 4
        pic = 0
    if data == "5" :
        room = 5

#   ارسال اطلاعات برای تعداد روز
#    if room != 0 and roz == 0:
    if data == "d1" :
        roz = 1
    if data == "d7" :
        roz = 7
    if data == "d14" :
        roz = 14
    if data == "d30" :
        roz = 30
    if data == "d0" :
        roz = 40
        room=-1
    if data == "p0" :
        price1()

#   ارسال اطلاعات برای دکمه بازگشت
    if room != 0 and roz==40:
       room=0
       roz=0
       pic=1
       query = update.callback_query
       # دریافت داده‌ی callback_data
       data = query.data
       # ارسال پیام بر اساس داده‌ی callback_data
       await context.bot.delete_message(chat_id=chat_id1, message_id=send_photo.message_id)
       await query.message.edit_text("لطفاً یک گزینه را انتخاب کنید:", reply_markup=reply_markup1)
       price=0
       price1()


    if room==1 :
        if roz==1:
            price=7
        if roz==7:
            price=45
        if roz==14:
            price=85
        if roz==30:
            price=150
        if roz!=40: roz=0
        pic1="5.jpg"

    if room==2 :
        if roz==1:
            price=9
        if roz==7:
            price=60
        if roz==14:
            price=110
        if roz==30:
            price=170
        if roz!=40: roz=0
        pic1="4.jpg"
        pic2="7.jpg"

    if room==3 :
        if roz==1:
            price=11
        if roz==7:
            price=70
        if roz==14:
            price=130
        if roz==30:
            price=180
        if roz!=40: roz=0
        pic1="6.jpg"

    if room==4 :
        if roz==1:
            price=14
        if roz==7:
            price=80
        if roz==14:
            price=150
        if roz==30:
            price=200
        if roz!=40: roz=0
        pic1="8.jpg" 

#   نمایش عکس مکانهای مشترک
    if room == 5 and j==0:
        pic1=1
        room=0
        context.chat_data['photo_messages'] = []  # لیست شناسه‌های پیام را برای حذف آماده می‌کنیم
        for photo_id, photo_path1 in photo_paths.items():
            j=j+1
            if j==7: back="بازگشت"
            else: back=""
            sent_message = await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=open(photo_path1, 'rb'),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(back, callback_data='delete')]
                ])
            )
            context.chat_data['photo_messages'].append(sent_message.message_id)
        
        # آخرین پیام حذف شده که دکمه حذف را ندارد
        last_photo_message = context.chat_data['photo_messages'][-1]
        
#   حذف عکس مکانهای مشترک
    if data == "delete":
        j = 0
        pic=1
        # حذف تمام عکس‌ها
        if 'photo_messages' in context.chat_data:
            for message_id in context.chat_data['photo_messages']:
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=message_id
                )
            del context.chat_data['photo_messages']




    price1()
    if pic == 0 and j==0:
        pic = 1
        chat_id1=query.message.chat_id
        photo=open(pic1,"rb")
        send_photo = await context.bot.send_photo(chat_id1,photo)
    
    if room != 0 and data != "p0" and room != 5 and j==0:
        await query.message.edit_text("لطفاً یک گزینه را انتخاب کنید:", reply_markup=reply_markup2)




def main() -> None:
    

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    
    application.add_handler(CommandHandler("help", help))

    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
