
# Tech Events Hub

Tech Events Hub is a web platform built with Flask to help college students discover and share upcoming tech events like hackathons, workshops, and tech talks.


## 🚀 Features

- Submit tech events easily  
- View curated events from other campuses  
- Filter events by date, location, or category  
- Lightweight and mobile-friendly design



## 🛠 Tech Stack

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Flask (Python)  
- **Database**: MySQL  
- **Tools**: Git, GitHub, dotenv



## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/croesus245/techeventshub.git
cd techeventshub
````

Create a virtual environment and activate it:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the root of your project and add your secrets:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DB_USER=your-database-username
DB_PASSWORD=your-database-password
DB_NAME=your-database-name
```

Run the development server:

```bash
flask run
```


## 🔐 Security Notice

> ❗ **Do not commit your `.env` file to GitHub.**
> It contains sensitive information like passwords and API keys.
> Make sure you’ve added `.env` to your `.gitignore` file:

```bash
# .gitignore
.env
__pycache__/
venv/
```

If you've already pushed `.env` by mistake:

1. Run: `git rm --cached .env`
2. Add `.env` to `.gitignore`
3. Commit & push again
4. Change your exposed secrets ASAP



## 🤝 Contributing

Have an event idea or want to improve the project?
Pull requests are welcome. For major changes, please open an issue first.


## 👤 Author

**Croesus (Ayinde Abdul-Sobur O.)**
GitHub: [@croesus245](https://github.com/croesus245)
