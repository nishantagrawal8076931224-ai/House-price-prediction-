import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import joblib


# ============================================================
# MAIN WINDOW CLASS (AUTO RESIZE BACKGROUND)
# ============================================================
class Housepage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("House Price Prediction App")
        self.geometry("900x600")          # Start larger
        self.minsize(650, 520)

        # Load RAW background image
        self.bg_raw = Image.open("bg.jpg").convert("RGB")

        # Container
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Create pages
        self.frames = {}
        for Page in (HomePage, PredictPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.place(relwidth=1, relheight=1)

        # Always update background image when window resizes
        self.bind("<Configure>", self.resize_background)

        self.show_frame(HomePage)

    def resize_background(self, event=None):
        """Auto resizes background image for both pages."""
        new_w = self.winfo_width()
        new_h = self.winfo_height()

        resized = self.bg_raw.resize((new_w, new_h), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)

        # Update background on each page
        for frame in self.frames.values():
            if hasattr(frame, "bg_label"):
                frame.bg_label.config(image=self.bg_photo)
                frame.bg_label.image = self.bg_photo

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


# ============================================================
# HOME PAGE
# ============================================================
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Background label
        self.bg_label = tk.Label(self)
        self.bg_label.place(relwidth=1, relheight=1)

        # Title
        title = tk.Label(self, text="House Price Prediction",
                         font=("Arial", 26, "bold"), bg="#ffffff")
        title.pack(pady=80)

        # Button
        start_btn = tk.Button(self, text="Go to Prediction Page",
                              command=lambda: controller.show_frame(PredictPage),
                              font=("Arial", 16),
                              bg="#4CAF50", fg="white",
                              padx=20, pady=10)
        start_btn.pack()


# ============================================================
# PREDICTION PAGE
# ============================================================
class PredictPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Background label
        self.bg_label = tk.Label(self)
        self.bg_label.place(relwidth=1, relheight=1)

        # Title
        title = tk.Label(self, text="Enter House Details",
                         font=("Arial", 22, "bold"), bg="#ffffff")
        title.pack(pady=10)

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

        # Predict button
        predict_btn = tk.Button(self, text="Predict Price",
                                command=self.predict_price,
                                font=("Arial", 16, "bold"),
                                bg="#4CAF50", fg="white",
                                padx=20, pady=10)
        predict_btn.pack(pady=20)

        # Result
        self.result_label = tk.Label(self, text="",
                                     font=("Arial", 18, "bold"),
                                     bg="#ffffff")
        self.result_label.pack(pady=10)

        # Back button
        back_btn = tk.Button(self, text="← Back to Home",
                             command=lambda: controller.show_frame(HomePage),
                             font=("Arial", 14),
                             bg="#f44336", fg="white",
                             padx=15, pady=5)
        back_btn.pack(pady=10)

    def predict_price(self):
        try:
            values = [float(entry.get()) for entry in self.entries]
            price = model.predict([values])[0]
            self.result_label.config(text=f"Predicted Price: ₹ {price:,.2f}")
        except:
            messagebox.showerror("Error", "Please enter valid numbers!")


# ============================================================
# RUN APP
# ============================================================
model = joblib.load("model.pkl")
app = Housepage()
app.mainloop()
