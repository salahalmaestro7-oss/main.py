import os
import telebot
from google import genai
from google.genai import types

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("خطأ: يرجى ضبط متغيرات البيئة في المنصة.")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    try:
        bot.reply_to(message, "⏳ جاري فحص الشارت وتحليل الهيكل ومناطق السيولة (ICT & موجات إليوت)...")

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        image_path = "temp_chart.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        with open(image_path, 'rb') as img_file:
            image_bytes = img_file.read()

        prompt = (
            "أنت محلل محترف ومخضرم في أسواق المال وتحديداً في مدرسة مفاهيم الأموال الذكية (ICT / SMC) وموجات إليوت. "
            "قم بتحليل شارت التداول المرفق في الصورة بدقة تامة، وحدد لي:\n"
            "1. الهيكل الحالي واتجاه السوق على الفريم المعروض (Market Structure / MSS / ChoCH).\n"
            "2. مناطق السيولة المستهدفة، فجوات القيمة العادلة (FVG)، وكتل الطلب (Order Blocks) الظاهرة.\n"
            "3. العد الموجي المرجح للوضع الحالي.\n"
            "4. سيناريوهات الدخول المحتملة (بيع أو شراء) مع تحديد مستويات وقف الخسارة والأهداف بدقة."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                prompt
            ]
        )

        bot.reply_to(message, response.text)

        if os.path.exists(image_path):
            os.remove(image_path)

    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء المعالجة: {str(e)}")

print("Bot is up and running on Cloud...")
bot.infinity_polling()
