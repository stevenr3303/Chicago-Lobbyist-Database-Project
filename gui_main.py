#!/usr/bin/env python3
"""
Simple Tkinter GUI frontend for the Chicago Lobbyist Database Project.

This captures output that was previously printed to the console and
displays it in a scrollable Text widget. User inputs are requested via
modal dialogs so the existing objecttier functions can be reused.

Run this file to open the GUI.
"""
import sqlite3
import sys
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, filedialog
from tkinter import ttk
import tkinter.font as tkfont
import objecttier


class GuiApp:
    def __init__(self, root):
        self.root = root
        root.title("Chicago Lobbyist Database")

        # Apply a ttk style for a cleaner look
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass

        # Fonts
        self.mono_font = tkfont.nametofont('TkFixedFont')
        self.mono_font.configure(size=10)
        self.header_font = tkfont.nametofont('TkHeadingFont') if 'TkHeadingFont' in tkfont.names() else tkfont.Font(size=11, weight='bold')

        # Top-level layout frames
        toolbar = ttk.Frame(root, padding=(6, 6))
        toolbar.grid(row=0, column=0, sticky='ew')

        content = ttk.Frame(root, padding=(6, 0, 6, 6))
        content.grid(row=1, column=0, sticky='nsew')

        # Output area (replaces printed output)
        self.output = scrolledtext.ScrolledText(content, wrap=tk.WORD, width=100, height=28, font=self.mono_font)
        self.output.grid(row=0, column=0, columnspan=4, padx=0, pady=(0, 6), sticky="nsew")
        self.output.configure(state=tk.DISABLED)

        # Small writer to capture prints from other modules and send them to GUI
        class _GuiWriter:
            def __init__(self, write_fn):
                self._write_fn = write_fn
            def write(self, data):
                # Avoid inserting empty strings
                if data:
                    # write without adding extra newline (gui_print handles ends)
                    self._write_fn(data, end='')
            def flush(self):
                pass

        # Buttons for commands 1-5 and General Stats (toolbar)
        btn_general = ttk.Button(toolbar, text="General Stats", command=self.general_stats)
        btn_cmd1 = ttk.Button(toolbar, text="1: Find Lobbyists", command=self.command1)
        btn_cmd2 = ttk.Button(toolbar, text="2: Lobbyist Details", command=self.command2)
        btn_cmd3 = ttk.Button(toolbar, text="3: Top N Lobbyists", command=self.command3)
        btn_cmd4 = ttk.Button(toolbar, text="4: Register Year", command=self.command4)
        btn_cmd5 = ttk.Button(toolbar, text="5: Set Salutation", command=self.command5)
        btn_clear = ttk.Button(toolbar, text="Clear Output", command=self.clear_output)
        btn_save = ttk.Button(toolbar, text="Save Output", command=self.save_output)
        btn_exit = ttk.Button(toolbar, text="Exit", command=self.on_exit)

        # Arrange toolbar buttons
        for i, w in enumerate((btn_general, btn_cmd1, btn_cmd2, btn_cmd3, btn_cmd4, btn_cmd5, btn_clear, btn_save, btn_exit)):
            w.grid(row=0, column=i, padx=4)

        # Make grid expand
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Status bar
        self.status = ttk.Label(root, text='Ready', relief='sunken', anchor='w')
        self.status.grid(row=2, column=0, sticky='ew')

        # Menubar
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Save Output', accelerator='Ctrl+S', command=self.save_output)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', accelerator='Ctrl+Q', command=self.on_exit)
        menubar.add_cascade(label='File', menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='About', command=self.show_about)
        menubar.add_cascade(label='Help', menu=help_menu)
        root.config(menu=menubar)

        # Keyboard shortcuts
        root.bind_all('<Control-s>', lambda e: self.save_output())
        root.bind_all('<Control-q>', lambda e: self.on_exit())

        # DB connection
        try:
            self.dbConn = sqlite3.connect('Chicago_Lobbyists.db')
        except Exception as e:
            messagebox.showerror("DB Error", f"Unable to open database: {e}")
            root.quit()

        # Welcome message
        # Redirect global stdout/stderr to GUI so existing print() calls show up
        # in the GUI output area without changing other modules.
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr
        sys.stdout = _GuiWriter(self.gui_print)
        sys.stderr = _GuiWriter(self.gui_print)

        self.gui_print('** Welcome to the Chicago Lobbyist Database Application (GUI) **')
        self.gui_print('')
        self.general_stats()

        # Restore stdout/stderr on close
        self.root.protocol('WM_DELETE_WINDOW', self.on_exit)

    # utility to append text to GUI output
    def gui_print(self, *args, sep=' ', end='\n'):
        text = sep.join(map(str, args)) + end
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def clear_output(self):
        self.output.configure(state=tk.NORMAL)
        self.output.delete('1.0', tk.END)
        self.output.configure(state=tk.DISABLED)
        self.set_status('Output cleared')

    def save_output(self):
        try:
            initial = 'lobbyists_output.txt'
            path = filedialog.asksaveasfilename(defaultextension='.txt', initialfile=initial, filetypes=[('Text', '*.txt'), ('All files', '*.*')])
            if not path:
                return
            text = self.output.get('1.0', tk.END)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            self.set_status(f'Saved output to {path}')
        except Exception as e:
            messagebox.showerror('Save Error', f'Unable to save file: {e}')
            self.set_status('Save failed')

    def set_status(self, msg):
        try:
            self.status.config(text=msg)
        except Exception:
            pass

    # wrappers for inputs using modal dialogs
    def gui_input(self, prompt, title="Input"):
        return simpledialog.askstring(title, prompt, parent=self.root)

    # Command implementations (mirror behavior from main.py)
    def general_stats(self):
        try:
            self.gui_print('General Statistics:')
            self.gui_print('  Number of Lobbyists: {:,}'.format(objecttier.num_lobbyists(self.dbConn)))
            self.gui_print('  Number of Employers: {:,}'.format(objecttier.num_employers(self.dbConn)))
            self.gui_print('  Number of Clients: {:,}'.format(objecttier.num_clients(self.dbConn)))
            self.gui_print('')
        except Exception as e:
            self.gui_print('Error retrieving general stats:', e)

    def command1(self):
        lob_name = self.gui_input('Enter lobbyist name (first or last, wildcards _ and % supported):')
        if lob_name is None:
            return
        self.gui_print('')
        try:
            lobbyists = objecttier.get_lobbyists(self.dbConn, lob_name)
            if len(lobbyists) > 100:
                self.gui_print('Number of Lobbyists found:', len(lobbyists))
                self.gui_print('')
                self.gui_print('There are too many lobbyists to display, please narrow your search and try again...')
            else:
                self.gui_print('Number of Lobbyists found:', len(lobbyists))
                if len(lobbyists) > 0:
                    self.gui_print('')
                    for l in lobbyists:
                        self.gui_print(l.Lobbyist_ID, ':', l.First_Name, l.Last_Name, 'Phone:', l.Phone)
        except Exception as e:
            self.gui_print('Error:', e)
            self.set_status('Error during search')

    def command2(self):
        lob_id = self.gui_input('Enter Lobbyist ID:')
        if lob_id is None:
            return
        self.gui_print('')
        try:
            ld = objecttier.get_lobbyist_details(self.dbConn, lob_id)
            if ld is None:
                self.gui_print('No lobbyist with that ID was found.')
            else:
                self.gui_print(ld.Lobbyist_ID, ':')
                self.gui_print(' Full Name:', ld.Salutation, ld.First_Name, ld.Middle_Initial, ld.Last_Name, ld.Suffix)
                self.gui_print(' Address:', ld.Address_1, ld.Address_2, ',', ld.City, ',', ld.State_Initial, ld.Zip_Code, ld.Country)
                self.gui_print(' Email:', ld.Email)
                self.gui_print(' Phone:', ld.Phone)
                self.gui_print(' Fax:', ld.Fax)
                self.gui_print(' Years Registered:', ', '.join(map(str, ld.Years_Registered)))
                self.gui_print(' Employers:', ', '.join(ld.Employers))
                self.gui_print(' Total Compensation: ${:,.2f}'.format(ld.Total_Compensation))
        except Exception as e:
            self.gui_print('Error:', e)
            self.set_status('Error retrieving details')

    def command3(self):
        n = self.gui_input('Enter the value of N:')
        if n is None:
            return
        try:
            if int(n) <= 0:
                self.gui_print('Please enter a positive value for N...')
                return
        except Exception:
            self.gui_print('Please enter a valid integer for N...')
            return
        year = self.gui_input('Enter the year:')
        if year is None:
            return
        try:
            lobbyists = objecttier.get_top_N_lobbyists(self.dbConn, int(n), year)
            if lobbyists == []:
                return
            self.gui_print('')
            for idx, l in enumerate(lobbyists):
                self.gui_print(f"{idx + 1} . {l.First_Name} {l.Last_Name}")
                self.gui_print(' Phone:', l.Phone)
                self.gui_print(' Total Compensation: ${:,.2f}'.format(l.Total_Compensation))
                self.gui_print(' Clients:', ', '.join(l.Clients), end='\n')
                if idx < len(lobbyists) - 1:
                    self.gui_print('')
            self.gui_print('')
        except Exception as e:
            self.gui_print('Error:', e)
            self.set_status('Error retrieving top N')

    def command4(self):
        year = self.gui_input('Enter year:')
        if year is None:
            return
        lob_id = self.gui_input('Enter the lobbyist ID:')
        if lob_id is None:
            return
        try:
            res = objecttier.add_lobbyist_year(self.dbConn, lob_id, year)
            self.gui_print('')
            if res > 0:
                self.gui_print('Lobbyist successfully registered.')
            else:
                self.gui_print('No lobbyist with that ID was found.')
        except Exception as e:
            self.gui_print('Error:', e)
            self.set_status('Error registering year')

    def command5(self):
        lob_id = self.gui_input('Enter the lobbyist ID:')
        if lob_id is None:
            return
        sal = self.gui_input('Enter the salutation:')
        if sal is None:
            return
        self.gui_print('')
        try:
            res = objecttier.set_salutation(self.dbConn, lob_id, sal)
            if res > 0:
                self.gui_print('Salutation successfully set.')
            else:
                self.gui_print('No lobbyist with that ID was found.')
        except Exception as e:
            self.gui_print('Error:', e)
            self.set_status('Error setting salutation')

    def show_about(self):
        messagebox.showinfo('About', 'Chicago Lobbyist Database GUI\nImproved UI')

    def on_exit(self):
        # Restore stdout/stderr
        try:
            sys.stdout = self._orig_stdout
            sys.stderr = self._orig_stderr
        except Exception:
            pass
        try:
            if hasattr(self, 'dbConn'):
                self.dbConn.close()
        except Exception:
            pass
        self.root.quit()


def main():
    root = tk.Tk()
    app = GuiApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
