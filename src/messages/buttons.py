from . import emojidb as emo

btn_offices = emo.bank + " Отделения"
btn_atm = emo.atm +" Банкоматы"
btn_cash = emo.currency_exchange + " Валюта"
btn_quotations  = emo.chart_upword + " Акции"
btn_smile = emo.smile_open_mouth
btn_star = emo.star
btn_phone = emo.telephone_receive


keyboard_main_layout = [[btn_offices, btn_atm], 
						[btn_cash, btn_quotations], 
						[btn_smile, btn_star, btn_phone]]



btn_offices_send = "Отправить"
btn_offices_cansel = "Отмена"

keyboard_offices_layout = [[btn_offices_send, btn_offices_cansel]]