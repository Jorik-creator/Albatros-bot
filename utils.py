import pygetwindow as gw
from aiogram import types

import config
import cv2
import handlers
import pyautogui
import subprocess

current_language = config.Config.default_language


async def change_language(message: types.Message):
    selected_language = message.text
    if selected_language in config.translations:
        global current_language
        current_language = selected_language
        await handlers.settings(message)
        await message.reply(f"Language changed to {selected_language}")
    else:
        print(f"Language '{selected_language}' not supported. Keeping current language.")
        await message.reply(f"Language change failed. Current language is {current_language}")


def translate(key):
    global current_language
    return config.translations.get(current_language, {}).get(key, f'_{key}_')


async def open_shortcut(message: types.Message):
    selected_shortcut = message.text + '.url'
    try:
        with open(config.Config.SHORTCUTS_DIR + "/" + selected_shortcut, 'r') as url_file:
            for line in url_file:
                if line.lower().startswith('url='):
                    url = line[4:].strip()
        print("Launching" + url)
        subprocess.run(["start", url], shell=True)
        await message.reply(message.text + translate("launched"))
    except Exception as e:
        await message.reply(translate("error") + str(e))


async def openDesktop(message: types.Message):
    pyautogui.hotkey('win', 'd')
    await message.reply(translate('minimised'))


async def restoreWindows(message: types.Message):
    pyautogui.hotkey('win', 'shift', 'm')
    await message.reply(translate('resored'))


async def screenshot(message: types.Message):
    from main import bot
    screenshot_path = 'screenshot.png'
    pyautogui.screenshot(screenshot_path)
    print("Роблю скриншот")

    with open(screenshot_path, 'rb') as screenshot_file:
        await bot.send_photo(message.chat.id, screenshot_file, translate('catch a screenshot'))


async def webshot(message: types.Message):
    from main import bot
    webshot_path = 'webshot.jpg'

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    ret, frame = cap.read()

    cv2.imwrite(webshot_path, frame)
    cap.release()

    print("Say cheese")

    with open(webshot_path, 'rb') as webshot_file:
        await bot.send_photo(message.chat.id, webshot_file, translate('catch a webcamshot'))


async def closeApp(message: types.Message):
    window = gw.getWindowsWithTitle(message.text)[0]
    window.close()
    print("Application is closed")
    await message.reply(translate('closed') + message.text)


async def shutdown(message: types.Message):
    print("Shutdown PC")
    try:
        subprocess.run(["shutdown", "/s", "/t", "5"])
        await message.reply(translate('shut down'))
    except Exception as e:
        await message.reply(translate('error') + {str(e)})
