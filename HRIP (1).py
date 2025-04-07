import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import os

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App")

        # Initialize camera variables
        self.cap = None
        self.camera_running = False
        self.last_qr_code = None  # To store the last scanned QR code message

        # Enhanced button style configuration
        button_style = {
            'font': ('Arial', 14, 'bold'),
            'background': 'white',
            'foreground': 'black',
            'relief': tk.RAISED,
            'borderwidth': 2,
            'padding': 10
        }

        # Configure ttk style
        ttk.Style().configure('Custom.TButton', **button_style)

        # Load and resize background image 
        bg_image_path = r"C:\Users\amrit\Downloads\Presentation1.png"
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(bg_image)

        # Create a canvas to place the background image
        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1) 

        # Create label for displaying live camera feed with larger size
        self.camera_label = tk.Label(self.root)
        self.camera_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.camera_label.config(width=int(root.winfo_screenwidth() * 0.6), height=int(root.winfo_screenheight() * 0.6))

        # Create buttons with enhanced style
        self.start_camera_button = ttk.Button(self.root, text="Start Camera", command=self.start_camera, style='Custom.TButton')
        self.start_camera_button.place(relx=0.05, rely=0.5, anchor=tk.W)

        self.capture_button = ttk.Button(self.root, text="Capture Image", command=self.capture_image, style='Custom.TButton')
        self.capture_button.place(relx=0.05, rely=0.6, anchor=tk.W)

        self.stop_camera_button = ttk.Button(self.root, text="Stop Camera", command=self.stop_camera, style='Custom.TButton')
        self.stop_camera_button.place(relx=0.05, rely=0.7, anchor=tk.W)

        # Start the camera automatically after getting QR code
        self.show_scan_prompt()

    def show_scan_prompt(self):
        # Disable main window until QR dialog is closed
        self.root.withdraw()

        #input from external scanner
        qr_code_text = simpledialog.askstring("Input QR Code", "Enter QR code message:")

        # After dialog is closed, focus back on main window
        self.root.deiconify()

        if qr_code_text:
            self.last_qr_code = qr_code_text
            self.start_camera()

    def start_camera(self):
        if not self.camera_running:
            self.cap = cv2.VideoCapture(0)  # Initialize camera 
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot access the camera.")
                return
            
            # Set camera resolution to the highest possible values
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            
            self.camera_running = True
            self.show_camera()

    def stop_camera(self):
        if self.camera_running:
            if self.cap is not None:
                self.cap.release()
            self.camera_running = False

    def show_camera(self):
        if self.camera_running and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                # Resize the frame to fit the larger label
                frame = cv2.resize(frame, (int(self.root.winfo_screenwidth() * 0.6), int(self.root.winfo_screenheight() * 0.6)))
                # Enhance image quality
                frame = self.enhance_image(frame)
                # Convert frame to RGB format and then to ImageTk format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(image=frame)
                self.camera_label.config(image=frame)
                self.camera_label.image = frame
            self.root.after(10, self.show_camera)  # Update every 10 milliseconds

    def capture_image(self):
        if self.camera_running and self.cap is not None and self.last_qr_code:
            ret, frame = self.cap.read()
            if ret:

                enhanced_image = self.enhance_image(frame)
                # Save the image with the QR code text as filename
                output_dir = 'captured_images'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_path = os.path.join(output_dir, f"{self.last_qr_code}.png")
                cv2.imwrite(output_path,enhanced_image)
                messagebox.showinfo("Image Saved", f"Image saved to {output_path}")
            else:
                messagebox.showwarning("Capture Error", "Failed to capture image from the camera.")

    def enhance_image(self, image):
        # Convert the image to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to the L channel with adjusted parameters
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        
        # Merge the CLAHE enhanced L channel back to LAB color space
        limg = cv2.merge((cl, a, b))
        
        # Convert back to BGR color space
        enhanced_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        
        # Apply Gaussian blur to reduce sharpness
        enhanced_image = cv2.GaussianBlur(enhanced_image, (3, 3), 0)
        
        return enhanced_image

    def close_camera(self):
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_camera)

    # Center the window on the screen
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    position_x = int((root.winfo_screenwidth() / 2) - (window_width / 2))
    position_y = int((root.winfo_screenheight() / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    root.mainloop()
 # python-primary lang, clahe-contrast limited adaptive histogram equalization-  coverts to high res.
 # each pixel is separately enhanced and then merged together. hence, the high clarity.
 #image stored in the name of the code associated with the board for easy access
 #to guarentee and show the authenticity and quality of the board.
 #this project is to show the proof of work and determine where exactly a potential defect might have occured.