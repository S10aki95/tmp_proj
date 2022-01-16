"""
二つのデータフレームを比較して差分を確認する実行スクリプト
"""

import pandas as pd
import numpy as np
from tkinter import *
from tkinter import font
import tkinter.ttk as ttk

class Main(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        # self.pack()
        
        #縦幅400横幅200に画面サイズを変更します。
        master.geometry("1200x500")
        
        #タイトルを指定
        master.title("出力の確認")
        
        # = =================================================================================
        # データの読み込み
        # new_dfを新しく作成したリストとする
        # old_dfを既存のリストとする
        # = =================================================================================
        self.new_df = pd.read_csv('C:/Users/akihiro/tmp_proj/test_1.csv', encoding='SHIFT-JIS')
        self.old_df = pd.read_csv('C:/Users/akihiro/tmp_proj/test_2.csv', encoding='SHIFT-JIS')
        self.trashed_df = None
        
        self.checked_for_delete_list = []
        
        # 更新ボタン関係の設定
        self.btn_update = Button(master, text = "更新", command = self.Update_Data_func)
        self.btn_update.place(x=50, y=20)
        
        # =================================================================
        # Treeviewの設定
        self.tree_new = ttk.Treeview(master, columns=[i for i in range(len(self.new_df.columns))])
        self.tree_new["show"] = "headings"
        
        # 事前にディスプレイに表示
        self.Data_to_display_func()
        
        
        # tree_newの表示設定
        for i, col_name in enumerate(self.new_df.columns):
            self.tree_new.column(i, width=150)
            self.tree_new.heading(i, text=col_name)
        self.tree_new.place(x=50, y=80)
        
        
        #self.tree_new.bind("<ButtonPress-1>", self.bDown)
        #self.tree_new.bind("<ButtonRelease-1>", self.bUp, add='+')
        self.tree_new.bind("<B1-Motion>", self.bMove, add='+')
        self.tree_new.bind("<Shift-ButtonPress-1>", self.bDown_Shift, add='+')
        self.tree_new.bind("<Shift-ButtonRelease-1>", self.bUp_Shift, add='+')
        
        # タイトル入力
        font2 = font.Font(family='Times', size=10)
        label_new = Label(master, text="更新後の承認者・報告者", font=font2)
        label_new.place(x=200, y=50)
        
        
        # ==================================================================
        # Treeviewの設定
        self.tree_old = ttk.Treeview(master, columns=[i for i in range(len(self.old_df.columns))], selectmode='none')
        self.tree_old["show"] = "headings"
        
        # 新しく作成されたデータを事前に入力しておく
        for i in range(len(self.old_df)):
            self.tree_old.insert("", "end", values=tuple([self.old_df.iloc[i, j] for j in range(len(self.old_df.columns))]))
        
        # tree_oldの表示設定
        for i, col_name in enumerate(self.old_df.columns):
            self.tree_old.column(i, width=150)
            self.tree_old.heading(i, text=col_name)
        self.tree_old.place(x=550, y=80)
        
        
        # タイトル入力
        label_old = Label(master, text="更新前の承認者・報告者", font=font2)
        label_old.place(x=700, y=50)
        
        
        # ==================================================================
        # Treeviewの設定
        self.tree_trashed = ttk.Treeview(master, height=5, columns=[i for i in range(len(self.old_df.columns))], selectmode='none')
        self.tree_trashed["show"] = "headings"
        
        # tree_trashedの表示設定(new_dfと同じ)
        for i, col_name in enumerate(self.new_df.columns):
            self.tree_trashed.column(i, width=150)
            self.tree_trashed.heading(i, text=col_name)
        self.tree_trashed.place(x=50, y=350)
        
        
        # タイトル入力
        label_old = Label(master, text="更新前の承認者・報告者", font=font2)
        label_old.place(x=200, y=320)
    
    
    
    
    
    def DataInitialization(self):
        self.tree_new.delete(*self.tree_new.get_children())
        self.tree_trashed.delete(*self.tree_trashed.get_children())
    
    
    
    
    def Update_Data_func(self):
        
        # 削除対象に指定されたリストの作成
        self.checked_for_delete_list += [self.tree_new.set(item) for item in self.tree_new.selection()]
        
        # tree_newの内容を削除
        self.DataInitialization()
        
        # 指定された人物についてサーチして削除
        all_list = []
        for d in self.checked_for_delete_list:
            init_list = []
            for key, value in d.items():
                if value == 'nan':
                    value = np.nan
                else:
                    pass
                init_list.append(self.new_df[self.new_df.columns[int(key)]].isin([value]))
            
            all_list.append(pd.concat(init_list, axis=1).all(axis=1))
        
        # チェックされなかった人物のみ残す
        self.new_df = self.new_df[~pd.concat(all_list, axis=1).any(axis=1)]
        
        # 表示をアップデート
        self.Data_to_display_func()
    
    
    
    
    
    def Data_to_display_func(self):
        
        # 新データと旧データの差分を観測
        self.check_differences()
        
        
        # 更新
        for i in range(len(self.new_df)):
                self.tree_new.insert("", "end", values=tuple([self.new_df.iloc[i, j] for j in range(len(self.new_df.columns))]))
        
        # 削除した人物も記録
        if len(self.checked_for_delete_list) == 0:
            pass
        else:
            for tmp_dict in self.checked_for_delete_list:
                self.tree_trashed.insert("", "end", values = tuple(tmp_dict.values()))
    
    
    
    def init_test_for_df(self):
        if (self.new_df.columns != self.old_df.columns).any():
            print("フォーマットが一致しないデータを参照してます。")
        else:
            pass
    
    
    def check_differences(self):
        
        # 新旧データのフォーマットが一致しているかを確認
        self.init_test_for_df()
        
        # 新しく加わったデータを確認
        for col_name in self.new_df.columns:
            list_1 = self.new_df[col_name].to_list()
            list_2 = self.old_df[col_name].to_list()
            
            self.newly_added_list = [i for i in set(list_1) - set(list_2)]
            self.newly_deleted_list = [i for i in set(list_2) - set(list_1)]
        
    
    
    
    # =========================================
    # motionの追加
    # =========================================
    
    def bDown_Shift(self, event):
        tv = event.widget
        select = [tv.index(s) for s in tv.selection()]
        select.append(tv.index(tv.identify_row(event.y)))
        select.sort()
        for i in range(select[0],select[-1]+1,1):
            tv.selection_add(tv.get_children()[i])

    
    def bDown(self, event):
        tv = event.widget
        if tv.identify_row(event.y) not in tv.selection():
            tv.selection_set(tv.identify_row(event.y))    
    
    
    def bUp(self, event):
        tv = event.widget
        if tv.identify_row(event.y) in tv.selection():
            tv.selection_set(tv.identify_row(event.y))    
    
    def bUp_Shift(self, event):
        pass
    
    
    def bMove(self, event):
        tv = event.widget
        moveto = tv.index(tv.identify_row(event.y))    
        for s in tv.selection():
            tv.move(s, '', moveto)




if __name__ == '__main__':
    #Tkインスタンスを作成し、app変数に格納する
    app  = Tk()
    
    
    #フレームを作成する
    frame = Main(app)
    
    # 格納したTkインスタンスのmainloopで画面を起こす
    app.mainloop()

# %%
