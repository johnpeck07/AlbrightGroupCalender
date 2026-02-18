import tkinter as tk
from tkinter import messagebox

# =========================
# User Class
# =========================
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.approved = False

    def request_access(self):
        if self.email.endswith("@albright.edu"):
            self.approved = True
            return True
        return False


# =========================
# Event Class
# =========================
class Event:
    def __init__(self, title, date, time, category, description):
        self.title = title
        self.date = date
        self.time = time
        self.category = category
        self.description = description

    def display(self):
        return f"{self.time} – {self.title} ({self.category})"


# =========================
# Calendar Class
# =========================
class Calendar:
    def __init__(self):
        self.events = []
        self.authorized_users = []

    def add_user(self, user):
        if user.approved:
            self.authorized_users.append(user)

    def add_event(self, user, event):
        if user in self.authorized_users:
            self.events.append(event)
            return True
        return False

    def delete_event(self, event):
        if event in self.events:
            self.events.remove(event)


# =========================
# GUI Application
# =========================
class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Albright Student Calendar")
        self.root.geometry("550x550")
        self.root.configure(bg="#000000")

        self.bg_color = "#000000"
        self.text_color = "#ffffff"
        self.accent_color = "#b30000"
        self.entry_bg = "#1a1a1a"

        self.calendar = Calendar()
        self.current_user = None
        self.display_map = {}  # maps listbox index → event

        self.build_login_screen()

    # ---------- Styling ----------
    def styled_label(self, text, size=12):
        return tk.Label(
            self.root,
            text=text,
            font=("Helvetica", size, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )

    def styled_entry(self):
        return tk.Entry(
            self.root,
            bg=self.entry_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat"
        )

    def styled_button(self, text, command):
        return tk.Button(
            self.root,
            text=text,
            command=command,
            bg=self.accent_color,
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            activebackground="#ff1a1a",
            padx=10,
            pady=5
        )

    # ---------- Screens ----------
    def build_login_screen(self):
        self.clear_screen()

        self.styled_label("Albright Student Calendar", 18).pack(pady=20)

        self.styled_label("Name").pack()
        self.name_entry = self.styled_entry()
        self.name_entry.pack(pady=5)

        self.styled_label("Email").pack()
        self.email_entry = self.styled_entry()
        self.email_entry.pack(pady=5)

        self.styled_button("Request Access", self.request_access).pack(pady=20)

    def request_access(self):
        user = User(self.name_entry.get(), self.email_entry.get())

        if user.request_access():
            self.calendar.add_user(user)
            self.current_user = user
            messagebox.showinfo("Success", "Access approved!")
            self.build_calendar_screen()
        else:
            messagebox.showerror("Denied", "Must use an @albright.edu email")

    def build_calendar_screen(self):
        self.clear_screen()

        self.styled_label(f"Welcome, {self.current_user.name}", 14).pack(pady=10)

        self.event_list = tk.Listbox(
            self.root,
            width=65,
            bg=self.entry_bg,
            fg=self.text_color,
            relief="flat",
            selectbackground="#b30000"
        )
        self.event_list.pack(pady=15)

        self.styled_button("Add Event", self.build_add_event_screen).pack(pady=5)
        self.styled_button("Delete Selected Event", self.delete_event).pack(pady=5)
        self.styled_button("Logout", self.build_login_screen).pack(pady=5)

        self.refresh_events()

    # ---------- Calendar View ----------
    def refresh_events(self):
        self.event_list.delete(0, tk.END)
        self.display_map.clear()

        # Group events by date
        events_by_date = {}
        for event in self.calendar.events:
            events_by_date.setdefault(event.date, []).append(event)

        index = 0
        for date in sorted(events_by_date):
            # Date header
            self.event_list.insert(tk.END, f"📅 {date}")
            self.event_list.itemconfig(index, fg="#ff4d4d")
            index += 1

            for event in events_by_date[date]:
                self.event_list.insert(tk.END, f"   {event.display()}")
                self.display_map[index] = event
                index += 1

            self.event_list.insert(tk.END, "")
            index += 1

    # ---------- Add Event ----------
    def build_add_event_screen(self):
        self.clear_screen()

        self.styled_label("Add New Event", 16).pack(pady=15)

        self.title_entry = self.labeled_entry("Title")
        self.date_entry = self.labeled_entry("Date (YYYY-MM-DD)")
        self.time_entry = self.labeled_entry("Time")
        self.category_entry = self.labeled_entry("Category")
        self.desc_entry = self.labeled_entry("Description")

        self.styled_button("Save Event", self.save_event).pack(pady=10)
        self.styled_button("Back", self.build_calendar_screen).pack()

    def save_event(self):
        event = Event(
            self.title_entry.get(),
            self.date_entry.get(),
            self.time_entry.get(),
            self.category_entry.get(),
            self.desc_entry.get()
        )

        if self.calendar.add_event(self.current_user, event):
            messagebox.showinfo("Success", "Event added!")
            self.build_calendar_screen()
        else:
            messagebox.showerror("Error", "Not authorized")

    # ---------- Delete Event ----------
    def delete_event(self):
        selection = self.event_list.curselection()
        if not selection:
            messagebox.showwarning("Select Event", "Please select an event to delete.")
            return

        index = selection[0]
        event = self.display_map.get(index)

        if not event:
            messagebox.showwarning("Invalid Selection", "Please select a valid event.")
            return

        if messagebox.askyesno("Confirm Delete", "Delete this event?"):
            self.calendar.delete_event(event)
            self.refresh_events()

    # ---------- Helpers ----------
    def labeled_entry(self, label_text):
        self.styled_label(label_text).pack()
        entry = self.styled_entry()
        entry.pack(pady=5)
        return entry

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# =========================
# Run App
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()