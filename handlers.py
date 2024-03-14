import pygetwindow as gw
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

import config
import glob
import os
import utils


async def send_welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_pc_managment = types.KeyboardButton(utils.translate("pc control"))
    button_open_game = types.KeyboardButton(utils.translate("open game"))
    button_settings = types.KeyboardButton(utils.translate("settings"))
    markup.add(button_pc_managment, button_open_game, button_settings)
    print("Bot is running")
    await message.reply(utils.translate("pc is ready"), reply_markup=markup)


async def open_game(message: types.Message):
    global available_shortcut
    available_shortcut = []
    shortcut_dir = os.path.join(config.Config.SHORTCUTS_DIR)

    if not os.path.isdir(shortcut_dir):
        await message.reply(utils.translate("no_shortcuts_dir"))
        return

    shortcut_files = glob.glob(os.path.join(shortcut_dir, '*.url'))

    if not shortcut_files:
        await message.reply(utils.translate("no_shortcuts_available"))
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton(utils.translate('back'))
    markup.add(button_back)

    for shortcut in shortcut_files:
        file_name = os.path.splitext(os.path.basename(shortcut))[0]
        available_shortcut.append(file_name)
        markup.add(types.KeyboardButton(file_name))

    print(available_shortcut)
    await message.reply(utils.translate("choosing game"), reply_markup=markup)


async def pcControlling(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_open_desktop = types.KeyboardButton(utils.translate("minimise windows"))
    button_restore_windows = types.KeyboardButton(utils.translate("restore windows"))
    button_screenshot = types.KeyboardButton(utils.translate("screenshot"))
    button_close_app = types.KeyboardButton(utils.translate("close program"))
    button_shutdown = types.KeyboardButton(utils.translate("pc off"))
    button_webcamshot = types.KeyboardButton(utils.translate("webcamshot"))
    button_back = types.KeyboardButton(utils.translate("back"))

    markup.add(button_open_desktop, button_restore_windows, button_screenshot, button_close_app, button_shutdown,
               button_webcamshot, button_back)
    await message.reply(utils.translate('instructions await'), reply_markup=markup)


async def settings(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_language = types.KeyboardButton(utils.translate('languages'))
    button_back = types.KeyboardButton(utils.translate('back'))

    markup.add(button_language, button_back)
    await message.reply(utils.translate('settings'), reply_markup=markup)


async def languages(message: types.Message):
    languages_list = list(config.translations.keys())
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for language in languages_list:
        button_language = types.KeyboardButton(language)
        markup.add(button_language)

    await message.reply("Select a language:", reply_markup=markup)


async def closeAppMenu(message: types.Message):
    global available_windows
    available_windows = []

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton(utils.translate('back'))

    window_titles = [window.title for window in gw.getWindowsWithTitle("")]

    for window_title in window_titles:
        item = types.KeyboardButton(window_title)
        available_windows.append(window_title)
        markup.add(item)
    markup.add(button_back)

    await message.reply(utils.translate('window select'), reply_markup=markup)


async def backToMainMenu(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_pc_managment = types.KeyboardButton(utils.translate("pc control"))
    button_open_game = types.KeyboardButton(utils.translate("open game"))
    button_settings = types.KeyboardButton(utils.translate("settings"))
    markup.add(button_pc_managment, button_open_game, button_settings)
    await message.reply(utils.translate("back menu"), reply_markup=markup)


async def stop(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.reply(utils.translate("back menu"), reply_markup=markup)
    exit(0)


def register_handlers(dp: Dispatcher):
    global available_shortcut
    available_shortcut = []
    global available_windows
    available_windows = []

    dp.register_message_handler(send_welcome, Command(commands=['start', 'help']))
    dp.register_message_handler(open_game, lambda message: message.text == utils.translate("open game"))
    dp.register_message_handler(pcControlling, lambda message: message.text == utils.translate("pc control"))
    dp.register_message_handler(settings, lambda message: message.text == utils.translate('settings'))
    dp.register_message_handler(languages, lambda message: message.text == utils.translate('languages'))
    dp.register_message_handler(closeAppMenu, lambda message: message.text == utils.translate("close program"))
    dp.register_message_handler(backToMainMenu, lambda message: message.text == utils.translate("back"))
    dp.register_message_handler(stop, Command(commands=['stop']))
    dp.register_message_handler(utils.change_language, text='ua' or 'en')
    dp.register_message_handler(utils.closeApp, lambda message: message.text in available_windows)
    dp.register_message_handler(utils.open_shortcut, lambda message: message.text in available_shortcut)
    dp.register_message_handler(utils.openDesktop, lambda message: message.text == utils.translate("minimise windows"))
    dp.register_message_handler(utils.restoreWindows,lambda message: message.text == utils.translate("restore windows"))
    dp.register_message_handler(utils.screenshot, lambda message: message.text == utils.translate("screenshot"))
    dp.register_message_handler(utils.webshot, lambda message: message.text == utils.translate("webcamshot"))
    dp.register_message_handler(utils.shutdown, lambda message: message.text == utils.translate("pc off"))
