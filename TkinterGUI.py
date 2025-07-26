
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from DatabaseConnector import *
from GolfSwingAnalysis import *

user_id = None
class HomePage(tk.Frame):
    def __init__(self, master, switch_callback):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Home Page", font=("Helvetica", 16)).pack(pady=20)

        new_user_button = tk.Button(self, text="New User", command=self.new_user)
        new_user_button.pack(pady=10)

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=10)

    def new_user(self):
        self.switch_callback(RegisterPage)

    def login(self):
        self.switch_callback(LoginPage)


class RegisterPage(tk.Frame):
    global user_id
    def __init__(self, master, switch_callback):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Registration Page", font=("Helvetica", 16)).pack(pady=20)

        back_home_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_home_button.pack(pady=10)

        tk.Label(self, text="Username:").pack()
        username_entry = tk.Entry(self)
        username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack()
        password_entry = tk.Entry(self, show="*")
        password_entry.pack(pady=5)

        error_label = tk.Label(text="")

        register_button = tk.Button(self, text="Register", command=lambda: self.register(username_entry.get(), password_entry.get(),
                                                                                         username_entry, password_entry, error_label))
        register_button.pack(pady=10)

        error_label = tk.Label(self, text="")
        error_label.pack(pady=10)

    def back_to_home(self):
        self.switch_callback(HomePage)

    def register(self, username, password, un_entry, pw_entry, error_label):
        global user_id
        if username == "" or password == "":
            error_label.config(text="Missing Username or Password", fg="red")
        elif is_in_db(db, username):
            error_label.config(text="Username Already Exists", fg="red")
            un_entry.delete(0, tk.END)
            pw_entry.delete(0, tk.END)
        else:
            insert_golfer(db, username, password)
            user_id = get_id_from_username(db, username)
            self.switch_callback(ChoicePage)

class LoginPage(tk.Frame):
    global user_id

    def __init__(self, master, switch_callback):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Login Page", font=("Helvetica", 16)).pack(pady=20)

        # Back to Home button
        back_home_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_home_button.pack(pady=10)

        # Entry for Username
        tk.Label(self, text="Username:").pack()
        username_entry = tk.Entry(self)
        username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack()
        password_entry = tk.Entry(self, show="*")
        password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(self, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get(),
                                                                                username_entry, password_entry, error_label))
        login_button.pack(pady=10)

        error_label = tk.Label(self, text="")
        error_label.pack(pady=10)

    def back_to_home(self):
        self.switch_callback(HomePage)

    def login(self, username, password, un_entry, pw_entry, error_label):
        global user_id
        if is_in_db(db, username) and get_password(db, username, password):
            user_id = get_id_from_username(db, username)
            self.switch_callback(ChoicePage)
        elif username == "" or password == "":
            error_label.config(text="Missing Username or Password", fg="red")
            un_entry.delete(0, tk.END)
            pw_entry.delete(0, tk.END)
        else:
            un_entry.delete(0, tk.END)
            pw_entry.delete(0, tk.END)
            error_label.config(text="Incorrect Username or Password", fg="red")


class ChoicePage(tk.Frame):
    global user_id
    def __init__(self, master, switch_callback):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Choice Page", font=("Helvetica", 16)).pack(pady=20)

        # New Analysis button
        new_analysis_button = tk.Button(self, text="New Analysis", command=self.new_analysis)
        new_analysis_button.pack(pady=10)

        # View Past Analyses button
        view_past_button = tk.Button(self, text="View Past Analyses", command=self.view_past_analyses)
        view_past_button.pack(pady=10)

        back_home_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_home_button.pack(pady=10)

    def new_analysis(self):
        self.switch_callback(NewAnalysisPage)

    def view_past_analyses(self):
        self.switch_callback(ViewPastAnalysesPage)

    def back_to_home(self):
        self.switch_callback(HomePage)


class NewAnalysisPage(tk.Frame):
    global user_id
    def __init__(self, master, switch_callback):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback
        self.create_widgets()


    def create_widgets(self):
        tk.Label(self, text="New Analysis Page", font=("Helvetica", 16)).pack(pady=20)

        upload_file_button = tk.Button(self, text="Choose File from Computer", command=lambda: self.upload_from_cpu(entered_video_path))
        upload_file_button.pack(pady=10)

        entered_video_path = tk.Entry(self)
        entered_video_path.pack(pady=10)

        advice_label_speed = tk.Label(self, text="Using videos that are at iPhone Slo-Mo speed or slower will provide the most accurate analysis.", font=("Helvetica", 12))
        advice_label_speed.pack(pady=10)
        advice_label_position = tk.Label(self, text="Make sure to record from DIRECTLY behind the golfer and from about their waist height.", font=("Helvetica", 12))
        advice_label_position.pack(pady=10)

        right_analyze_button = tk.Button(self, text="Analyze Swing - Right Handed", command = lambda: self.right_analysis_output(entered_video_path.get()))
        right_analyze_button.pack(pady=10)

        left_analyze_button = tk.Button(self, text="Analyze Swing - Left Handed", command = lambda:self.left_analysis_output(entered_video_path.get()))
        left_analyze_button.pack(pady=10)

        back_home_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_home_button.pack(pady=10)
    def upload_from_cpu(self, entered_video_path):
        # Open up files from computer
        file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[])
        # Delete any text currently in text box
        entered_video_path.delete(0, tk.END)
        # Add the computer file path to the text box
        entered_video_path.insert(0, file_path)


    def back_to_home(self):
        self.switch_callback(HomePage)

    def left_analysis_output(self, video_path):
        try:
            self.switch_callback(AnalysisOutputPage, False, video_path)
        except Exception as e:
            # If an error occurs, display an error label
            error_message = "Invalid File Input"
            error_label = tk.Label(self, text=error_message, font=("Helvetica", 12), fg="red")
            error_label.pack(pady=10)
    def right_analysis_output(self, video_path):
        try:
            self.switch_callback(AnalysisOutputPage, True, video_path)
        except Exception as e:
            # If an error occurs, display an error label
            error_message = "Invalid File Input"
            error_label = tk.Label(self, text=error_message, font=("Helvetica", 12), fg="red")
            error_label.pack(pady=10)




class AnalysisOutputPage(tk.Frame):
    global user_id
    def __init__(self, master, switch_callback, right_handed, video_path):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback
        self.right_handed = right_handed
        self.video_path = video_path
        self.create_widgets()

    def create_widgets(self):
        global user_id
        tk.Label(self, text="Analysis Output", font=("Helvetica", 16)).pack()

        stats = swing_analysis(self.video_path, self.right_handed)
        now = datetime.now()
        current_date = datetime(now.year, now.month, now.day)
        insert_submission(db, user_id, float(stats[8]), current_date)
        stats_title_label = tk.Label(self, text=" Rory's Stats:                                                                              User's Stats: ", font=("Helvetica", 14))
        stats_title_label.place(relx = 0.43, rely=0.1, anchor=tk.CENTER)
        #Holds all titles for each stat
        titles = [
            "Kneebend Initial Angle: ",
            "Initial Back Posture Angle: ",
            "Initial Ball Position Angle: ",
            "Initial Back Arm Angle: ",
            "Arm Takeback Distance from Initial X-Value: ",
            "Top Arm Angle: ",
            "Final Back Leg Angle: ",
            "Head Vertical Change: "]
        rory_data = [156.8, 129.75, 47, 170.67, 9.9, 93.8, 157.4, 26.1]

        # Display Similarity Score
        message = "Similarity Score: " + str(stats[-1])
        sim_label = tk.Label(self, text=message, font=("Helvetica", 16))
        sim_label.place(relx=0.5, rely=0.8)

        for i, stat in enumerate(stats[0:-1]):
            message = titles[i] + str(stat)
            stats_label = tk.Label(self, text=message, font=("Helvetica", 12))
            stats_label.place(relx=0.6, rely=i / 13 + 0.15)
            #Use this list format for Rory's Data
        for i, stat in enumerate(rory_data):
            message = titles[i] + str(stat)
            stats_label = tk.Label(self, text=message, font=("Helvetica", 12))
            stats_label.place(relx=0.1, rely=i / 13 + 0.15)

        back_home_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_home_button.place(relx=0.3, rely=0.8, anchor=tk.CENTER)





    def back_to_home(self):
        self.switch_callback(HomePage)


class ViewPastAnalysesPage(tk.Frame):
    def __init__(self, master, switch_callback):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback
        self.create_widgets()

    def create_widgets(self):
        global user_id
        tk.Label(self, text="View Past Analyses Page", font=("Helvetica", 16)).pack(pady=20)

        # Back to Home button
        back_home_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_home_button.pack(pady=10)

        # ListBox for displaying list of similarity scores
        listbox = tk.Listbox(self)
        listbox.insert(tk.END, "      Date                Score")
        for score in get_user_submissions(db, user_id):
            formatted_entry = str(score[0]) +  "          " + str(score[1])
            listbox.insert(tk.END, formatted_entry)
        listbox.pack(pady=10)

    def back_to_home(self):
        self.switch_callback(ChoicePage)


class GUIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("User Analysis Application")
        self.geometry("800x600")
        self.current_page = None
        self.switch_page(HomePage)

    def switch_page(self, page_class, *args, **kwargs):
        new_page = page_class(self, self.switch_page, *args, **kwargs)
        if self.current_page is not None:
            self.current_page.destroy()
        new_page.pack(fill="both", expand=True)
        self.current_page = new_page

if __name__ == "__main__":
    app = GUIApp()
    app.mainloop()
