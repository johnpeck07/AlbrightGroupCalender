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
        return f"{self.date} | {self.time} | {self.title} ({self.category})"


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


# =========================
# GUI Application
# =========================
class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Albright Student Calendar")

        self.calendar = Calendar()
        self.current_user = None

        self.build_login_screen()

    # ---------- LOGIN SCREEN ----------
    def build_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Albright Student Calendar", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Name").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="Email").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        tk.Button(self.root, text="Request Access", command=self.request_access).pack(pady=10)

    def request_access(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        user = User(name, email)

        if user.request_access():
            self.calendar.add_user(user)
            self.current_user = user
            messagebox.showinfo("Success", "Access approved!")
            self.build_calendar_screen()
        else:
            messagebox.showerror("Denied", "Must use an @albright.edu email")

    # ---------- CALENDAR SCREEN ----------
    def build_calendar_screen(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Welcome, {self.current_user.name}", font=("Arial", 14)).pack(pady=5)

        self.event_list = tk.Listbox(self.root, width=60)
        self.event_list.pack(pady=10)

        tk.Button(self.root, text="Add Event", command=self.build_add_event_screen).pack()
        tk.Button(self.root, text="Logout", command=self.build_login_screen).pack(pady=5)

        self.refresh_events()

    def refresh_events(self):
        self.event_list.delete(0, tk.END)
        for event in self.calendar.events:
            self.event_list.insert(tk.END, event.display())

    # ---------- ADD EVENT SCREEN ----------
    def build_add_event_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Add New Event", font=("Arial", 14)).pack(pady=10)

        self.title_entry = self.labeled_entry("Title")
        self.date_entry = self.labeled_entry("Date (YYYY-MM-DD)")
        self.time_entry = self.labeled_entry("Time")
        self.category_entry = self.labeled_entry("Category")
        self.desc_entry = self.labeled_entry("Description")

        tk.Button(self.root, text="Save Event", command=self.save_event).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.build_calendar_screen).pack()

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

    # ---------- HELPERS ----------
    def labeled_entry(self, label_text):
        tk.Label(self.root, text=label_text).pack()
        entry = tk.Entry(self.root)
        entry.pack()
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
