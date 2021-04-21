from job.models import Job
from bson import ObjectId
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch, cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from io import StringIO, BytesIO
import re
import os
import json

def get_all_jobs():
    jobs = Job.objects.all().order_by('date_of_job')
    return jobs

def get_single_job(object_id):
    jobresp = Job.objects.get(_id=ObjectId(object_id))
    return jobresp


addressStyle = ParagraphStyle(
    name='Normal_RIGHT',
    fontSize=15,
    alignment=TA_RIGHT
)

dataStyle = ParagraphStyle(
    name='Normal',
    fontSize=15
)


#add data to pdf
def add_data(job):
    document = []
    document.append(get_image('./general/static/general/logosmall.jpg', width=8*cm))
    document.append(Spacer(1, 30))

    if job['issued_by_name'] == 'Michael':
        letter_address_data = os.environ.get('OWNER1_DETAILS')
    elif job['issued_by_name'] == "Andy":
        letter_address_data = os.environ.get('OWNER2_DETAILS')
    #else:
        # do something here
    
    letter_address_data = json.loads(letter_address_data)
    
    for key, value in letter_address_data.items():
        document.append(Paragraph(value, addressStyle))
        document.append(Spacer(1, 5))
    document.append(Spacer(1, 20))

    with open('test_invoice_template.txt') as txt:
        for line in txt.read().split('\n'):
            line = line.replace("\n", "")
            to_replace = re.match(r"^.*\[(.*)\].*$", line)

            if to_replace:
                rep = "[" + to_replace.group(1) + "]"
                dat = job[to_replace.group(1)]               
                line = line.replace(rep, str(dat))
            
            document.append(Paragraph(line, dataStyle))
            document.append(Spacer(1, 12))
    
    return document


#construct and output pdf
def create_pdf(job):
    buffer = BytesIO()
    SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMrgin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=6).build(add_data(job)
    )
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


#to get logo and keep original aspect ratio
def get_image(path, width):
    img = ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))
