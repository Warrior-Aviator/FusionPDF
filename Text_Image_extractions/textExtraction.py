# Import required dependencies
import fitz
import os
import json
from PIL import Image

# Define the path to the PDF file
pdf_path = r"documents\TranslatedDemo1.pdf"
new_pdf_path = r"d.pdf"

# Define default font style for the new PDF
default_font = "NotoSansKannada"

# Define the path to the Noto Sans Kannada TTF file
noto_sans_kannada_path = r"NotoSansKannada-VariableFont_wdth,wght.ttf"

# Load the font into a buffer
with open(noto_sans_kannada_path, "rb") as font_file:
    font_buffer = font_file.read()

# Create a document object
doc = fitz.open(pdf_path)

# Create a new PDF document
new_doc = fitz.open()

# Extract the number of pages
print(f"Number of pages: {doc.page_count}")

# Extract metadata
print("Metadata:", doc.metadata)

# Define the path to the output JSON file
output_json_path = r"extracted_text_with_coordinates.json"

# Dictionary to store text with coordinates
extracted_data = {}

# Iterate through all pages
for i in range(doc.page_count):
    # Get the page
    page = doc.load_page(i)  # or page = doc[i]
    # Get the original page
    original_page = doc.load_page(i)
    
    # Create a new page with the same size as the original page
    new_page = new_doc.new_page(width=original_page.rect.width, height=original_page.rect.height)
    
    # Extract text blocks from the page
    blocks = page.get_text_blocks()
    
    # List to store text and coordinates for the current page
    page_data = []

    for b in blocks:
        # Extract text and coordinates
        text = b[4]
        x0, y0, x1, y1 = b[:4]

        # Check if text contains multiple '\n'
        if text.count('\n') >= 1:
            # Multiply the coordinates by 0.5
            z = 999
            #x0 *= 0.5
            #y0 *= 0.5
            #x1 *= 0.5
            #y1 *= 0.5
        else:
            # Multiply the coordinates by 1.5 to expand the text box area
            x0 *= 1.5
            y0 *= 1.5
            x1 *= 1.5
            y1 *= 1.5

        # Append to the result
        page_data.append({
            "text": text,
            "coordinates": {
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1
            }
        })

        # Draw text on the new page with default font style
        new_page.insert_text((x0, y0), text, fontname=default_font, fontfile=noto_sans_kannada_path, fontsize=9, color=(0, 0, 0))
    
    # Add the page data to the extracted data dictionary
    extracted_data[f"page_{i + 1}"] = page_data

# Save the new PDF document
new_doc.save(new_pdf_path)

# Save the extracted data to a JSON file
with open(output_json_path, "w", encoding="utf-8") as json_file:
    json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)

# Close all documents
doc.close()
new_doc.close()

print(f"Text with coordinates has been saved to {output_json_path}")
print(f"New PDF has been saved to {new_pdf_path}")
