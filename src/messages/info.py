from . import emojidb

starting_message="""
<b>Запущен в тестовом режиме.</b> Работаю круглосуточно и всегда готов Вам помочь {0}

{1} <b>Расскажите друзьям</b>
Мой username @BankTestBot

{2} <b>Официальный сайт</b>
www.testtest.kz

{3} <b>Предложения и замечания по Боту</b>
bekbaganbetov.abay@gmail.com
""".format(emojidb.ok_hand, emojidb.smile_open_mouth, emojidb.check_mark, emojidb.envelope)


helping_info = """
<b>Чем я могу Вам помочь?</b> Отправьте мне "/help" для справки.
"""



share_location_office = """
Я найду {0} отделения рядом с Вами.
Пожалуйста, отправьте Ваше местоположение.
""".format(emojidb.bank)

share_location_atm = """
Я найду {0} отделения рядом с Вами.
Пожалуйста, отправьте Ваше местоположение.
""".format(emojidb.atm)


cansel = "Возвращаюсь"

currancy_rate = """
<b>USD</b> (Доллар США)
• Продажа: 337.5 KZT
• Покупка: 332.5 KZT
<b>EUR</b> (Евро)
• Продажа: 392 KZT
• Покупка: 387 KZT
"""