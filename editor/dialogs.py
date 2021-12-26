# Customised dialogs

import tkinter as tk
import tkinter.simpledialog 

class FindDlg(tk.simpledialog.Dialog):
  """Create dialog to find the text"""

  def __init__(self, parent, title, txt):
    self.text = txt
    self.nocase = 0
    self.pressok = True
    super().__init__(parent, title)

  def body(self, frame):
    """Window structure"""
    self.entry = tk.Entry(frame, width=20)
    self.entry.insert('1', self.text)
    self.entry.pack()
    self.var = tk.IntVar()
    self.check = tk.Checkbutton(frame, text="Case insensitive", variable=self.var, onvalue=1, offvalue=0)
    self.check.pack()

  def on_ok(self):
    """Button 'OK' action"""
    self.text = self.entry.get()
    self.nocase = self.var.get()
    self.destroy()

  def on_cancel(self):
    """Button 'Cancel' action"""
    self.pressok = False
    self.destroy()

  def buttonbox(self):
    """Buttons and bindings"""
    self.btn_ok = tk.Button(self, text='OK', width=5, command=self.on_ok)
    self.btn_ok.pack(side='left')
    self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.on_cancel)
    self.btn_cancel.pack(side='right')
    self.bind('<Return>', lambda ev: self.on_ok)
    self.bind('<Escape>', lambda ev: self.on_cancel)


class ReplaceDlg(tk.simpledialog.Dialog):
  """Create dialog to replace the found strings"""

  def __init__(self, parent, title, fnd, repl):
    self.find = fnd
    self.replace = repl
    self.nocase = 0
    self.all = 1
    self.pressok = True
    super().__init__(parent, title)

  def body(self, frame):
    """Window structure"""
    self.ent_find = tk.Entry(frame, width=20)
    self.ent_find.insert('1', self.find)
    self.ent_find.pack()
    self.ent_replace = tk.Entry(frame, width=20)
    self.ent_replace.insert('1', self.replace)
    self.ent_replace.pack()
    self.var_sens = tk.IntVar()
    self.var_all = tk.IntVar(value=1)
    self.check_sens = tk.Checkbutton(frame, text="Case insensitive", variable=self.var_sens, onvalue=1, offvalue=0)
    self.check_sens.pack()
    self.check_all = tk.Checkbutton(frame, text="Replace all", variable=self.var_all, onvalue=1, offvalue=0)
    self.check_all.pack()

  def on_ok(self):
    """Button 'OK' action"""
    self.find = self.ent_find.get()
    self.replace = self.ent_replace.get()
    self.nocase = self.var_sens.get()
    self.all = self.var_all.get()
    self.destroy()

  def on_cancel(self):
    """Button 'Cancel' action"""
    self.pressok = False
    self.destroy()

  def buttonbox(self):
    """Buttons and bindings"""
    self.btn_ok = tk.Button(self, text='OK', width=5, command=self.on_ok)
    self.btn_ok.pack(side='left')
    self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.on_cancel)
    self.btn_cancel.pack(side='right')
    self.bind('<Return>', lambda ev: self.on_ok)
    self.bind('<Escape>', lambda ev: self.on_cancel)

class GetParams(tk.simpledialog.Dialog):
  """Create dialog to get 1 or 2 parameters"""
  
  def __init__(self, parent, title, tips, defaults=('','')):
    self.tips = tips
    self.defaults = defaults
    self.pressok = True
    super().__init__(parent, title)

  def body(self, frame):
    """Window structure"""
    self.var1 = tk.StringVar(value=self.defaults[0])
    self.var2 = tk.StringVar(value=self.defaults[1])
    lbl1 = tk.Label(frame, text=self.tips[0])
    lbl1.pack()
    ent1 = tk.Entry(frame, textvariable=self.var1, width=18)
    ent1.pack()
    if len(self.tips) > 1:
      lbl2 = tk.Label(frame, text=self.tips[1])
      lbl2.pack()
      ent2 = tk.Entry(frame, textvariable=self.var2, width=18)
      ent2.pack()

  def on_ok(self):
    """Button 'OK' action"""
    self.v1 = self.var1.get()
    self.v2 = self.var2.get()
    self.destroy()

  def on_cancel(self):
    """Button 'Cancel' action"""
    self.pressok = False
    self.destroy()

  def buttonbox(self):
    """Buttons and bindings"""
    btn_ok = tk.Button(self, text='OK', width=5, command=self.on_ok)
    btn_ok.pack(side='left')
    btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.on_cancel)
    btn_cancel.pack(side='right')
    self.bind('<Return>', lambda ev: self.on_ok)
    self.bind('<Escape>', lambda ev: self.on_cancel)

