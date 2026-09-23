from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime

def render_to_pdf(template_src, context_dict={}):
    """
    Generates a PDF from a Django template and returns it as an HTTP response.
    """
    # Load and render the template with context
    template = get_template(template_src)
    html = template.render(context_dict)

    # Generate a timestamped PDF filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    invoice_title = context_dict.get('invoice_title', 'document')
    filename = f"{invoice_title}_{timestamp}.pdf"

    # Create HTTP response with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response['Content-Transfer-Encoding'] = 'binary'

    # Convert HTML to PDF and write to response
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Error handling
    if pisa_status.err:
        return HttpResponse("We had some errors while generating the PDF.<br><pre>" + html + "</pre>")

    return response
