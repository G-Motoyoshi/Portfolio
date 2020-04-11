# モジュールのインポート
import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox


# ファイル選択ダイアログの表示
def fileopen(text):
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('レシート読み取り',text)
    file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    return file

def folderopen(text):
    root = tkinter.Tk()
    root.withdraw()
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('レシート読み取り',text)
    folder = tkinter.filedialog.askdirectory(initialdir =  iDir)
    return folder

def notice_end():
    tkinter.messagebox.showinfo('レシート読み取り', '入力が完了しました。')

def check_amount(filepath, amount):
    ret = tkinter.messagebox.askyesno('入力情報の確認', f'これで正しいですか？\n{filepath}\n金額: {amount}')
    if ret == False:
        return True

def input_correct():
    root = tkinter.Tk()
    root.geometry('300x200')
    root.title('入力情報の修正')

    # label = tkinter.Label(text='正しい情報')
    # label.place(x=30, y=95)

    text = tkinter.Entry(width=20)
    # text.place(x=60, y=120)
    text.pack()
    out_text = text.get()

    root.mainloop()

    return out_text