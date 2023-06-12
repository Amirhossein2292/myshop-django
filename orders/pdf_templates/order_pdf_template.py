from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        # Add header logic
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Order PDF", 0, 1, "C")

    def footer(self):
        # Add footer logic
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page %s/{nb}" % self.page_no(), 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, title, ln=True, align="L")

    def chapter_body(self, text):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)
        self.ln(5)


def generate_order_pdf(order):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add order information
    pdf.chapter_title("Order Information")
    pdf.chapter_body("Order ID: " + order.order_id)
    pdf.chapter_body("User: " + order.user.username)
    pdf.chapter_body("Created at: " + str(order.created_at))
    pdf.chapter_body("Billing Address: " + order.billing_address_line_1)
    pdf.chapter_body("Note: " + order.note)
    pdf.chapter_body("City: " + order.get_city_display())
    pdf.chapter_body("Postal Code: " + order.postal_code)
    pdf.chapter_body("Status: " + order.get_status_display())
    pdf.chapter_body("Is Paid: " + str(order.is_paid))
    pdf.chapter_body("Telephone Number: " + str(order.telephone_number))
    pdf.chapter_body("Total: " + order.total)

    # Add order items
    pdf.chapter_title("Order Items")
    for item in order.order_items.all():
        pdf.chapter_body("Product: " + item.product.name)
        pdf.chapter_body("Quantity: " + str(item.quantity))
        pdf.chapter_body("Subtotal: " + item.subtotal())

    return pdf.output(dest="S").encode("latin-1")
