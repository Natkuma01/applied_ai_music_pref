from weasyprint import HTML
import os

# Get the directory where this script is located
base_dir = '/Users/nataliechan/Desktop/codePath/AI101/final/applied_ai_music_pref'
html_file = os.path.join(base_dir, 'DataFlow_Diagram.html')
pdf_file = os.path.join(base_dir, 'DataFlow_Diagram.pdf')

# Convert HTML to PDF
try:
    HTML(html_file).write_pdf(pdf_file)
    print(f"PDF created successfully: {pdf_file}")
except Exception as e:
    print(f"Error creating PDF: {e}")
