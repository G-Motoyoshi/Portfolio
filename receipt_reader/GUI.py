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