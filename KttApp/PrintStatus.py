from reportlab.pdfgen import canvas
import io
from .models import * 
from django.http import HttpResponse
from reportlab.platypus import Table, TableStyle ,Paragraph
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet


def PrintStatus(request,PermitId):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(595, 841))

    can.setFont('Times-Roman', 9)
    can.drawString(480, 820, "PG : 1 OF 1")
    

    Inheader = InheaderTbl.objects.get(PermitId=PermitId)
    Import = Importer.objects.get(code=Inheader.ImporterCompanyCode)
    Loading = LoadingPort.objects.get(portcode=Inheader.LoadingPortCode)
    style = getSampleStyleSheet()['Normal']
    style.fontName = 'Times-Roman'  # Set the font family
    style.fontSize = 9
    style.spaceBefore = 0 
    

    rejectStatus = [['SERIAL NO ','CODE','MESSAGE']]
    TitleStatus = ''
    if Inheader.Status == "REJ":
        y_ax = 430
        filename = "RejectStatus"
        TitleStatus = 'REJECTION MESSAGE'
        for re in RejectStatus.objects.filter(MsgId=Inheader.MSGId,MailBoxId = Inheader.TradeNetMailboxID).order_by("Sno"):
            rejectStatus.append([Paragraph(str(re.Sno),style),Paragraph(str(re.ErrorId),style),Paragraph(re.ErrorDescription,style)])
    elif Inheader.Status == "QRY":
        y_ax = 430
        filename = "QUERY_STATUS"
        TitleStatus = 'QUERY MESSAGE'
        for re in RejectStatus.objects.filter(MsgId=Inheader.MSGId,MailBoxId = Inheader.TradeNetMailboxID).order_by("Sno"):
            rejectStatus.append([Paragraph(str(re.Sno),style),Paragraph(str(re.ErrorId),style),Paragraph(re.ErrorDescription,style)])
    elif Inheader.Status == "CNL":
        filename = f"Cancellation_{Inheader.PermitNumber}"
        TitleStatus = 'CANCELLATION MESSAGE'
        can.rect(50, 460, 500, 50)
        InpayCancel = InpaymentCancel.objects.get(PermitNo=Inheader.PermitNumber)
        can.drawString(60, 490, f"CANCELLATION REASON : {((InpayCancel.ResonForCancel).upper())[:4]}")
        can.drawString(60, 475, f"DESCRIPTION OF REASON : {(InpayCancel.DescriptionOfReason).upper()}")
        y_ax = 370
        for re in InCancel.objects.filter(MsgId=Inheader.MSGId,MailBoxId = Inheader.TradeNetMailboxID).order_by("Sno"):
            rejectStatus.append([Paragraph(str(re.Sno),style),Paragraph(str(re.ConditionCde),style),Paragraph(re.ConditionDes,style)])
    can.setFont('Times-Bold', 10)
    can.drawString(250, 790, TitleStatus)
    can.setFont('Times-Roman', 9)
    coveyance = ''
    Obl_hawb = ''
    InTransportId = ''
    if ((Inheader.InwardTransportMode)[4:]).upper() == "SEA":
        Obl_hawb = Inheader.OceanBillofLadingNo
        coveyance = Inheader.VoyageNumber
        InTransportId = Inheader.VesselName
    elif ((Inheader.InwardTransportMode)[4:]).upper() == "AIR":
        Obl_hawb = Inheader.MasterAirwayBill
        coveyance = Inheader.FlightNO
        InTransportId = Inheader.VesselName


    can.rect(50, 530, 500, 250)

    can.drawString(60, 760, "MESSAGE TYPE : IN-PAYMENT DECLARATION ")
    can.drawString(60, 745, f"DECLARATION TYPE : {Inheader.DeclarationType}")
    can.drawString(60, 730, f"COMPANY UEN : {Import.cruei}")
    can.drawString(60, 715, f"COMPANY NAME : {Import.name}")
    can.drawString(60, 700, f"PORT OF LOADING : {Loading.portname}")
    can.drawString(60, 685, "PORT OF DISCHARGE : ")
    can.drawString(60, 670, "DESTINATION COUNTRY : ")

    can.drawString(60, 655, f"IN TRANSPORT ID : {InTransportId}")
    can.drawString(60, 640, f"ARRIVAL DATE : {datetime.strptime(str(Inheader.ArrivalDate), '%Y-%m-%d').strftime('%d-%m-%Y')}")
    can.drawString(60, 625, f"CONVEYANCE NO : {coveyance}")
    can.drawString(60, 610, f"MAWB / OBL : {Obl_hawb}")
    can.drawString(60, 595, "OUT TRANSPORT ID :")
    can.drawString(60, 580, "DEPARTURE DATE :")
    can.drawString(60, 565, "CONVEYANCE NO :")
    can.drawString(60, 550, "MAWB / OBL :")
    createDate = (Inheader.TouchTime).strftime("%d-%m-%Y")
    can.drawString(310, 760, f"CREATE DATE : {createDate}")
    can.drawString(310, 745, f"MESSAGE ID : {Inheader.MSGId}")
    can.drawString(310, 730, f"PERMIT NUMBER : {Inheader.PermitNumber}")
    can.drawString(310, 715, f"PREVIOUS PERMIT : {Inheader.PreviousPermit}")
    can.drawString(310, 700, f"PLACE OF RELEASE : {Inheader.ReleaseLocName}")
    can.drawString(310, 685, f"PLACE OF RECEIPT : {Inheader.RecepitLocName}")
    can.drawString(310, 670, f"TOTAL OUTER PACKAGE : {Inheader.TotalOuterPack}/{Inheader.TotalOuterPackUOM}")
    can.drawString(310, 655, f"TOTAL GROSS WEIGHT : {Inheader.TotalGrossWeight}/{Inheader.TotalGrossWeightUOM}")
    can.drawString(310, 640, f"NUMBER OF ITEMS : {len(ItemDtl.objects.filter(PermitId = PermitId))}")

    col_widths = [90, 70, 340]
    table = Table(rejectStatus,colWidths=col_widths)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('COLWIDTHS', (2, -1), (-1, -1), 102),
        ('GRID', (0, 0), (-1, -1), 1, colors.black), 
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('SPLITLONGWORDS', (0, 0), (-1, -1), 1), 
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    table.wrapOn(can, 0, 0)
    table.drawOn(can, 50, y_ax)
    can.showPage()
    can.save()

    packet.seek(0)
    response = HttpResponse(packet, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}{(datetime.now()).strftime("%d-%m-%Y %H:%M")}.pdf"'

    return response