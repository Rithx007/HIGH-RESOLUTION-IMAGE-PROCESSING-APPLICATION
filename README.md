# HIGH-RESOLUTION-IMAGE-PROCESSING-APPLICATION
High Resolution image processing using CLAHE (Contrast Limited Adaptive Histogram Equalization) to enhance the resolution of the image while preserving the color information.  This tool is intended to help verify the  quality and authenticity of PCB boards, in scenarios where boards are damaged during transit and to handle customer complaints.
Technologies Used: 
• Python: The primary programming language used for the application development. 
• CLAHE (Contrast Limited Adaptive Histogram Equalization): An image processing 
technique used to enhance the contrast of images while preserving color 
information. 
Process: 
1. Barcode Scanning: 
o The process begins with a barcode scanner that scans the SFC (Shop Floor 
Control) code of the circuit board. This SFC code serves as a unique identifier 
for each board. 
o Upon scanning, the code is provided as input to the software via a dialog box. 
2. Image Capture: 
o An external camera connected through a cord is automatically activated upon 
the scanning of the SFC code. 
o The camera captures a high-resolution image of the circuit board when the 
"Capture" button is pressed in the application. 
3. Image Processing: 
o The captured image undergoes processing using the CLAHE technique. CLAHE 
enhances the image by adjusting the contrast of each pixel independently, 
ensuring that the intensity of the image is improved without losing any color 
information. 
o The enhancement is done in such a way that the finer details of the circuit 
board are more visible, making it easier to detect any defects or irregularities. 
4. Image Storage: 
o After processing, the high-resolution image is stored either in the cloud or 
locally. The filename of the stored image corresponds to the previously 
scanned SFC code, ensuring that each image can be easily matched with its 
respective circuit board. 
o This stored image can be used as proof of work, providing a visual record of 
the board's condition at the time of production. 
Applications and Benefits: 
• Quality Verification: When a PCB board is damaged during transit or otherwise, the 
stored high-resolution images can be used to verify the board's authenticity and 
quality. 
• Customer Complaints: In cases where customers raise complaints about the quality 
of the circuit boards, these images serve as valuable evidence to address and resolve 
the issues. 
• Documentation: The process provides a systematic method for documenting the 
condition of each circuit board, which is essential for maintaining quality control 
standards.
