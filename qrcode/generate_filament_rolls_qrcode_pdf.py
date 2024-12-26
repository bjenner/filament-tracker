import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(filename)

def create_qr_sheet(data_list, output_pdf):
    page_width, page_height = letter
    c = canvas.Canvas(output_pdf, pagesize=letter)
    x, y = 50, page_height - 100
    qr_size = 100  # Size of each QR code
    for i, data in enumerate(data_list):
        url = f"http://speeder-pad.local/{data}"
        qr_filename = f"qr_code_{i}.png"
        generate_qr_code(url, qr_filename)
        c.drawImage(qr_filename, x, y, width=qr_size, height=qr_size)
        c.drawString(x, y - 10, data)  # Optional: Label below QR code
        x += qr_size + 20
        if x > page_width - qr_size:
            x = 50
            y -= qr_size + 50
            if y < qr_size:
                c.showPage()
                y = page_height - 100
    c.save()

# Example usage:
database_ids = [f"cam/{i}" for i in range(1, 51)]  # Replace with your unique identifiers
create_qr_sheet(database_ids, "qr_codes_sheet.pdf")

