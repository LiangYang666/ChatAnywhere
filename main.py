import os
import time
import tkinter as tk
import pyperclip
import keyboard
import win32api
import win32gui
from openai_api import get_response_stream_generate_from_ChatGPT_API

API_KEY = os.environ.get("OPENAI_API_KEY")
os.environ["https_proxy"] = "socks5://127.0.0.1:7890"


class TranslatorApp:
    def __init__(self, master):
        self.master = master
        self.width = 300  # 窗口宽度
        self.height = 200  # 窗口高度

        # 创建翻译框
        self.textbox = tk.Text(master, height=10)
        self.textbox.pack()

        # 创建复制按钮
        self.copy_button = tk.Button(master, text="复制到剪切板", command=self.copy)
        self.copy_button.pack()

        # 绑定快捷键 释放后再调用
        keyboard.add_hotkey('ctrl+alt+\\', self.translate)

    def center_window(self):
        # 计算窗口的中心位置
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        # 如果按下快捷键时鼠标指针在屏幕的右边，则将窗口置于鼠标左侧
        mouse_x, mouse_y = win32api.GetCursorPos()
        if mouse_x > screen_width // 2:
            x = mouse_x - 10 - self.width

        # 如果按下快捷键时鼠标指针在屏幕的下方，则将窗口置于鼠标上方
        if mouse_y > screen_height // 2:
            y = mouse_y - 10 - self.height

        # 设置窗口居中显示
        self.master.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

    def copy(self):
        # 将翻译框内容复制到剪切板
        pyperclip.copy(self.textbox.get('1.0', tk.END))

    def translate(self):
        # 等待三个键都释放
        while keyboard.is_pressed('alt') or keyboard.is_pressed('\\') or keyboard.is_pressed('ctrl'):
            time.sleep(0.1)

        # # 将窗口置顶并居中显示
        # self.master.attributes('-topmost', True)
        # self.center_window()
        # 清空剪切板
        pyperclip.copy('')
        # 模拟按下ctrl+c
        keyboard.press_and_release('ctrl+c')
        # 等待完成复制并设置1s超时
        try:
            pyperclip.waitForNewPaste(timeout=1)
        except pyperclip.PyperclipTimeoutException:
            print("复制超时，释放")
            return

        # 获取剪切板内容并翻译
        original_text = pyperclip.paste()
        print("original_text:\t", original_text)
        keyboard.press_and_release('right')
        # translated_text = my_translation_function(original_text)
        # print("response_text:\t", translated_text)
        msg = "【请稍等，等待补全】"
        keyboard.write(msg)
        message_history = []
        generate = get_response_stream_generate_from_ChatGPT_API(original_text, API_KEY, message_history)
        # 删除提示字符
        for i in range(len(msg)):
            keyboard.press_and_release('backspace')
        msg = " << 请勿其它操作，长按ctrl键终止"
        keyboard.write("【"+msg)
        for i in range(len(msg)):
            keyboard.press_and_release('left')


        for g in generate():
            # 将获得的内容进行输出
            print("gen:\t", g)
            keyboard.write(g)
            # 如果用户按下任意键 停止
            if keyboard.is_pressed('ctrl'):
                print("break")
                keyboard.write("--用户终止")
                time.sleep(0.1)
                while keyboard.is_pressed('ctrl'):
                    time.sleep(0.1)
                break
        keyboard.write("】")
        for i in range(len(msg)):
            keyboard.press_and_release('delete')

        # 取消窗口置顶
        # self.master.attributes('-topmost', False)


if __name__ == '__main__':
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()