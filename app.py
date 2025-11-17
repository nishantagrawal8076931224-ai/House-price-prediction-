import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import joblib

# Load your model
model = joblib.load("model.pkl")


# ============================================================
# MAIN WINDOW CLASS
# ============================================================
class Housepage(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window size settings
        self.title("House Price Prediction App")
        self.geometry("650x520")
        self.minsize(650, 520)
        self.resizable(False, False)

        # Load background image
        try:
            self.bg_img = Image.open("bg.jpg")   # Make sure image name is bg.jpg
            self.bg_img = self.bg_img.resize((650, 520))
            self.bg_photo = ImageTk.PhotoImage(self.bg_img)
            print("Background image loaded successfully.")
        except Exception as e:
            print("Error loading background image:", e)

        # Main Container Frame
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.pack_propagate(False)

        # Creating both pages
        self.frames = {}
        for Page in (HomePage, PredictPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.place(relwidth=1, relheight=1)

        # Show Home Page first
        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


# ============================================================
# HOME PAGE
# ============================================================
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Background
        bg_label = tk.Label(self, image=controller.bg_photo)
        bg_label.place(relwidth=1, relheight=1)

        self.pack_propagate(False)

        # Title Label
        title = tk.Label(self, text="🏠 House Price Prediction",
                         font=("Arial", 26, "bold"), bg="#ffffff")
        title.pack(pady=120)

        # Button to go to Prediction Page
        start_btn = tk.Button(self, text="Go to Prediction Page",
                              command=lambda: controller.show_frame(PredictPage),
                              font=("Arial", 16), bg="#4CAF50",
                              fg="white", padx=20, pady=10)
        start_btn.pack()


# ============================================================
# PREDICTION PAGE
# ============================================================
class PredictPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Background Image
        bg_label = tk.Label(self, image=controller.bg_photo)
        bg_label.place(relwidth=1, relheight=1)

        self.pack_propagate(False)

        # Title
        title = tk.Label(self, text="Enter House Details",
                         font=("Arial", 22, "bold"), bg="#ffffff")
        title.pack(pady=10)

        # Input Form
        form = tk.Frame(self, bg="#ffffff")
        form.pack(pady=10)

        labels = [
            "Number of Bedrooms:",
            "Number of Bathrooms:",
            "Living Area (sq ft):",
            "Number of Floors:",
            "Area of House:",
            "Number of Schools Nearby:"
        ]

        self.entries = []

        for i, text in enumerate(labels):
            tk.Label(form, text=text, font=("Arial", 12),
                     bg="#ffffff").grid(row=i, column=0, pady=5)

            entry = tk.Entry(form, font=("Arial", 12))
            entry.grid(row=i, column=1, pady=5)
            self.entries.append(entry)

        # Predict Button
        predict_btn = tk.Button(self, text="Predict Price",
                                command=self.predict_price,
                                font=("Arial", 16, "bold"), bg="#4CAF50",
                                fg="white", padx=20, pady=10)
        predict_btn.pack(pady=20)

        # Result label
        self.result_label = tk.Label(self, text="",
                                     font=("Arial", 18, "bold"), bg="#ffffff")
        self.result_label.pack(pady=10)

        # Back button
        back_btn = tk.Button(self, text="← Back to Home",
                             command=lambda: controller.show_frame(HomePage),
                             font=("Arial", 14), bg="#f44336", fg="white",
                             padx=15, pady=5)
        back_btn.pack(pady=10)

    def predict_price(self):
        try:
            vals = [float(entry.get()) for entry in self.entries]
            price = model.predict([vals])[0]
            self.result_label.config(
                text=f"Predicted Price: ₹ {price:,.2f}"
            )
        except:
            messagebox.showerror("Error", "Please enter valid numbers!")


# ============================================================
# RUN APP
# ============================================================
app = Housepage()
app.mainloop()