from flask import Flask, request, send_file
from flask_cors import CORS
import pikepdf
import io
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/compress-pdf', methods=['POST'])
def compress_pdf():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Read the PDF file
    pdf_reader = pikepdf.open(file.stream)

    # Create a BytesIO object to hold the compressed PDF
    compressed_pdf = io.BytesIO()

    # Save the PDF with compression
    pdf_reader.save(compressed_pdf)  # No additional parameters needed
    compressed_pdf.seek(0)

    # Send the compressed PDF back to the client
    return send_file(compressed_pdf, as_attachment=True, download_name='compressed.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)  # Listen on all interfaces