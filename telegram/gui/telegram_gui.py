#!/usr/bin/env python3

import re
import sys
import signal
import asyncio

from asyncqt import QEventLoop, asyncSlot, asyncClose
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import *

from telegram.core.config import config
from telegram.core.logger import logger
from telegram.core.bot import Bot

bot = None


class TelegramGUI(QWidget):

    def __init__(self, loop=None):
        super().__init__()
        uic.loadUi('telegram/gui/ui/form.ui', self)
        self.loop = loop
        self.init_components()

    def init_components(self):

        self.tab_widget = self.findChild(QTabWidget, 'tabWidget')
        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(2, False)
        self.tab_widget.setTabEnabled(3, False)

        # Input for Page 1
        self.input_session = self.findChild(QLineEdit, 'input_session')
        self.input_api_key = self.findChild(QLineEdit, 'input_api_key')
        self.input_api_key.setValidator(QtGui.QIntValidator())
        self.input_api_hash = self.findChild(QLineEdit, 'input_api_hash')
        self.input_phone = self.findChild(QLineEdit, 'input_phone')

        # TODO: Remove after development
        self.input_api_key.setText(config['API_KEY'])
        self.input_api_hash.setText(config['API_HASH'])
        self.input_phone.setText(config['PHONE'])

        # Input for Page 3
        self.input_phone_2 = self.findChild(QLineEdit, 'input_phone_2')
        self.input_code = self.findChild(QLineEdit, 'input_code')

        # Input for Page 3
        self.input_channels = self.findChild(QPlainTextEdit, 'input_channels')

        # Input for Page 4
        self.input_channels_2 = self.findChild(QPlainTextEdit, 'input_channels_2')
        self.input_message = self.findChild(QPlainTextEdit, 'input_message')

        # Buttons for Page 1
        self.btn_generate_code = self.findChild(QPushButton, 'btn_generate_code')
        self.btn_generate_code.clicked.connect(self.generate_code)

        self.btn_sign_out = self.findChild(QPushButton, 'btn_sign_out')
        self.btn_sign_out.clicked.connect(self.sign_out)

        # Buttons for Page 2
        self.btn_sign_in = self.findChild(QPushButton, 'btn_sign_in')
        self.btn_sign_in.clicked.connect(self.sign_in)

        self.btn_sign_out_1 = self.findChild(QPushButton, 'btn_sign_out_1')
        self.btn_sign_out_1.clicked.connect(self.sign_out)

        # Buttons for Page 3
        self.btn_join_channels = self.findChild(QPushButton, 'btn_join_channels')
        self.btn_join_channels.clicked.connect(self.join_channels)

        self.btn_sign_out_2 = self.findChild(QPushButton, 'btn_sign_out_2')
        self.btn_sign_out_2.clicked.connect(self.sign_out)

        # self.btn_skip = self.findChild(QPushButton, 'btn_skip')
        # self.btn_skip.clicked.connect(self.show_send_message_window)

        # Buttons for Page 4
        self.btn_send_message = self.findChild(QPushButton, 'btn_send_message')
        self.btn_send_message.clicked.connect(self.send_message)

        self.btn_sign_out_3 = self.findChild(QPushButton, 'btn_sign_out_3')
        self.btn_sign_out_3.clicked.connect(self.sign_out)

        # self.statusBar().showMessage('Offline')

        self.init_table()

    def init_table(self):
        self.table = self.findChild(QTableWidget, 'tableWidget')

        self.table.setRowCount(4)
        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(['Channel', 'Joined', 'Message Sent', 'Error'])
        # self.table.setVerticalHeaderLabels(['Channel'])

        self.table.setItem(0, 0, QTableWidgetItem('Channel Name'))
        self.table.setItem(0, 1, QTableWidgetItem('Joined or Not'))
        self.table.setItem(0, 2, QTableWidgetItem('Message Sent or Failed'))
        self.table.setItem(0, 3, QTableWidgetItem('Error'))

        self.table.resizeColumnsToContents()

    @asyncSlot()
    async def generate_code(self):
        logger.info('generate_code')

        bot_config = {
            'APP_SESSION': self.input_session.text().strip(),
            'API_KEY': self.input_api_key.text().strip(),
            'API_HASH': self.input_api_hash.text().strip(),
            'PHONE': self.input_phone.text().strip(),
            'APP_ENV': config['APP_ENV']
        }

        if(bot_config.get('APP_ENV') == 'test'):
            bot_config['TEST_SERVER'] = config['TEST_SERVER']

        if '' in bot_config.values():
            self.show_error(message='Please fill all the values.')
            return
        
        global bot
        bot = Bot(bot_config)

        data = await bot.initiate(self.loop)

        logger.info('generate_code: data')
        logger.info(data)

        bot.client = data['client']

        if(data.get('started')):
            title = 'Session Found'
            message = 'Session is started from old login, you can start using the app'

            self.show_message_box(title, message)

            self.input_phone_2.setText(self.input_phone.text())
            self.tab_widget.setTabEnabled(0, False)
            self.tab_widget.setTabEnabled(2, True)
            self.tab_widget.setTabEnabled(3, True)
            self.tab_widget.setCurrentIndex(2)
        else:
            title = 'Session Initiate'
            message = 'If you have received the code on telegram, enter code at sign in page to start the session'
        
            self.show_message_box(title, message)

            self.input_phone_2.setText(self.input_phone.text())
            self.tab_widget.setTabEnabled(0, False)
            self.tab_widget.setTabEnabled(1, True)
            self.tab_widget.setCurrentIndex(1)


    def get_code(self):
        code, ok = QInputDialog.getText(self, 'Code', 'Enter the code received on telegram', QLineEdit.Normal, '')
        if ok:
            print(f'code: {code}')
            return code
        else:
            print('Cancelled')


    @asyncSlot()
    async def sign_in(self):
        logger.info('sign_in')

        phone = self.input_phone_2.text().strip()
        code = self.input_code.text().strip()

        if not phone or not code:
            self.show_error(message='Please fill all the values.')
            return

        await bot.sign_in(phone=phone, code=code)

        self.show_message_box('Sign In', 'Sign In Successful')
        self.tab_widget.setTabEnabled(2, True)
        self.tab_widget.setTabEnabled(3, True)
        self.tab_widget.setCurrentIndex(2)

    @asyncSlot()
    async def sign_out(self):
        logger.info('sign_out')

        await bot.client.log_out()

        self.show_message_box('Sign Out', 'Sign Out Successful')
        self.tab_widget.setTabEnabled(0, True)
        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(2, False)
        self.tab_widget.setTabEnabled(3, False)
        self.tab_widget.setCurrentIndex(0)
    
    @asyncSlot()
    async def join_channels(self):
        logger.info('join_channels')

        channels_str = self.input_channels.toPlainText().strip()
        channels = re.sub(r'\s+', ',', channels_str)
        channels = [x.strip() for x in channels.split(',') if x.strip()]
        logger.info(f'join_channels: {channels}')

        if not channels:
            self.show_error(message='Please fill all the values.')
            return
        
        results = {}
        for channel in channels:
            results[channel] = await bot.join_channel(channel)

        logger.info('join_channels results')
        logger.info(results)

        self.table.setRowCount(len(results))
        for index, channel in enumerate(results):
            self.table.setItem(index, 0, QTableWidgetItem(channel))
            self.table.setItem(index, 1, QTableWidgetItem('Yes' if results.get(channel).get('joined') else 'No'))
            self.table.setItem(index, 2, QTableWidgetItem(''))
            self.table.setItem(index, 3, QTableWidgetItem(results.get(channel).get('error')))

        # joined_channels = filter(lambda ch: ch.get('joined'), channels)
        
        self.input_channels_2.insertPlainText('\n'.join(channels))
        self.show_message_box('Success', 'Channel Joined!!')
    
    @asyncSlot()
    async def send_message(self):
        logger.info('send_message')

        channels_str = self.input_channels_2.toPlainText().strip()
        channels = re.sub(r'\s+', ',', channels_str)
        channels = [x.strip() for x in channels.split(',') if x.strip()]

        message = self.input_message.toPlainText().strip()
        logger.info(f'send_message: channels: {channels}, message: {message}')

        if not channels or not message:
            self.show_error(message='Please fill all the values.')
            return

        results = await bot.join_channels_and_send_message(channels, message)
        logger.info('send_message results')
        logger.info(results)

        self.table.setRowCount(len(results))
        for index, channel in enumerate(results):
            self.table.setItem(index, 0, QTableWidgetItem(channel))
            self.table.setItem(index, 1, QTableWidgetItem('Yes' if results.get(channel).get('joined') else 'No'))
            self.table.setItem(index, 2, QTableWidgetItem('Yes' if results.get(channel).get('sent') else 'No'))
            self.table.setItem(index, 3, QTableWidgetItem(results.get(channel).get('error')))

        # is_success = len(list(filter(lambda channel: results[channel].get('error') is not None, channels))) is 0

        self.show_message_box('Success', 'Message Sent!!')

    def show_error(self, title='Error', message=''):
        QMessageBox.about(self, title, message)

    def show_message_box(self, title, message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(message)
        message_box.setWindowTitle(title)
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # message_box.buttonClicked.connect(message_box_on_click)

        if(message_box.exec() == QMessageBox.Ok):
            print('OK')


# Handler Ctrl+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

def main_gui():
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    ex = TelegramGUI(loop)
    ex.show()

    with loop:
        sys.exit(loop.run_forever())

if __name__ == '__main__':
    main_gui()
