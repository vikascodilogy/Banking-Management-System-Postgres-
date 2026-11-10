# 🏦 CodilogyBank — Banking Management System

A full-stack Banking Management System built with **Python + PostgreSQL**, featuring both a command-line interface (CLI) and a modern **Streamlit GUI** with glassmorphism design and 3D animations.

> Built & maintained by [Codilogy](https://github.com/vikascodilogy)

---

## ✨ Features

| Feature | CLI | Streamlit GUI |
|---------|-----|---------------|
| Create Account | ✅ | ✅ |
| Login / Auth | ✅ | ✅ |
| Check Balance | ✅ | ✅ |
| Deposit Money | ✅ | ✅ |
| Withdraw Money | ✅ | ✅ |
| Transaction History | ✅ | ✅ |
| Update Profile | ✅ | ✅ |
| Change PIN | ✅ | ✅ |
| Close Account | ✅ | ✅ |
| PIN Hashing (SHA-256) | ✅ | ✅ |
| Audit Logging | ✅ | ✅ |
| Glassmorphism UI | ❌ | ✅ |
| 3D Animated Cube | ❌ | ✅ |
| Responsive Design | ❌ | ✅ |

---

## 📁 Project Structure

```
Banking Management System/
├── app.py              # Streamlit GUI (CodilogyBank)
├── main.py             # CLI banking logic (BankSystem, Account, Audit)
├── database.py         # PostgreSQL connection
├── README.md           # Project documentation
├── .venv/              # Virtual environment
├── __pycache__/        # Python cache
└── .git/               # Git version control
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Database:** PostgreSQL
- **Database Driver:** psycopg2
- **GUI Framework:** Streamlit
- **Password Security:** SHA-256 hashing
- **Styling:** Custom CSS (Glassmorphism, Gradients, 3D CSS animations)

---

## 🗄️ Database Schema

### `accounts` Table
| Column | Type | Constraints |
|--------|------|-------------|
| `account_number` | `varchar(50)` | PRIMARY KEY |
| `name` | `varchar(100)` | NOT NULL |
| `pin` | `varchar(64)` | NOT NULL (SHA-256 hash) |
| `balance` | `decimal(15,2)` | DEFAULT 0.00 |
| `created_at` | `timestamp` | DEFAULT current_timestamp |

### `audit` Table
| Column | Type | Constraints |
|--------|------|-------------|
| `id` | `serial` | PRIMARY KEY |
| `account_number` | `varchar(50)` | FOREIGN KEY → accounts |
| `holder_name` | `varchar(100)` | |
| `action` | `varchar(100)` | NOT NULL |
| `amount` | `decimal(15,2)` | DEFAULT 0.00 |
| `timestamp` | `timestamp` | DEFAULT current_timestamp |

Tables are auto-created on first run via `initialize_tables()`.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vikascodilogy/Banking-Management-System-Postgres-.git
cd "Banking Management System"
```

### 2. Create & Activate Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install psycopg2-binary streamlit
```

### 4. Configure PostgreSQL

Make sure PostgreSQL is running and update `database.py` with your credentials:

```python
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="banksystemmanagement",  # Create this database first
    user="postgres",
    password="your_password"
)
```

Create the database beforehand:

```sql
CREATE DATABASE banksystemmanagement;
```

---

## ▶️ How to Run

### Option 1: Streamlit GUI (Recommended 🎨)

```bash
streamlit run app.py
```

Then open: **http://localhost:8501**

The GUI includes:
- 🎯 Home page with 3D animated "CODILY" cube
- 📝 Account creation
- 🔐 Secure login
- 💳 Dashboard with balance display
- 💰 Deposit & 🏧 Withdraw
- 📄 Transaction history
- 👤 Profile & PIN management
- ❌ Account closure

### Option 2: CLI (Command Line)

```bash
python main.py
```

---

## 📸 Screenshots (Coming Soon)

> Add screenshots of the GUI here once deployed.

---

## 🔐 Security

- PINs are stored as **SHA-256 hashes** (never plain text)
- Every action is logged in the `audit` table
- PIN verification on sensitive operations (close account, change PIN)
- Parameterized queries to prevent SQL injection

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Vikas Gupta** — [Codilogy](https://github.com/vikascodilogy)

GitHub: https://github.com/vikascodilogy/Banking-Management-System-Postgres-

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the Python GUI framework
- [PostgreSQL](https://www.postgresql.org/) for the relational database
- [psycopg2](https://www.psycopg.org/) for PostgreSQL adapter