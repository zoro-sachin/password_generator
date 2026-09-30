# 🔐 Password Generator

A secure, lightweight desktop password generator built with **Python** and **Tkinter**.

The application generates strong random passwords using Python's built-in `secrets` module and provides a simple graphical interface for customizing password length, character types, and the number of passwords generated.

---

## ✨ Features

- 🔐 Cryptographically secure password generation using `secrets`
- 🖥️ Clean desktop GUI built with Tkinter
- 🔢 Password length from **4 to 128 characters**
- 📦 Generate **1 to 20 passwords** at once
- 🔠 Uppercase letters
- 🔡 Lowercase letters
- 🔢 Numbers
- 🔣 Symbols
- 🚫 Option to exclude ambiguous characters
- 📋 Copy all generated passwords to the clipboard
- ✅ Ensures every selected character category is represented
- ⚠️ Input validation and error messages
- 🧪 Unit tests included
- 📦 No third-party Python packages required

---

## 🖼️ Application

The application provides controls for:

- Password length
- Number of passwords
- Character categories
- Ambiguous-character exclusion
- Password generation
- Copying generated passwords

The interface also displays generated passwords and the current application status.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.9+ | Application development |
| Tkinter | Desktop graphical interface |
| `secrets` | Secure random password generation |
| `unittest` | Automated testing |

The project uses only Python's standard library, so no external packages are required.

---

## 📁 Project Structure

```text
password-generator/
│
├── password_generator.py
├── test_password_generator.py
├── README.md
└── .gitignore
```

### `password_generator.py`

Contains the password-generation logic and Tkinter desktop application.

### `test_password_generator.py`

Contains automated unit tests for the password-generation functionality.

### `README.md`

Project documentation and usage instructions.

---

## ⚙️ Requirements

Before running the project, make sure you have:

- **Python 3.9 or newer**
- **Tkinter**

Tkinter is included with most standard Python installations.

No third-party packages are required.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/password-generator.git
```

### 2. Enter the project directory

```bash
cd password-generator
```

### 3. Run the application

```bash
python password_generator.py
```

On some systems, you may need:

```bash
python3 password_generator.py
```

---

## 🎯 How to Use

### Step 1 — Set Password Length

Choose a password length between:

```text
4 - 128 characters
```

### Step 2 — Choose Password Count

Select how many passwords you want to generate:

```text
1 - 20 passwords
```

### Step 3 — Select Character Types

You can include:

- Uppercase
- Lowercase
- Numbers
- Symbols

The generator ensures that each selected category contributes at least one character to the generated password.

### Step 4 — Exclude Ambiguous Characters

Enable:

> Exclude ambiguous characters

This removes:

```text
I  l  1  O  0  |
```

from generated passwords.

This can make passwords easier to read and manually enter.

### Step 5 — Generate

Click:

```text
Generate passwords
```

The generated passwords will appear in the application.

### Step 6 — Copy

Click:

```text
Copy all
```

to copy all generated passwords to the system clipboard.

---

## 🔒 Security

Password generation uses Python's:

```python
secrets
```

module rather than the standard `random` module.

The application selects characters using `secrets.choice()` and securely shuffles the generated characters before returning the final password.

### Important

Generated passwords are **not saved by the application**.

However, when you use **Copy all**, the passwords are placed on your system clipboard. They may remain there until another application replaces or clears the clipboard contents.

---

## 🧪 Testing

The project includes unit tests using Python's built-in `unittest` framework.

Run all tests with:

```bash
python -m unittest -v
```

The tests verify:

- Correct password length
- Required character categories
- Ambiguous-character exclusion
- Single-category passwords
- Empty-category validation
- Invalid password lengths
- Unknown category validation

A successful test run should report all tests as passing.

---

## 🧠 Password Generation Logic

The generator follows this basic process:

```text
User Settings
     │
     ▼
Select Character Categories
     │
     ▼
Validate Settings
     │
     ▼
Generate One Character
from Each Selected Category
     │
     ▼
Fill Remaining Characters
     │
     ▼
Securely Shuffle Characters
     │
     ▼
Final Password
```

For example, if the user selects:

```text
Uppercase
Lowercase
Numbers
Symbols
```

the generator first guarantees at least one character from each category, then fills the remaining positions from the combined character set.

---

## 🎨 User Interface

The application uses Tkinter and `ttk` styling to provide:

- Password settings panel
- Password length control
- Password count control
- Character category selection
- Ambiguous-character option
- Generate button
- Copy button
- Password output area
- Status messages
- Animated security indicator

The interface is configured with a minimum window size and custom styling for buttons, labels, panels, and input controls.

---

## 📋 Example

Example configuration:

```text
Length:        20
How many:      3

Include:
✓ Uppercase
✓ Lowercase
✓ Numbers
✓ Symbols

✓ Exclude ambiguous characters
```

The application will generate three passwords satisfying those settings.

---

## ⚠️ Input Validation

The application validates user input before generating passwords.

Examples of invalid configurations include:

- Password length below 4
- Password length above 128
- Number of passwords below 1
- Number of passwords above 20
- No character categories selected
- Password length smaller than the number of selected categories
- Unknown character categories

Invalid settings are displayed through an error dialog.

---

## 📌 Current Limitations

The current project is a **local desktop password generator**.

It does not currently provide:

- Online password synchronization
- Cloud storage
- Password manager functionality
- Account management
- Password history
- Browser integration
- Automatic password saving

These features are not part of the current implementation.

---

## 🔮 Future Improvements

Possible future improvements include:

- 🌙 Dark mode
- 📊 Password strength indicator
- 🎨 Additional themes
- 🔑 Password strength estimation
- 📋 Individual copy buttons
- 🗑️ Clipboard auto-clear option
- 💾 Optional encrypted password vault
- ⚙️ More advanced generation settings
- 📤 Export functionality
- 🔄 Password regeneration shortcut
- 🖥️ Cross-platform packaging as an executable

---

## 🤝 Contributing

Contributions are welcome.

### Steps

1. Fork the repository.
2. Create a new branch.

```bash
git checkout -b feature/new-feature
```

3. Make your changes.
4. Run the tests.

```bash
python -m unittest -v
```

5. Commit your changes.

```bash
git commit -m "Add new feature"
```

6. Push the branch.

```bash
git push origin feature/new-feature
```

7. Open a Pull Request.

---

## 📄 License

No license is currently specified for this project.

If you plan to make the repository public, consider adding an appropriate open-source license such as the MIT License.

---

## 👨‍💻 Author

**Your Name**

GitHub: `https://github.com/YOUR-USERNAME`

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 🔐 Security Reminder

A password generator can create strong random passwords, but security also depends on how passwords are stored and used.

**Never share your passwords publicly or commit them to a Git repository.**
