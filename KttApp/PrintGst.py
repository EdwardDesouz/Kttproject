from reportlab.pdfgen import canvas
import io
from .models import *
from django.http import HttpResponse
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from django.db.models import Count


def PrintGst(request, PermitId):

    for invoiceD in InvoiceDtl.objects.filter(PermitId=PermitId):
        Import = Importer.objects.get(code=invoiceD.ImportPartyCode)
    Inheader = InheaderTbl.objects.get(PermitId=PermitId)
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(595, 841))

    can.setFont('Times-Bold', 9)
    x = 10
    y = 820
    can.drawString(200, y, "GOODS AND SERVICE TAX (GST) - CALCULATION SHEET")
    y -= 20
    can.drawString(x, y, "COMPANY NAME:")
    can.drawString(x+440, y, "JOB NUMBER:")
    y -= 15
    can.drawString(x, y, "COMPANY UEN:")
    can.drawString(x+440, y, "JOB CREATED:")
    y -= 15
    can.drawString(x, y, "PERMIT NUMBER:")
    can.drawString(x+440, y, "MESSAGE ID:")

    can.setFont('Times-Roman', 9)
    x = 100
    y = 820
    y -= 20
    can.drawString(x, y, Import.name)
    can.drawString(x+420, y, Inheader.JobId)
    y -= 15
    can.drawString(x, y, Import.cruei)
    can.drawString(
        x+410, y, (Inheader.TouchTime).strftime("%d/%m/%Y  %H:%M:%S"))
    y -= 15
    can.drawString(x, y, Inheader.PermitNumber)
    can.drawString(x+420, y, Inheader.MSGId)
    x = 10
    for invoiceD in InvoiceDtl.objects.filter(PermitId=PermitId):
        can.setFont('Times-Bold', 9)
        y -= 25
        can.drawString(x, y, "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        y -= 15
        can.drawString(x, y, "INVOICE NUMBER:")
        y -= 15
        can.drawString(x, y, "INVOICE TERM:")
        can.setFont('Times-Roman', 9)
        y -= 15
        can.drawString(x+100, y+30, invoiceD.InvoiceNo)
        y -= 15
        can.drawString(x+80, y+30, invoiceD.TermType)

        rejectStatus = [['SNO', 'ITEM', "CURRENCY",
                         "EXCHG. RATE", "PERC.", "AMOUNT", "AMOUNT (SGD)"]]
        rejectStatus.append(["1", 'TOTAL INVOICE', ((invoiceD.TICurrency) if '--Select--' != (
            invoiceD.TICurrency) else ""), invoiceD.TIExRate, "", invoiceD.TIAmount, invoiceD.TISAmount])

        rejectStatus.append(["2", 'FREIGHT CHARGES', ((invoiceD.FCCurrency) if '--Select--' != (invoiceD.FCCurrency)
                            else ""), invoiceD.FCExRate, invoiceD.FCCharge, invoiceD.FCAmount, invoiceD.FCSAmount])

        rejectStatus.append(["3", 'INSURANCE', ((invoiceD.ICCurrency) if '--Select--' != (invoiceD.ICCurrency)
                            else ""), invoiceD.ICExRate, invoiceD.ICCharge, invoiceD.ICAmount, invoiceD.ICSAmount])

        rejectStatus.append(["4", 'OTHER CHARGES', ((invoiceD.OTCCurrency) if '--Select--' != (invoiceD.OTCCurrency)
                            else ""), invoiceD.OTCExRate, invoiceD.OTCCharge, invoiceD.OTCAmount, invoiceD.OTCSAmount])

        rejectStatus.append(["5", 'CUSTOMS VALUE', "", "",
                            "", "", invoiceD.CIFSUMAmount])

        rejectStatus.append(
            ["6", 'GST', "", "", invoiceD.GSTPercentage, "", invoiceD.GSTSUMAmount])

        col_widths = [80, 90, 80, 80, 80, 80]
        table = Table(rejectStatus, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('COLWIDTHS', (2, -1), (-1, -1), 102),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPLITLONGWORDS', (0, 0), (-1, -1), 1),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        table.wrapOn(can, 0, 0)
        table.drawOn(can, 10, y-120)
        y -= 120

    can.save()
    packet.seek(0)
    response = HttpResponse(packet, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{Inheader.PermitNumber}_GST.pdf"'

    return response
