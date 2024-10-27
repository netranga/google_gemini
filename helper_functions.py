import os
import pandas as pd
import PyPDF2
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from google.generativeai import caching
import datetime

def write_transcripts_to_files(df):
    """
    Function to write transcripts to individualtext files
    """

    output_dir = '/Users/netraranga/Desktop/Projects/google_gemini/docs/transcripts'
    os.makedirs(output_dir, exist_ok=True)
    

    for index, row in df.iterrows():
        # Create a filename based on the lecture number
        filename = f"lecture_{row['Lecture']}_transcript.txt"
        file_path = os.path.join(output_dir, filename)
        

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(row['Video Contents'])
        
        print(f"Transcript for Lecture {row['Lecture']} written to {file_path}")

def create_title_page(title):
    """
    Helper function to create title pages for the PDFs
    """

    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 24)
    can.drawString(100, 400, title)
    can.save()
    packet.seek(0)
    return PyPDF2.PdfReader(packet)

def merge_annotated_slides(combined_annotated_slides):
    """
    Helper function to merge regular lecture slides and annotated slides
    """

    docs_folder = '/Users/netraranga/Desktop/Projects/google_gemini/docs'
    consolidated_folder = os.path.join(docs_folder, 'consolidated')

    output_files = []
    
    for base_name in combined_annotated_slides:
        merger = PyPDF2.PdfMerger()
        original_file = os.path.join(docs_folder, f"{base_name}.pdf")
        annotated_file = os.path.join(docs_folder, f"{base_name}_annotated.pdf")
        
        # Add title page and original slides
        original_title = create_title_page(f"Original {base_name} Slides")
        merger.append(original_title)
        merger.append(original_file)
        
        # Add title page and annotated slides
        annotated_title = create_title_page(f"Annotated {base_name} Slides")
        merger.append(annotated_title)
        merger.append(annotated_file)
        
        # Output PDF file name
        output_pdf = os.path.join(consolidated_folder, f'combined_{base_name}_slides.pdf')
        
        try:
            merger.write(output_pdf)
            print(f"PDFs merged successfully for {base_name}. Output file: {output_pdf}")
            output_files.append(output_pdf)
        except Exception as e:
            print(f"Error writing output file for {base_name}: {str(e)}")
        finally:
            merger.close()
    
    return output_files

def create_cache(name, contents, time=10):
    """
    Create a cache for the gemini model
    """
    custom_cache = caching.CachedContent.create(
    model='models/gemini-1.5-flash-002',
    display_name=name,
    system_instruction=("""You are an expert tutor specializing in machine learning, with comprehensive knowledge of the Stanford CS229 "Introduction to Machine Learning" course. You have access to all relevant materials, including:
    - Annotated and regular lecture notes for each session.
    - Transcripts of all recorded lectures.
    - The complete course textbook.
    Your role is to guide the user through the CS229 course material by:
    1. **Providing clear, detailed explanations** of key machine learning concepts and algorithms, from foundational topics like linear regression and classification to advanced areas such as support vector machines and unsupervised learning.
    2. **Connecting course concepts**, explaining how different topics (e.g., gradient descent, regularization) relate and build upon each other across lectures.
    3. **Summarizing lectures and sections**, highlighting major takeaways, essential equations, and conceptual insights.
    4. **Supporting exam preparation**, identifying high-impact topics, common pitfalls, and suggesting areas for further review."""),
    contents=contents,
    ttl=datetime.timedelta(minutes=time))

    return custom_cache


def gemini_response(cache, question):
    """
    Function to generate a response from the gemini model
    """
    model = genai.GenerativeModel.from_cached_content(cached_content=cache)
    response = model.generate_content([(question)])
    return response