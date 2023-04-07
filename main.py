import os
import time
import tkinter as tk
import pyperclip
import keyboard
import win32api
from openai_api import get_response_stream_generate_from_ChatGPT_API

API_KEY = os.environ.get("OPENAI_API_KEY")
os.environ["https_proxy"] = "socks5://127.0.0.1:7890"


class ChatAnywhereApp:
    def __init__(self, master):
        self.master = master
        self.width = 100  # 窗口宽度
        self.height = 100  # 窗口高度
        self.master.title("ChatAnywhere")
        self.master.iconbitmap("chatgpt.ico")
        tk.Label(self.master, text="ChatAnywhere", font=("Arial", 20)).pack()
        tk.Label(self.master, text="\n使用方法:", font=("Arial", 18)).pack()
        tk.Label(self.master, text="选中文字，按下Ctrl+Alt+\\开始补全\n长按Ctrl停止当前补全", font=("Arial", 15)).pack()
        tk.Label(self.master, text="\n\n使用ChatAnywhere时请保证该窗口后台运行", font=("Arial", 12)).pack()

        # 绑定快捷键
        keyboard.add_hotkey('ctrl+alt+\\', self.complete)

    def complete(self):
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
            # 如果用户按下任意键 停止
            if keyboard.is_pressed('ctrl'):
                print("break")
                keyboard.write("--用户终止")
                time.sleep(0.1)
                while keyboard.is_pressed('ctrl'):
                    time.sleep(0.1)
                break
            # 将获得的内容进行输出
            print("gen:\t", g)
            keyboard.write(g)
        keyboard.write("】")
        for i in range(len(msg)):
            keyboard.press_and_release('delete')

        # 取消窗口置顶
        # self.master.attributes('-topmost', False)


if __name__ == '__main__':
    root = tk.Tk()
    app = ChatAnywhereApp(root)
    root.mainloop()
    keyboard.unhook_all_hotkeys()

