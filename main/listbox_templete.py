#%%
import sys
import tkinter as tk
import pandas as pd
import tkinter.ttk as ttk

class ListboxSampleApp(ttk.Frame):
    def __init__(self, app, team = 'Team_田中'):
        super().__init__(app)
        self.pack()
        
        self.team = team
        self.df_new = pd.read_csv("../data/test_1.csv", encoding="SHIFT-JIS", usecols=[team, '報告者'])
        self.df_old = pd.read_csv("../data/test_2.csv", encoding="SHIFT-JIS", usecols=[team, '報告者'])
        
        # 承認者のリストボックスの作成
        self.build_shoninsha_listbox()
        
        # 報告者のリストボックスの作成
        #self.build_hokokusha_listbox()
        
        # ボタンの作成
        button = ttk.Button(app,text = "更新" ,command=self.selectItem)
        button.pack()
        
        
        # アクションの設定
        self.new_shoninsha.bind('<Button-1>', self.getState, add='+')
        self.new_shoninsha.bind('<Button-1>', self.setCurrent, add='+')
        self.new_shoninsha.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None
        self.curState = None
    
    def setCurrent(self, event):
        self.event = event
        ''' gets the current index of the clicked item in the listbox '''
        self.curIndex = self.nearest(event.y)
        
    def getState(self, event):
        ''' checks if the clicked item in listbox is selected '''
        i = self.nearest(event.y)
        self.curState = self.selection_includes(i)
    def shiftSelection(self, event):
        ''' shifts item up or down in listbox '''
        i = self.nearest(event.y)
        if self.curState == 1:
            self.selection_set(self.curIndex)
        else:
            self.selection_clear(self.curIndex)
        if i < self.curIndex:
            # Moves up
            x = self.get(i)
            selected = self.selection_includes(i)
            self.delete(i)
            self.insert(i+1, x)
            if selected:
                self.selection_set(i+1)
            self.curIndex = i
        elif i > self.curIndex:
            # Moves down
            x = self.get(i)
            selected = self.selection_includes(i)
            self.delete(i)
            self.insert(i-1, x)
            if selected:
                self.selection_set(i-1)
            self.curIndex = i
    
    def build_shoninsha_listbox(self):
        
        # 新しいverの承認者
        self.new_shoninsha_list = self.df_new[self.team].to_list()
        new_shoninsha = tk.StringVar(value=self.new_shoninsha_list)
        self.new_shoninsha  =  tk.Listbox(app, listvariable=new_shoninsha, height=5,selectmode= tk.MULTIPLE)
        self.new_shoninsha.pack(side='left')
        
        # 古いverの承認者
        self.old_shoninsha_list = self.df_old[self.team].to_list()
        old_shoninsha = tk.StringVar(value=self.old_shoninsha_list)
        self.old_shoninsha  =  tk.Listbox(app, listvariable=old_shoninsha, height=5,selectmode= tk.BROWSE)
        self.old_shoninsha.pack(side='left')
    
    
    
    def build_hokokusha_listbox(self):
        
        # 新しいverの報告者
        self.new_hokokusha_list = self.df_new["報告者"].to_list()
        new_hokokusha = tk.StringVar(value=self.new_hokokusha_list)
        self.new_hokokusha  =  tk.Listbox(app, listvariable=new_hokokusha, height=5, selectmode= tk.MULTIPLE)
        self.new_hokokusha.pack(side='left')
        
        # 古いverの報告者
        self.old_hokokusha_list = self.df_old["報告者"].to_list()
        old_hokokusha = tk.StringVar(value=self.old_hokokusha_list)
        self.old_hokokusha  =  tk.Listbox(app, listvariable=old_hokokusha, height=5, selectmode= tk.BROWSE)
        self.old_hokokusha.pack(side='left')
    
    
    def selectItem(self):
        # 選択されている数値インデックスを含むリストを取得
        itemIdxList_shoninsha =  self.new_shoninsha.curselection()
        #itemIdxList_hokokusha =  self.new_hokokusha.curselection().curselection()

        for i in reversed(itemIdxList_shoninsha):
            self.new_shoninsha.delete(i)
                
        #for i in reversed(itemIdxList_hokokusha):
            #self.new_hokokusha.delete(i)
    
    
    
    def Data_to_display_func(self):
            
        # 新データと旧データの差分を観測
        self.check_differences()
        
        
        # 更新
        for i in range(len(self.new_df)):
                self.new_shoninsha.insert("", "end", values=tuple([self.new_df.iloc[i, j] for j in range(len(self.new_df.columns))]))
        
        # 削除した人物も記録
        if len(self.checked_for_delete_list) == 0:
            pass
        else:
            for tmp_dict in self.checked_for_delete_list:
                self.tree_trashed.insert("", "end", values = tuple(tmp_dict.values()))
    
    
    
    
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
    
    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)
    
    
    
    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i



if __name__ == '__main__':
    #Tkインスタンスを作成し、app変数に格納する
    app  = tk.Tk()
    #縦幅400横幅200に画面サイズを変更します。
    app.geometry("400x200")
    #タイトルを指定
    app.title("Listbox SelectMode Multi Sample Program")
    # #フレームを作成する
    frame = ListboxSampleApp(app)
    # 格納したTkインスタンスのmainloopで画面を起こす
    app.mainloop()
# %%
