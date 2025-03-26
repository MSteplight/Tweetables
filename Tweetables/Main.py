import tkinter as tk
import threading
import subprocess
import os
import sys

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("350x300")
        self.master.configure(bg="#ADD8E6")

        self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="Username:", font=("Arial", 12), bg="#ADD8E6").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="#ADD8E6").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)

        self.message_label = tk.Label(self.frame, text="", fg="red", bg="#ADD8E6", font=("Arial", 10))
        self.message_label.grid(row=2, columnspan=2, pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.validate_login, font=("Arial", 12), bg="black", fg="black", padx=10, pady=5)
        self.login_button.grid(row=3, columnspan=2, pady=10)

        self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.open_signup, font=("Arial", 12), bg="black", fg="black", padx=10, pady=5)
        self.signup_button.grid(row=4, columnspan=2, pady=10)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.check_credentials(username, password):
            self.message_label.config(text="Login successful!", fg="green")
            self.open_sentiment_analysis()
        else:
            self.message_label.config(text="Invalid credentials.", fg="red")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def check_credentials(self, username, password):
        try:
            with open("users.txt", "r") as file:
                for line in file:
                    stored_user, stored_pass = line.strip().split(",")
                    if stored_user == username and stored_pass == password:
                        return True
        except FileNotFoundError:
            return False
        return False

    def open_signup(self):
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Sign Up")
        signup_window.geometry("350x200")
        signup_window.configure(bg="#ADD8E6")

        frame = tk.Frame(signup_window, bg="#ADD8E6", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="New Username:", font=("Arial", 12), bg="#ADD8E6").grid(row=0, column=0, sticky="w", pady=5)
        new_username = tk.Entry(frame, font=("Arial", 12))
        new_username.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(frame, text="New Password:", font=("Arial", 12), bg="#ADD8E6").grid(row=1, column=0, sticky="w", pady=5)
        new_password = tk.Entry(frame, font=("Arial", 12), show="*")
        new_password.grid(row=1, column=1, pady=5, padx=10)

        def save_credentials():
            username = new_username.get()
            password = new_password.get()
            if username and password:
                with open("users.txt", "a") as file:
                    file.write(f"{username},{password}\n")
                signup_window.destroy()

        signup_button = tk.Button(frame, text="Sign Up", command=save_credentials, font=("Arial", 12), bg="black", fg="black", padx=10, pady=5)
        signup_button.grid(row=2, columnspan=2, pady=10)

    def open_sentiment_analysis(self):
        self.master.destroy()
        root = tk.Tk()
        app = SentimentAnalysisApp(root)
        root.mainloop()

class SentimentAnalysisApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tweetables: Sentiment Analysis")
        self.master.geometry("600x400")
        self.master.configure(bg="#ADD8E6")

        self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.frame, text="Tweetables: Movie Sentiment Analysis Tool", font=("Helvetica", 16, "bold"), bg="#ADD8E6").pack(pady=10)
        
        self.output_text = tk.Text(self.frame, wrap=tk.WORD, height=12, font=("Arial", 12))
        self.output_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        btn_frame = tk.Frame(self.frame, bg="#ADD8E6")
        btn_frame.pack(pady=10)
        
        self.search_button = tk.Button(btn_frame, text="Fetch Tweets", command=self.open_fetch_tweets, font=("Arial", 12), bg="black", fg="black", padx=10, pady=5)
        self.search_button.grid(row=0, column=0, padx=5)
        
        self.analysis_button = tk.Button(btn_frame, text="Analyze Sentiment", command=self.run_sentiment_analysis, font=("Arial", 12), bg="black", fg="black", padx=10, pady=5)
        self.analysis_button.grid(row=0, column=1, padx=5)
    
    def append_output(self, output):
        self.output_text.insert(tk.END, output + '\n')
        self.output_text.see(tk.END)
        print(output)

    def open_fetch_tweets(self):
        threading.Thread(target=self.run_fetch_tweets).start()

    def run_fetch_tweets(self):
        self.append_output("Fetching tweets for sentiment analysis...")
        script_path = os.path.join(os.path.dirname(__file__), "fetch_tweets.py")
        process = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.append_output(output.strip())

        return_code = process.wait()
        self.append_output(f"Tweet fetching completed with return code: {return_code}")

if __name__ == "__main__":
    root = tk.Tk()
    login = LoginScreen(root)
    root.mainloop()

