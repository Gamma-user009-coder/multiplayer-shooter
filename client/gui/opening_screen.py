import customtkinter as ctk
from game import Game

# Set the appearance mode and theme (optional but recommended)
ctk.set_appearance_mode("Dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"


class LoginScreen(ctk.CTk):
    """
    Represents the main application window (Login Screen) using OOP.
    """

    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Wizard")
        self.geometry("400x300")
        self.resizable(False, False)

        # Configure the grid to center the content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # --- Widgets ---

        # 1. Title Label
        self.title_label = ctk.CTkLabel(self, text="Application Login",
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=1, padx=20, pady=(30, 10), sticky="s")

        # 2. Username Entry Label
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="w")

        # 3. Username Entry Textbox
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter your username", width=250)
        self.username_entry.grid(row=2, column=1, padx=20, pady=(0, 10), sticky="ew")

        # 4. Login Button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_event, width=100)
        self.login_button.grid(row=3, column=1, padx=(20, 140), pady=(10, 5), sticky="w")

        # 5. Exit/Cancel Button
        self.cancel_button = ctk.CTkButton(self, text="Exit", command=self.destroy, fg_color="red",
                                           hover_color="darkred", width=100)
        self.cancel_button.grid(row=3, column=1, padx=(140, 20), pady=(10, 5), sticky="e")

    # --- Button Command Methods ---

    def login_event(self):
        """
        Handles the login button click event.
        """
        username = self.username_entry.get()
        self.destroy()
        Game(username).run()
        print(f"Login attempt with username: {username}")
        # Add your authentication logic here (e.g., check against a database)


# --- Main Execution Block ---
if __name__ == "__main__":
    app = LoginScreen()
    app.mainloop()