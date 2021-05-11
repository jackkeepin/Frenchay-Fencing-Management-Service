from job.models import Job
from bson import ObjectId
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from io import BytesIO
import re

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

materialStyle = ParagraphStyle(
    name='Material',
    fontSize=15,
    leftIndent=50
)


def add_data(job):
    """
    Add all the data from the job to the pdf.
    """
    document = []
    document.append(get_image('./general/static/general/img/logosmall.jpg', width=8*cm))
    document.append(Spacer(1, 30))
    
    owner_split_address = job['issued_by_address'].split(',')
    owner_street = owner_split_address[0].lstrip()
    owner_city = owner_split_address[1].lstrip()
    owner_post_code = owner_split_address[2].lstrip()

    # format to be used for owner address 
    letter_owner_address_data = {
        'business': 'Frenchay Fencing',
        'name': job['issued_by_first_name'] + ' ' + job['issued_by_last_name'],
        'street': owner_street,
        'city': owner_city,
        'post_code': owner_post_code,
        'number': job['issued_by_number']
    }

    customer_split_address = job['address'].split(',')
    customer_street = customer_split_address[0].lstrip()
    customer_city = customer_split_address[1].lstrip()
    customer_post_code = customer_split_address[2].lstrip()

    # format to be used for owner address 
    letter_customer_address_data = {
        'name': job['customer_first_name'] + ' ' + job['customer_last_name'],
        'street': customer_street,
        'city': customer_city,
        'post_code': customer_post_code,
        'number': job['customer_phone_num']
    }
    
    # add owner address to pdf
    for key, value in letter_owner_address_data.items():
        document.append(Paragraph(value, addressStyle))
        document.append(Spacer(1, 5))
    document.append(Spacer(1, 20))


    for key, value in letter_customer_address_data.items():
        document.append(Paragraph(value, dataStyle))
        document.append(Spacer(1, 5))

    document.append(Spacer(1, 30))

    # replace placeholders in template with data
    with open('invoice_template.txt') as txt:
        for line in txt.read().split('\n'):
            line = line.replace("\n", "")
            to_replace = re.match(r"^.*\[(.*)\].*$", line)

            #get placeholder and replace it with data
            if to_replace:
                rep = "[" + to_replace.group(1) + "]"
                dat = job[to_replace.group(1)]

                #if adding date to pdf, format date
                if rep == '[date_of_job]':
                    dat = dat.strftime("%d %B %Y")
                    line = line.replace(rep, dat)
                    document.append(Paragraph(line, dataStyle))
                    document.append(Spacer(1, 30))

                # if adding materials to pdf, format differently
                elif rep == '[materials]': 
                    materials = dat.splitlines()
                    line = line.replace(rep, "")
                    document.append(Paragraph(line, dataStyle))
                    document.append(Spacer(1, 4))

                    for material in materials:
                        document.append(Paragraph(material, materialStyle))
                        document.append(Spacer(1, 10))
                    document.append(Spacer(1, 30))
                
                # if removal_included is False, do not display price on invoice
                elif rep == '[removal_included]':
                    if dat == True:
                        dat = "Yes"
                        line = line.replace(rep, dat)
                        price_of_removal_line = "Price of removal: " + job['price_of_removal']
                        document.append(Paragraph(line, dataStyle))
                        document.append(Spacer(1, 30))
                        document.append(Paragraph(price_of_removal_line, dataStyle))
                        document.append(Spacer(1, 30))
                    else:
                        dat = "No"
                        line = line.replace(rep, dat)
                        document.append(Paragraph(line, dataStyle))
                        document.append(Spacer(1, 30))    
                
                # if adding anything but materials, format normally
                else:
                    line = line.replace(rep, str(dat))
                    document.append(Paragraph(line, dataStyle))
                    document.append(Spacer(1, 30))
    
    return document


def create_pdf(job):
    """
    Construct and output pdf.
    """

    # create and use buffer so pdf is saved in an in-memory buffer
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


def get_image(path, width):
    """
    Get image to diplay on pdf at original aspect ratio
    """
    img = ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

