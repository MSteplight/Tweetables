import tkinter as tk
import threading
import subprocess
import os
import sys

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("300x200")

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(master, text="Login", command=self.validate_login)
        self.login_button.pack(pady=10)

        self.message_label = tk.Label(master, text="", fg="red")
        self.message_label.pack(pady=5)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # TODO: Replace with secure authentication (e.g., hashed passwords)
        if username == "admin" and password == "password":
            self.message_label.config(text="Login successful!", fg="green")
            self.open_sentiment_analysis()
        else:
            self.message_label.config(text="Invalid credentials.", fg="red")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

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

        self.welcome_label = tk.Label(
            master, 
            text="Tweetables: Movie Sentiment Analysis Tool!", 
            font=('Helvetica', 18, 'bold')
        )
        self.welcome_label.pack(pady=10)

        # Create a Text widget to display sentiment analysis results
        self.output_text = tk.Text(master, wrap=tk.WORD, height=15)
        self.output_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Buttons for sentiment analysis
        self.search_button = tk.Button(master, text="Fetch Tweets", command=self.open_fetch_tweets)
        self.search_button.pack(pady=10)

        self.analysis_button = tk.Button(master, text="Analyze Sentiment", command=self.run_sentiment_analysis)
        self.analysis_button.pack(pady=10)

    def append_output(self, output):
        """ Append output to the text widget and print to terminal. """
        self.output_text.insert(tk.END, output + '\n')
        self.output_text.see(tk.END)
        print(output)

    def open_fetch_tweets(self):
        threading.Thread(target=self.run_fetch_tweets).start()

    def run_fetch_tweets(self):
        """ Runs the script to fetch tweets for analysis. """
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

    def run_sentiment_analysis(self):
        """ Runs the sentiment analysis script. """
        threading.Thread(target=self.run_analysis_script).start()

    def run_analysis_script(self):
        self.append_output("Running sentiment analysis on tweets...")
        script_path = os.path.join(os.path.dirname(__file__), "fetch_tweets.py")

        process = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.append_output(output.strip())

        return_code = process.wait()
        self.append_output(f"Sentiment analysis completed with return code: {return_code}")


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    login = LoginScreen(root)
    root.mainloop()
