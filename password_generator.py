"""A secure, dependency-free password generator with a Tkinter interface."""

from __future__ import annotations

import secrets
import tkinter as tk
from collections.abc import Iterable
from tkinter import messagebox, ttk


CHARACTER_SETS = {
    "Uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "Lowercase": "abcdefghijklmnopqrstuvwxyz",
    "Numbers": "0123456789",
    "Symbols": "!@#$%^&*()-_=+[]{};:,.?",
}
AMBIGUOUS_CHARACTERS = frozenset("Il1O0|")


def generate_password(
    length: int,
    categories: Iterable[str],
    exclude_ambiguous: bool = False,
) -> str:
    """Generate a password containing at least one character from each category."""
    selected_categories = set(categories)
    if not selected_categories:
        raise ValueError("Select at least one character category.")

    unknown_categories = selected_categories.difference(CHARACTER_SETS)
    if unknown_categories:
        raise ValueError(f"Unknown character categories: {', '.join(sorted(unknown_categories))}")
    if length < len(selected_categories):
        raise ValueError("Length must be at least the number of selected categories.")

    groups = []
    for category in sorted(selected_categories):
        characters = CHARACTER_SETS[category]
        if exclude_ambiguous:
            characters = "".join(
                character for character in characters if character not in AMBIGUOUS_CHARACTERS
            )
        if not characters:
            raise ValueError(f"No characters remain in the {category} category.")
        groups.append(characters)

    all_characters = "".join(groups)
    password_characters = [secrets.choice(group) for group in groups]
    password_characters.extend(
        secrets.choice(all_characters) for _ in range(length - len(password_characters))
    )
    secrets.SystemRandom().shuffle(password_characters)
    return "".join(password_characters)


class PasswordGeneratorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("620x590")
        self.root.minsize(560, 540)
        self.root.configure(bg="#f3f6f5")

        self.length_var = tk.StringVar(value="20")
        self.count_var = tk.StringVar(value="1")
        self.exclude_ambiguous_var = tk.BooleanVar(value=True)
        self.category_vars = {
            category: tk.BooleanVar(value=True) for category in CHARACTER_SETS
        }
        self.status_var = tk.StringVar(value="Ready when you are.")
        self._pulse_step = 0
        self._reveal_after_id: str | None = None
        self._generated_passwords: list[str] = []

        self._configure_styles()
        self._build_interface()
        self._animate_indicator()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#f3f6f5")
        style.configure("Panel.TFrame", background="#ffffff")
        style.configure("TLabel", background="#f3f6f5", foreground="#183330", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 25, "bold"), foreground="#153f39")
        style.configure("Hint.TLabel", foreground="#60736f", font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background="#ffffff", foreground="#183330", font=("Segoe UI", 10))
        style.configure("PanelHeading.TLabel", background="#ffffff", foreground="#153f39", font=("Segoe UI", 12, "bold"))
        style.configure("TCheckbutton", background="#ffffff", foreground="#183330", font=("Segoe UI", 10))
        style.map("TCheckbutton", background=[("active", "#ffffff")])
        style.configure("TSpinbox", padding=7, fieldbackground="#ffffff", foreground="#183330")
        style.configure("Primary.TButton", background="#137b68", foreground="#ffffff", font=("Segoe UI", 10, "bold"), padding=(16, 10), borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#0e6657"), ("pressed", "#0b594c")])
        style.configure("Secondary.TButton", background="#e4efec", foreground="#145548", font=("Segoe UI", 10, "bold"), padding=(13, 9), borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#d4e7e1")])

    def _build_interface(self) -> None:
        outer = ttk.Frame(self.root, padding=(32, 26, 32, 22))
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x")
        ttk.Label(header, text="PASSWORD GENERATOR", style="Title.TLabel").pack(side="left")
        secure_badge = ttk.Frame(header)
        secure_badge.pack(side="right", padx=(12, 0), pady=(8, 0))
        self.status_indicator = tk.Canvas(
            secure_badge, width=20, height=20, bg="#f3f6f5", highlightthickness=0
        )
        self.status_halo = self.status_indicator.create_oval(
            4, 4, 16, 16, fill="#d5eee7", outline=""
        )
        self.status_indicator.create_oval(7, 7, 13, 13, fill="#137b68", outline="")
        self.status_indicator.pack(side="left", padx=(0, 5))
        ttk.Label(secure_badge, text="SECURE", style="Hint.TLabel").pack(side="left")
        ttk.Label(
            outer,
            text="Make strong, random passwords for your accounts.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(4, 20))

        options = ttk.Frame(outer, style="Panel.TFrame", padding=20)
        options.pack(fill="x")
        ttk.Label(options, text="Password settings", style="PanelHeading.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 14)
        )

        ttk.Label(options, text="Length", style="Panel.TLabel").grid(row=1, column=0, sticky="w")
        ttk.Spinbox(options, from_=4, to=128, textvariable=self.length_var, width=8).grid(
            row=1, column=1, sticky="w", padx=(10, 26)
        )
        ttk.Label(options, text="How many", style="Panel.TLabel").grid(row=1, column=2, sticky="w")
        ttk.Spinbox(options, from_=1, to=20, textvariable=self.count_var, width=8).grid(
            row=1, column=3, sticky="w", padx=(10, 0)
        )

        ttk.Label(options, text="Include", style="Panel.TLabel").grid(
            row=2, column=0, sticky="nw", pady=(22, 0)
        )
        categories_frame = ttk.Frame(options, style="Panel.TFrame")
        categories_frame.grid(row=2, column=1, columnspan=3, sticky="w", pady=(16, 0))
        for index, (category, variable) in enumerate(self.category_vars.items()):
            ttk.Checkbutton(categories_frame, text=category, variable=variable).grid(
                row=index // 2, column=index % 2, sticky="w", padx=(0, 24), pady=5
            )

        ttk.Checkbutton(
            options,
            text="Exclude ambiguous characters (I, l, 1, O, 0, |)",
            variable=self.exclude_ambiguous_var,
        ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(14, 0))

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(16, 14))
        ttk.Button(
            actions, text="Generate passwords", style="Primary.TButton", command=self._generate
        ).pack(side="left")
        ttk.Button(
            actions, text="Copy all", style="Secondary.TButton", command=self._copy
        ).pack(side="right")

        ttk.Label(outer, text="Your passwords", style="PanelHeading.TLabel").pack(anchor="w", pady=(2, 8))
        self.output = tk.Text(
            outer,
            height=8,
            wrap="none",
            state="disabled",
            relief="flat",
            borderwidth=0,
            padx=14,
            pady=12,
            bg="#ffffff",
            fg="#183330",
            insertbackground="#137b68",
            font=("Consolas", 12),
        )
        self.output.pack(fill="both", expand=True)
        ttk.Label(outer, textvariable=self.status_var, style="Hint.TLabel").pack(
            anchor="w", pady=(10, 0)
        )

    def _animate_indicator(self) -> None:
        radii = (6, 6.5, 7, 7.5, 7, 6.5)
        radius = radii[self._pulse_step]
        self.status_indicator.coords(
            self.status_halo, 10 - radius, 10 - radius, 10 + radius, 10 + radius
        )
        self._pulse_step = (self._pulse_step + 1) % len(radii)
        self.root.after(120, self._animate_indicator)

    def _generate(self) -> None:
        try:
            length = int(self.length_var.get())
            count = int(self.count_var.get())
            categories = [
                category for category, variable in self.category_vars.items() if variable.get()
            ]
            if not 4 <= length <= 128:
                raise ValueError("Choose a password length from 4 to 128.")
            if not 1 <= count <= 20:
                raise ValueError("Choose between 1 and 20 passwords.")
            if length < len(categories):
                raise ValueError("Length must be at least the number of selected categories.")

            passwords = [
                generate_password(length, categories, self.exclude_ambiguous_var.get())
                for _ in range(count)
            ]
        except ValueError as error:
            messagebox.showerror("Check your settings", str(error), parent=self.root)
            return

        if self._reveal_after_id is not None:
            self.root.after_cancel(self._reveal_after_id)
            self._reveal_after_id = None
        self._generated_passwords = passwords
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")
        self.status_var.set("Revealing passwords...")
        self._reveal_password_line(passwords, 0)

    def _reveal_password_line(self, passwords: list[str], index: int) -> None:
        if index == len(passwords):
            count = len(passwords)
            self.status_var.set(f"Generated {count} password{'s' if count != 1 else ''}.")
            self._reveal_after_id = None
            return

        self.output.configure(state="normal")
        if index:
            self.output.insert("end", "\n")
        self.output.insert("end", passwords[index])
        self.output.configure(state="disabled")
        self._reveal_after_id = self.root.after(
            55, self._reveal_password_line, passwords, index + 1
        )

    def _copy(self) -> None:
        passwords = "\n".join(self._generated_passwords)
        if not passwords:
            self.status_var.set("Generate a password first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(passwords)
        self.status_var.set("Passwords copied to the clipboard.")


def main() -> None:
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
