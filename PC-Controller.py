import os
import subprocess
import ctypes
import time
import locale

class PC_Controller:
    
    def __init__(self):
        self.blue = '\033[94m'
        self.green = '\033[92m'
        self.end = '\033[0m'
        self.menu_options = {
            '1': (self._display_font_info, "Управление системными шрифтами (Информация)"),
            '2': (self._display_keyboard_layout, "Проверка текущей раскладки клавиатуры"),
            '3': (self._open_cmd, "Запуск Командной Строки (CMD)"),
            '4': (self._clear_temp_files, "Очистка временных системных файлов"),
            '5': (self._check_lock_keys, "Диагностика состояния клавиш-индикаторов"),
            '6': (self._reboot, "Перезагрузка системы"),
            '7': (self._shutdown, "Выключение системы"),
            '8': (self._display_boot_mode, "Проверка текущего режима загрузки (Boot Mode)"),
            '9': (self._show_system_info, "Отображение подробных сведений о системе"),
            '10': (self._open_task_manager, "Запуск Диспетчера Задач"),
            '11': (exit, "Выход из программы"),
        }

    def _execute(self, cmd_list, name):
        try:
            result = subprocess.run(cmd_list, shell=True, capture_output=True, text=True, check=False)
            output = result.stdout.strip() if result.stdout else "Операция выполнена."
            print(f"{self.green}[STATUS] {name}: Успех.\n{output[:150]}...{self.end}")
        except Exception as e:
            print(f"{self.blue}[INFO] Не удалось выполнить {name}. (Сбой: {e}){self.end}")

    def _display_font_info(self):
        print(f"{self.blue}Проверка наличия стандартного системного шрифта (Segoe UI).{self.end}")
        self._execute(['reg', 'query', r'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts', '/v', 'Segoe UI (TrueType)'], "Проверка шрифта")

    def _display_keyboard_layout(self):
        current_locale = locale.getlocale()
        print(f"{self.blue}Текущий региональный формат: {current_locale}. {self.end}")

    def _open_cmd(self):
        os.startfile("cmd.exe")
        print(f"{self.green}[STATUS] Командная Строка запущена. {self.end}")

    def _clear_temp_files(self):
        temp_dir = os.path.expandvars(r"%TEMP%")
        self._execute(['powershell', '-Command', f'Remove-Item -Path "{temp_dir}\\*" -Recurse -Force -ErrorAction SilentlyContinue'], "Очистка TEMP")

    def _check_lock_keys(self):
        cap = ctypes.windll.user32.GetKeyState(0x14) & 1
        num = ctypes.windll.user32.GetKeyState(0x90) & 1
        scroll = ctypes.windll.user32.GetKeyState(0x91) & 1
        print(f"{self.blue}Состояние клавиш-индикаторов: Caps Lock: {bool(cap)}, Num Lock: {bool(num)}, Scroll Lock: {bool(scroll)}{self.end}")

    def _reboot(self):
        self._execute(['shutdown', '/r'], "Инициализация перезагрузки (с предупреждением)")

    def _shutdown(self):
        self._execute(['shutdown', '/s'], "Инициализация выключения (с предупреждением)")

    def _display_boot_mode(self):
        self._execute(['bcdedit', '/enum', 'current'], "Получение информации о режиме загрузки")

    def _show_system_info(self):
        self._execute(['systeminfo'], "Получение сведений о системе")

    def _open_task_manager(self):
        subprocess.run(['taskmgr'], check=False)
        print(f"{self.green}[STATUS] Диспетчер Задач запущен. {self.end}")

    def run(self):
        while True:
            print("\n" + "="*45)
            print(f"""{self.blue}PC-CONTROLLER By N3lson
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@ %&&&&&&&&&&&&&&  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@ &&&&&&&&&&&&&&& (/// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@ &&&&&&&&&&&&&&@ (/////// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@ ,,,,,,,,,,,,,,* (////// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@@
@@@@@@@@&.///////////// *///////(#                                  %#  @@@@@@@@
@@@@@@@@&.              *///////(# ////////////////%%%/////%%%%%%%//%#  @@@@@@@@
@@@@@@@@&.///////////(/ *///////(# //////////////%%%/////%%%%%%/////%#  @@@@@@@@
@@@@@@@@&.              *///////(# ////////////#%%/////#%%%%%///////%#  @@@@@@@@
@@@@@@@@&.///////////// *///////(# //////////#%%/////#%%%%(/////////%#  @@@@@@@@
@@@@@@@@&(((((((((((((((*///////(# ////////#%%/////(%%%%////////////%#  @@@@@@@@
@@@@@@@@&.              *///////(# //////(%%//////%%%%//////////////%#  @@@@@@@@
@@@@@@@@&.///////////// *///////(# /////%%//////%%%/////////////////%#  @@@@@@@@
@@@@@@@@&.///////////// *///////(# ///%%//////%%%///////////////////%#  @@@@@@@@
@@@@@@@@&.///////////// *///////(# /%%//////%%//////////////////////%#  @@@@@@@@
@@@@@@@@&./////##////// *///////(##################################### @@@@@@@@@
@@@@@@@@&.///////(///// *///////////// @@@@@@@@@@//// @@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@&.///////////// *//////////* @@@@@@@@@*. ////  ,#@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@&###############*//////, @@@@@@@ /&&&&&&& ((, &&&&&&& @@@@@@@@@@@@@@@@@@
@@@@@@@@&#   #%   ######*//  @@@@@@@@@@@@@   ,(///////(((   #@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@ %%**%,,%,,%*,%,,/&,,%*,%,*%,,#&  @@@@@@@., /##&@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@,%//%//%//(#/*%//%//%//%//##//% .@@@@@@@@ **(****.@@@@@@@
@@@@@@@@@@@@@@@@@@@@ %//*%//%//%////////*%//%//%//#%  @@@@@@@@@@ ****** @@@@@@@@
@@@@@@@@@@@@@@@@@@@&////////////////////////////////@@@@@@@@@@@@@@  *@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{self.end}""")
            print("="*45)
            for key, (func, desc) in self.menu_options.items():
                print(f"{key}. {desc}")
            print("="*45)
            
            choice = input("Введите номер команды: ").strip()
            
            if choice in self.menu_options:
                if choice == '11':
                    print("Сессия завершена. Работа программы прекращена.")
                    break
                self.menu_options[choice][0]()
            else:
                print(f"{self.blue}Неверный выбор. Повторите ввод.{self.end}")

if __name__ == '__main__':
    if os.name == 'nt':
        controller = PC_Controller()
        controller.run()
    else:
        print("Данный скрипт PC-Controller предназначен для операционной системы Windows.")
