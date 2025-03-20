import os
import pdfplumber

def find_pdfs(directory):
    """Recursively find all PDF files in the directory, ignoring files ending with '-Sols'."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf") and not file.endswith("Solns.pdf"):
                yield os.path.join(root, file)

def search_pdf(file_path, keyword):
    """Search for a keyword in a PDF and return the pages it appears on."""
    pages_with_keyword = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and keyword in text:
                    pages_with_keyword.append(i + 1)
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {str(e)}")
    return pages_with_keyword

def main(directory, keyword):
    results = {}
    for pdf_path in find_pdfs(directory):
        print(f"Processing {os.path.basename(pdf_path)}...")  # Display just the file name
        pages = search_pdf(pdf_path, keyword)
        if pages:
            results[os.path.basename(pdf_path)] = pages

    # Print results in an aligned list
    if results:
        print("\nResults:")
        print("{:<40} {:<10}".format("File Name", "Pages"))
        for file_name, pages in results.items():
            print("{:<40} {:<10}".format(file_name, ', '.join(map(str, pages))))
    else:
        print("No PDFs found with the specified keyword.")

if __name__ == '__main__':
    directory = input("Enter the directory path: ")
    keyword = input("Enter the keyword to search for: ")
    main(directory, keyword)
