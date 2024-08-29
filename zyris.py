import tkinter as tk
from tkinter import messagebox, colorchooser, simpledialog
import json

# Funktion zum Laden der Mapping-Daten
def load_mapping():
    try:
        with open('gam.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Funktion zum Übersetzen
def translate(text, mapping):
    return ''.join(mapping.get(char, char) for char in text)

# Funktion zum Rückübersetzen
def reverse_translate(text, reverse_mapping):
    return ''.join(reverse_mapping.get(char, char) for char in text)

# Funktion zum Verarbeiten der Benutzereingabe
def on_translate():
    input_text = input_textbox.get("1.0", tk.END).strip()
    if reverse_var.get():
        reverse_mapping = {v: k for k, v in mapping.items()}
        output_text = reverse_translate(input_text, reverse_mapping)
    else:
        output_text = translate(input_text, mapping)
    
    output_textbox.config(state=tk.NORMAL)
    output_textbox.delete("1.0", tk.END)
    output_textbox.insert(tk.END, output_text)
    output_textbox.config(state=tk.DISABLED)

# Funktion zum Kopieren des Textes
def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_textbox.get("1.0", tk.END).strip())

# Funktion zum Einfügen des Textes
def paste_text():
    input_textbox.delete("1.0", tk.END)
    input_textbox.insert(tk.END, root.clipboard_get())

# Funktion zum Speichern der Änderungen
def save_mapping():
    try:
        with open('gam.json', 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Info", "Mapping gespeichert.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Speichern der Datei: {e}")

# Funktion zum Hinzufügen eines neuen Eintrags
def add_entry():
    key = simpledialog.askstring("Neuer Eintrag", "Geben Sie den Buchstaben ein:")
    if key and key not in mapping:
        value = simpledialog.askstring("Neuer Eintrag", "Geben Sie das Symbol ein:")
        if value:
            mapping[key] = value
            update_letter_editor()
            save_mapping()

# Funktion zum Aktualisieren des Buchstaben-Editors
def update_letter_editor():
    if 'letter_editor_window' in globals() and letter_editor_window:
        for widget in letter_editor_window.winfo_children():
            widget.destroy()
    
        tk.Label(letter_editor_window, text="Bearbeiten Sie die Buchstaben-Zuordnungen:", font=("Helvetica", 12)).pack(pady=10)
        
        canvas = tk.Canvas(letter_editor_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(letter_editor_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        editor_frame = tk.Frame(canvas)
        
        canvas.create_window((0, 0), window=editor_frame, anchor='nw')
        
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        
        editor_frame.bind('<Configure>', on_configure)
        
        buchstaben_entries = []
        for key, value in mapping.items():
            frame = tk.Frame(editor_frame)
            frame.pack(pady=5, fill=tk.X)
            key_entry = tk.Entry(frame, width=10)
            key_entry.insert(tk.END, key)
            key_entry.grid(row=0, column=0, padx=5)
            value_entry = tk.Entry(frame, width=40)
            value_entry.insert(tk.END, value)
            value_entry.grid(row=0, column=1, padx=5)
            buchstaben_entries.append((key_entry, value_entry))
        
        def save_letter_editor():
            for key_entry, value_entry in buchstaben_entries:
                key = key_entry.get()
                value = value_entry.get()
                if key and value:
                    mapping[key] = value
            save_mapping()
            letter_editor_window.destroy()
        
        save_button = tk.Button(letter_editor_window, text="Speichern", command=save_letter_editor)
        save_button.pack(pady=10)
        
        add_button = tk.Button(letter_editor_window, text="+ Hinzufügen", command=add_entry)
        add_button.pack(pady=10)
    else:
        messagebox.showerror("Fehler", "Der Buchstaben-Editor ist nicht geöffnet.")

# Funktion zum Öffnen des Buchstaben-Editors
def open_letter_editor():
    global letter_editor_window
    letter_editor_window = tk.Toplevel(settings_window)
    letter_editor_window.title("Buchstaben-Editor")
    letter_editor_window.geometry("600x400")
    update_letter_editor()

# Funktion zum Öffnen des Einstellungen-Fensters
def open_settings():
    global settings_window
    settings_window = tk.Toplevel(root)
    settings_window.title("Einstellungen")
    settings_window.geometry("600x400")

    def choose_bg_color():
        color = colorchooser.askcolor()[1]
        if color:
            settings_window.configure(bg=color)
            color_display_bg.config(bg=color)
            root.configure(bg=color)
            input_textbox.configure(bg=color)
            output_textbox.configure(bg=color)

    def choose_text_color():
        color = colorchooser.askcolor()[1]
        if color:
            input_textbox.configure(fg=color)
            output_textbox.configure(fg=color)
            color_display_text.config(fg=color)

    def choose_button_color():
        color = colorchooser.askcolor()[1]
        if color:
            translate_button.configure(bg=color)
            settings_button.configure(bg=color)
            color_display_button.config(bg=color)

    def choose_entry_color():
        color = colorchooser.askcolor()[1]
        if color:
            input_textbox.configure(bg=color)
            output_textbox.configure(bg=color)
            color_display_entry.config(bg=color)

    # Farben anzeigen
    tk.Label(settings_window, text="Farben anzeigen:", font=("Helvetica", 12)).pack(pady=10)

    color_frame = tk.Frame(settings_window)
    color_frame.pack(pady=10)

    tk.Label(color_frame, text="Hintergrundfarbe:").pack(side=tk.LEFT, padx=5)
    color_display_bg = tk.Label(color_frame, text=" ", width=10, bg="gray")
    color_display_bg.pack(side=tk.LEFT, padx=5)
    bg_color_button = tk.Button(color_frame, text="Ändern", command=choose_bg_color)
    bg_color_button.pack(side=tk.LEFT, padx=5)

    tk.Label(color_frame, text="Textfarbe:").pack(side=tk.LEFT, padx=5)
    color_display_text = tk.Label(color_frame, text=" ", width=10, fg="white", bg="black")
    color_display_text.pack(side=tk.LEFT, padx=5)
    text_color_button = tk.Button(color_frame, text="Ändern", command=choose_text_color)
    text_color_button.pack(side=tk.LEFT, padx=5)

    tk.Label(color_frame, text="Buttonfarbe:").pack(side=tk.LEFT, padx=5)
    color_display_button = tk.Label(color_frame, text=" ", width=10, bg="#8a2be2")
    color_display_button.pack(side=tk.LEFT, padx=5)
    button_color_button = tk.Button(color_frame, text="Ändern", command=choose_button_color)
    button_color_button.pack(side=tk.LEFT, padx=5)

    tk.Label(color_frame, text="Textfeldfarbe:").pack(side=tk.LEFT, padx=5)
    color_display_entry = tk.Label(color_frame, text=" ", width=10, bg="#333")
    color_display_entry.pack(side=tk.LEFT, padx=5)
    entry_color_button = tk.Button(color_frame, text="Ändern", command=choose_entry_color)
    entry_color_button.pack(side=tk.LEFT, padx=5)

    # Button zum Öffnen des Buchstaben-Editors
    open_letter_editor_button = tk.Button(settings_window, text="Buchstaben-Editor öffnen", command=open_letter_editor)
    open_letter_editor_button.pack(pady=10)

# GUI-Setup
root = tk.Tk()
root.title("Galactic Alphabet Übersetzer")
root.geometry("600x500")
root.configure(bg="#2e2e2e")

mapping = load_mapping()

# Eingabe-Textfeld
tk.Label(root, text="Eingabe:", bg="#2e2e2e", fg="white").pack(pady=5)
input_textbox = tk.Text(root, height=10, width=50, bg="#333", fg="white", bd=0, highlightthickness=1, highlightcolor="#8a2be2")
input_textbox.pack(pady=5)

# Ausgabe-Textfeld
tk.Label(root, text="Übersetzung:", bg="#2e2e2e", fg="white").pack(pady=5)
output_textbox = tk.Text(root, height=10, width=50, bg="#333", fg="white", state=tk.DISABLED, bd=0, highlightthickness=1, highlightcolor="#8a2be2")
output_textbox.pack(pady=5)

# Checkbutton für zweiseitige Übersetzung
reverse_var = tk.BooleanVar()
reverse_checkbutton = tk.Checkbutton(root, text="Rückübersetzung", variable=reverse_var, bg="#2e2e2e", fg="white", selectcolor="#333", activebackground="#333")
reverse_checkbutton.pack(pady=5)

# Übersetzungs-Button
translate_button = tk.Button(root, text="Übersetzen", command=on_translate, bg="#8a2be2", fg="white", bd=0, padx=10, pady=5)
translate_button.pack(pady=10)

# Kopieren-Button
copy_button = tk.Button(root, text="Kopieren", command=copy_text, bg="#8a2be2", fg="white", bd=0, padx=10, pady=5)
copy_button.pack(side=tk.LEFT, padx=10, pady=10)

# Einfügen-Button
paste_button = tk.Button(root, text="Einfügen", command=paste_text, bg="#8a2be2", fg="white", bd=0, padx=10, pady=5)
paste_button.pack(side=tk.LEFT, padx=10, pady=10)

# Einstellungen-Button
settings_button = tk.Button(root, text="Einstellungen", command=open_settings, bg="#8a2be2", fg="white", bd=0, padx=10, pady=5)
settings_button.pack(side=tk.LEFT, padx=10, pady=10)

root.mainloop()
