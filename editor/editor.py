
import tkinter as tk
import tkinter.filedialog as filedialog
import hashlib

from .dialogs import FindDlg, ReplaceDlg
from .symbolic import Sym

COLOR_NORM = 'white'
COLOR_WARN = 'yellow'
INIT_POW   = True
INIT_EVAL  = False

class Editor:
  """Create the main window"""

  def __init__(self, root):
    self.root = root
    # symbolical operations
    self.sym = Sym()
    self.sym.simpParse(INIT_EVAL)
    self.sym.powXOR(INIT_POW)
    # editor
    self.editor = tk.Frame(root, width=600, height=400)
    self.editor.grid(row=1, column=0, sticky='nsew')
    self.textEditor(self.editor)
    # bar
    self.bar = tk.Frame(root) 
    self.bar.grid(row=0, column=0, sticky='we') 
    self.menuFile(self.bar)
    self.menuEdit(self.bar)
    self.menuSearch(self.bar)
    self.menuSympy(self.bar)
    self.c_menu = self.createSympyMenu(self.text)
    self.text.bind('<ButtonRelease-3>', self.callContext)
    # status
    self.statusVar = tk.StringVar()
    self.status = tk.Label(root, textvariable=self.statusVar, bg=COLOR_NORM, relief='sunken')
    self.status.grid(row=2, column=0, sticky='nsew')
    # evaluate
    self.editor_name = 'TermIt v.0.0'
    self.text.focus_set()
    self.root.title(self.editor_name)
    self.root.mainloop()

  def menuFile(self, frame):
    """Define elements of the 'File' menu"""
    btn = tk.Menubutton(frame, text='Files', underline=0)
    btn.grid(row=0, column=0, sticky='w')
    menu = tk.Menu(btn, tearoff=0)
    menu.add_command(label='New  (Ctrl+N)', command=lambda: self.fileNew(1))
    menu.add_command(label='Open (Ctrl+O)', command=lambda: self.fileOpen(1))
    menu.add_command(label='Save (Ctrl+S)', command=lambda: self.fileSave(1))
    menu.add_command(label='SaveAs', command=lambda: self.fileSaveAs(1))
    menu.add_separator()
    menu.add_command(label='Quit (Ctrl+Q)', command=lambda: self.fileQuit(1))
    btn.configure(menu=menu)
    self.root.bind("<Control-n>", self.fileNew)
    self.root.bind("<Control-o>", self.fileOpen)
    self.root.bind("<Control-s>", self.fileSave)
    self.root.bind("<Control-q>", self.fileQuit)

  def menuSearch(self, frame):
    """Define elements of the 'Search' menu"""
    btn = tk.Menubutton(frame, text='Search', underline=0)
    btn.grid(row=0, column=2, sticky='w')
    menu = tk.Menu(btn, tearoff=0)
    menu.add_command(label='Find (Ctrl+F)', command=lambda: self.searchFind(1))
    menu.add_command(label='Find next (Ctrl+G)', command=lambda: self.searchNext(1))
    menu.add_command(label='Find and Replace (Ctrl+R)', command=lambda: self.searchFindReplace(1))
    btn.configure(menu=menu)
    self.text.bind("<Control-f>", self.searchFind)
    self.text.bind("<Control-g>", self.searchNext)
    self.text.bind("<Control-r>", self.searchFindReplace)

  def menuEdit(self, frame):
    """Define elements of the 'Edit' menu"""
    btn = tk.Menubutton(frame, text='Edit', underline=0)
    btn.grid(row=0, column=1, sticky='w')
    menu = tk.Menu(btn, tearoff=0)
    menu.add_command(label='Undo ', command=self.text.edit_undo)
    menu.add_command(label='Redo ', command=self.text.edit_redo)
    menu.add_separator()
    menu.add_command(label='Cut (Ctrl+X)', command=lambda: self.text.event_generate('<<Cut>>'))
    menu.add_command(label='Copy (Ctrl+C)', command=lambda: self.text.event_generate('<<Copy>>'))
    menu.add_command(label='Paste (Ctrl+V)', command=lambda: self.text.event_generate('<<Paste>>'))
    btn.configure(menu=menu)

  def menuSympy(self, frame):
    """Define elements of the 'Simpy' menu"""
    btn = tk.Menubutton(frame, text='Sympy', underline=0)
    btn.grid(row=0, column=3, sticky='w')
    btn.configure(menu=self.createSympyMenu(btn))

  def createSympyMenu(self, frame):
    """List of symbolical operations"""
    menu = tk.Menu(frame, tearoff=0)
    # base operations
    basemenu = tk.Menu(menu, tearoff=0)
    basemenu.add_command(label='Expand', command=lambda: self.symExpand(1))
    basemenu.add_command(label='Factor', command=lambda: self.symFactor(1))
    basemenu.add_command(label='Simplify', command=lambda: self.symSimplify(1))
    menu.add_cascade(label='Base..', menu=basemenu)
    # power
    powmenu = tk.Menu(menu, tearoff=0)
    powmenu.add_command(label='Expand Exp', command=lambda: self.symPowExpandExp(1))
    powmenu.add_command(label='Expand Base', command=lambda: self.symPowExpandBase(1))
    powmenu.add_command(label='Simplify', command=lambda: self.symPowSimplify(1))
    menu.add_cascade(label='Power..', menu=powmenu)
    # trigonometry
    trigmenu = tk.Menu(menu, tearoff=0)
    trigmenu.add_command(label='Expand', command=lambda: self.symTrigExpand(1))
    trigmenu.add_command(label='Simplify', command=lambda: self.symTrigSimp(1))
    menu.add_cascade(label='Trig..', menu=trigmenu)
    # settings
    setmenu = tk.Menu(menu, tearoff=0)
    self.cb_eval = tk.BooleanVar()
    self.cb_eval.set(INIT_EVAL)
    setmenu.add_checkbutton(label='Evaluate', variable=self.cb_eval, onvalue=True, 
        offvalue=False, command=lambda: self.sym.simpParse(self.cb_eval.get()))
    self.cb_pow = tk.BooleanVar()
    self.cb_pow.set(INIT_POW)
    setmenu.add_checkbutton(label='Power as ^', variable=self.cb_pow, onvalue=True,
        offvalue=False, command=lambda: self.sym.powXOR(self.cb_pow.get()))
    menu.add_cascade(label='Settings..', menu=setmenu)
    return menu

  def textEditor(self, frame):
    """Create text editor widget"""
    self.text = tk.Text(frame, wrap='none', undo=True)
    vscroll = tk.Scrollbar(frame, command=self.text.yview, orient='vertical')
    hscroll = tk.Scrollbar(frame, command=self.text.xview, orient='horizontal')
    self.text.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)
    self.text.grid(row=0, column=0, sticky='nsew')
    vscroll.grid(row=0, column=1, sticky='ns')
    hscroll.grid(row=1, column=0, sticky='ew')
    self.hashcode = self.getHash()

  def getHash(self):
    """Find hash code for the text"""
    txt = self.text.get('1.0', 'end') 
    return hashlib.md5(txt.encode()).hexdigest()

  def checkChanges(self, ev, msg):
    """Provide menu to save changes if need"""
    if self.hashcode != self.getHash():
      if tk.messagebox.askyesno(msg, "Save changes?"):
        self.fileSave()

  def fileNew(self, ev):
    """Command to create new empty file"""
    self.checkChanges(ev, "New file")
    self.text.delete('1.0', 'end')
    self.root.title(self.editor_name)
    self.hashcode = self.getHash()

  def fileOpen(self, ev):
    """Command to open an existing file"""
    self.checkChanges(ev, "Open file")
    name = filedialog.Open(self.root, filetypes = [('All files', '*')]).show()
    if type(name) != str or name == '':
      return
    self.text.delete('1.0', 'end')
    self.text.insert('1.0', open(name, 'rt').read())
    self.root.title(name)
    self.hashcode = self.getHash()

  def fileSaveAs(self, ev):
    """Command to save the text as a new file"""
    name = filedialog.SaveAs(self.root, filetypes = [('All files','*')]).show()
    if name == '':
      return
    open(name, 'wt').write(self.text.get('1.0', 'end'))
    self.root.title(name)
    self.hashcode = self.getHash()

  def fileSave(self, ev):
    """Command to save changes in the text"""
    if self.hashcode == self.getHash(): 
      return    # no changes
    name = self.root.title()
    if name == self.editor_name:
      self.fileSaveAs(ev)
    else:
      open(name, 'wt').write(self.text.get('1.0', 'end'))
      self.root.title(name)
      self.hashcode = self.getHash()

  def fileQuit(self, ev):
    """Command to quit the program"""
    self.checkChanges(ev, "Quit")
    self.root.destroy()

  def searchFind(self, ev):
    """Command to open menu for the text searching"""
    sel = ""
    if self.text.tag_ranges('sel'):
      sel = self.text.selection_get()
    find = FindDlg(self.root, "Find text", sel)
    if find.pressok and find.text:
      self.text.selection_clear()
      i_from = self.text.search(find.text, 'insert + 1 chars', nocase=find.nocase)
      self.text.mark_set('insert', i_from)
      i_to = 'insert + %d chars' % len(find.text)
      self.text.tag_add('sel', i_from, i_to)
    return 'break'

  def searchNext(self, ev):
    """Command to find the highlighted text"""
    # TODO: save state
    if self.text.tag_ranges('sel'):
      sel = self.text.selection_get()
      self.text.selection_clear()
      i_from = self.text.search(sel, 'insert + 1 chars')
      self.text.mark_set('insert', i_from)
      i_to = 'insert + %d chars' % len(sel)
      self.text.tag_add('sel', i_from, i_to)
    return 'break'

  def searchFindReplace(self, ev):
    """Command to open menu to find and replace the text"""
    # TODO: save state
    dlg = ReplaceDlg(self.root, "Find and replace", "", "") 
    if dlg.pressok and dlg.find and dlg.replace:
      self.text.selection_clear()
      i_from = '1.0' if dlg.all else 'insert + 1 chars'
      while True:
        # find
        i_from = self.text.search(dlg.find, i_from, nocase=dlg.nocase)
        if not i_from: break
        i_to = '% s+% dc' % (i_from, len(dlg.find))
        # replace
        self.text.delete(i_from, i_to)
        self.text.insert(i_from, dlg.replace)
        # break if need
        if dlg.all:
          i_from = '% s+% dc' % (i_from, len(dlg.replace))
        else:
          break
  
  def callContext(self, ev):
    """Call context menu"""
    self.c_menu.post(ev.x_root, ev.y_root)

  def INFO(self, msg):
    """Update status label in normal mode"""
    self.status['bg'] = COLOR_NORM
    self.statusVar.set(msg)

  def WARN(self, msg):
    """Update status label in warning mode"""
    self.status['bg'] = COLOR_WARN
    self.statusVar.set(msg)

  def _call(self,fn):
    rng = self.text.tag_ranges('sel')
    if not rng:
      # whole line
      rng = (self.text.index('insert linestart'), self.text.index('insert lineend'))
    s = self.text.get(*rng)
    # execute 
    ok, snext = fn(s)
    if ok:
      self.text.delete(*rng)
      self.text.insert(rng[0], snext+' ')  # fix it
      self.INFO("Done!")
    else:
      self.WARN(snext)

  def symExpand(self, ev):
    return self._call(self.sym.expand)

  def symFactor(self, ev):
    return self._call(self.sym.factor)

  def symSimplify(self, ev):
    return self._call(self.sym.simplify)

  def symPowExpandExp(self, ev):
    return self._call(self.sym.powExpandExp)

  def symPowExpandBase(self, ev):
    return self._call(self.sym.powExpandBase)

  def symPowSimplify(self, ev):
    return self._call(self.sym.powSimp)

  def symTrigExpand(self, ev):
    return self._call(self.sym.trigExpand)

  def symTrigSimp(self, ev):
    return self._call(self.sym.trigSimp)
