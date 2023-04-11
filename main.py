import os
import time
import tkinter as tk
import pyperclip
import keyboard
import win32api
from openai_api import get_response_stream_generate_from_ChatGPT_API

API_KEY = os.environ.get("OPENAI_API_KEY")  # 可在此处修改默认的 API_KEY = "sk-xxxx"，或在环境变量中设置OPENAI_API_KEY，或者在窗口中设置
https_proxy = os.environ.get("https_proxy", "socks5://127.0.0.1:7890")  # 可在此处修改默认的代理，或在环境变量中设置https_proxy，或者在窗口中设置

os.environ["https_proxy"] = https_proxy


class ChatAnywhereApp:
    def __init__(self, master):
        self.master = master
        self.width = 100  # 窗口宽度
        self.height = 100  # 窗口高度
        self.master.title("ChatAnywhere")
        self.master.iconbitmap("chatgpt.ico")
        self.https_proxy = https_proxy
        self.apikey = API_KEY
        self.complete_number = 150
        self.temperature = 0.9
        tk.Label(self.master, text="ChatAnywhere", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, padx=10,
                                                                            pady=10)
        tk.Label(self.master, text="\n使用方法:", font=("Arial", 18)).grid(row=1, column=0, columnspan=2, padx=10,
                                                                           pady=10)
        tk.Label(self.master, text="选中文字，按下Ctrl+Alt+\\开始补全\n长按Ctrl停止当前补全", font=("Arial", 15)).grid(
            row=2, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.master,
                 text="\n\n使用ChatAnywhere时请保证该窗口后台运行\n-----------------------------------\n\n设置",
                 font=("Arial", 12)).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        row = 3
        # api_key
        row += 1
        self.lbl_apikey = tk.Label(self.master, text="api_key:")
        self.lbl_apikey.grid(row=row, column=0, padx=10, pady=10)
        self.ent_apikey = tk.Entry(self.master)
        self.ent_apikey.insert(0, API_KEY)
        self.ent_apikey.grid(row=row, column=1, padx=10, pady=10)
        # 补全文字数量限制
        row += 1
        self.lbl_number = tk.Label(self.master, text="补全文字数量限制:")
        self.lbl_number.grid(row=row, column=0, padx=10, pady=10)
        self.ent_number = tk.Entry(self.master)
        self.ent_number.insert(0, str(self.complete_number))
        self.ent_number.grid(row=row, column=1, padx=10, pady=10)
        # temperature设置
        row += 1
        self.lbl_temperature = tk.Label(self.master, text="temperature:")
        self.lbl_temperature.grid(row=row, column=0, padx=10, pady=10)
        self.ent_temperature = tk.Entry(self.master)
        self.ent_temperature.insert(0, str(self.temperature))
        self.ent_temperature.grid(row=row, column=1, padx=10, pady=10)
        # 代理设置
        row += 1
        self.lbl_proxy = tk.Label(self.master, text="代理设置:")
        self.lbl_proxy.grid(row=row, column=0, padx=10, pady=10)
        self.ent_proxy = tk.Entry(self.master)
        self.ent_proxy.insert(0, self.https_proxy)
        self.ent_proxy.grid(row=row, column=1, padx=10, pady=10)
        # 提交按钮
        row += 1
        self.btn_submit = tk.Button(self.master, text="修改", command=self.submit)
        self.btn_submit.grid(row=row, column=1, padx=10, pady=10)

        # 绑定快捷键
        keyboard.add_hotkey('ctrl+alt+\\', self.complete)

    def submit(self):
        # 提交修改
        self.apikey = self.ent_apikey.get()
        self.complete_number = int(self.ent_number.get())
        self.temperature = float(self.ent_temperature.get())
        self.https_proxy = self.ent_proxy.get()
        os.environ["https_proxy"] = self.https_proxy
        self.btn_submit["text"] = "修改成功"

        def reset():
            self.btn_submit["text"] = "修改"

        self.master.after(700, reset)
        print("修改成功")

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
        generate = get_response_stream_generate_from_ChatGPT_API(original_text, API_KEY, message_history,
                                                                 temperature=self.temperature,
                                                                 complete_number=self.complete_number)
        # 删除提示字符
        for i in range(len(msg)):
            keyboard.press_and_release('backspace')
        msg = " << 请勿其它操作，长按ctrl键终止】"
        keyboard.write("【" + msg)
        for i in range(len(msg)):
            keyboard.press_and_release('left')

        for g in generate():
            # 如果用户按下任意键 停止
            if keyboard.is_pressed('ctrl'):
                print("\n--用户终止")
                keyboard.write(" >> 用户终止")
                return
            # 将获得的内容进行输出
            print(g, end="")
            keyboard.write(g)
        print()
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
