# -*- coding: utf-8 -*-
import os
from datetime import datetime
from lunar_python import Solar
from linebot import LineBotApi
from linebot.models import TextSendMessage

# 從 GitHub Secrets 讀取金鑰與 ID
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')

def send_line_message(message):
    """使用 Messaging API 發送 Push Message"""
    if not LINE_CHANNEL_ACCESS_TOKEN or not USER_ID:
        print("錯誤：尚未設定 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_USER_ID")
        return
        
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    try:
        line_bot_api.push_message(
            USER_ID,
            TextSendMessage(text=message)
        )
        print("LINE 訊息推送成功！")
    except Exception as e:
        print(f"發送失敗，錯誤資訊: {e}")

def check_and_notify():
    """檢查今天的農曆日期並發送對應提醒"""
    today_solar = Solar.fromDate(datetime.now())
    lunar = today_solar.getLunar()
    
    month_name = lunar.getMonthInChinese()
    day_name = lunar.getDayInChinese()
    lunar_day = lunar.getDay()
    
    print(f"今天是國曆: {datetime.now().strftime('%Y-%m-%d')}，農曆: {month_name}月{day_name}")

    # 初一 (1) 或 十五 (15)：布施提醒
    if lunar_day in [1, 15]:
        msg = f"🌟 【無限財富與佈施提醒】\n今天是農曆 {month_name}月{day_name}。\n心懷慈悲，廣結善緣，今天記得安排您的「佈施」計畫，累積福德與財富磁場！🙏"
        send_line_message(msg)
        
    # 初二 (2) 或 十六 (16)：拜拜提醒
    elif lunar_day in [2, 16]:
        msg = f"🏮 【土地公/福德正神拜拜提醒】\n今天是農曆 {month_name}月{day_name}（做牙）。\n記得準備供品敬拜土地公，祈求事業順遂、財源廣進、合家平安！💰"
        send_line_message(msg)
    else:
        print("今天沒有需要發送的特殊農曆提醒。")

if __name__ == "__main__":
    check_and_notify()
