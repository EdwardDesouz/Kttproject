from django.http import HttpResponse
from .models import *
from reportlab.pdfgen import canvas
import io
from reportlab.graphics.barcode import code39
from PyPDF2 import PdfFileWriter, PdfFileReader
import os

def PdfCcp(request, Data):
    global itemy, p, countPage
    pdfFiles = []
    pdfWriter = PdfFileWriter()
    for PermitId in Data.split(','):
        lftcol = 50
        rgtcol = 280
        countPage = 1

        Inheader = InheaderTbl.objects.get(PermitId=PermitId)
        Impo = Importer.objects.get(code=Inheader.ImporterCompanyCode)
        loadingPort = LoadingPort.objects.get(portcode=Inheader.LoadingPortCode)
        try:
            InwardCarrier = InwardCarrierAgent.objects.get(code=Inheader.InwardCarrierAgentCode)
            InwardCarrierName = InwardCarrier.name+InwardCarrier.name1
        except:
            InwardCarrierName = ""

        Cpc = CpcDtl.objects.filter(PermitId=PermitId).values('CpcType').distinct()
        Declarant = DeclarantCompany.objects.get(tradenetmailboxId=Inheader.TradeNetMailboxID)
        try:
            for inp in Inpmt.objects.filter(PermitNumber=Inheader.PermitNumber):
                inpstrtdate = datetime.strptime(str(inp.StartDate), '%Y-%m-%d').strftime('%d/%m/%Y')
                inpEndate = datetime.strptime(str(inp.EndDate), '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception as e:
            inpmtD = ""

        importerName = Impo.name+Impo.name1

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=(595, 841))
        if Inheader.PermitNumber == " " or Inheader.PermitNumber == "":
            draft = "DRAFT"
            inpstrtdate = ""
            inpEndate = ""
        else:
            draft = Inheader.PermitNumber
            barcode = code39.Standard39(draft, barHeight=36.0, barWidth=1.1, baseline=9.0,size=12.0, N=3.0, X=1.0, StartsStopText=False, Extended=False)
            barcode.drawOn(p, 330, 760)

        p.setFont('Courier-Bold', 10)
        p.drawString(480, 750, draft)

        p.setFont('Courier', 10)
        p.drawString(400, 750, "PERMIT NO : ")

        p.drawString(rgtcol, 700, "CARGO CLEARANCE PERMIT")
        p.drawString(460, 700, ("PG : {} OF").format(countPage))
        countPage += 1

        p.drawString(lftcol, 670, "MESSAGE TYPE      : IN-PAYMENT PERMIT")
        p.drawString(lftcol, 660, "DECLARATION TYPE  : " + (str(Inheader.DeclarationType)[6:]).upper())

        p.drawString(lftcol, 630, "IMPORTER:")
        if len(importerName) >= 35:
            p.drawString(lftcol, 620, (importerName[:35]).upper())
            p.drawString(lftcol, 610, (importerName[35:]).upper())
        else:
            p.drawString(lftcol, 620, (importerName).upper())

        p.drawString(lftcol, 600, (Impo.cruei).upper())
        p.drawString(lftcol, 590, "EXPORTER:")
        p.drawString(lftcol, 580, " ")
        p.drawString(lftcol, 570, " ")
        p.drawString(lftcol, 560, " ")
        p.drawString(lftcol, 550, "HANDLING AGENT: ")
        p.drawString(lftcol, 540, " ")
        p.drawString(lftcol, 530, " ")
        p.drawString(lftcol, 520, " ")
        p.drawString(lftcol, 510, " ")
        p.drawString(lftcol, 500, "PORT OF LOADING/NEXT PORT OF CALL:")
        p.drawString(lftcol, 490, (loadingPort.portname).upper())
        p.drawString(lftcol, 480, "PORT OF DISCHARGE/FINAL PORT OF CALL ")
        p.drawString(lftcol, 470, " ")
        p.drawString(lftcol, 460, "COUNTRY OF FINAL DESTINATION:")
        p.drawString(lftcol, 450, " ")
        p.drawString(lftcol, 440, "INWARD CARRIER AGENT: ")

        if len(InwardCarrierName) >= 35:
            p.drawString(lftcol, 430, (InwardCarrierName[:35]).upper())
            p.drawString(lftcol, 420, (InwardCarrierName[35:70]).upper())
            p.drawString(lftcol, 410, (InwardCarrierName[70:]).upper())
        else:
            p.drawString(lftcol, 430, (InwardCarrierName).upper())
        p.drawString(lftcol, 400, "OUTWARD CARRIER AGENT: ")
        p.drawString(lftcol, 390, " ")
        p.drawString(lftcol, 380, " ")
        p.drawString(lftcol, 370, " ")
        p.drawString(lftcol, 360, "PLACE OF RELEASE: ")
        rely = 350
        relVal = (Inheader.ReleaseLocName).upper()
        chr = 0
        if len(relVal) >= 32:
            for i in range(len(relVal)):
                if (i+1) % 32 == 0:
                    p.drawString(lftcol, rely, relVal[chr:i])
                    chr = i+1
                    rely -= 10
            else:
                p.drawString(lftcol, rely, relVal[chr:])
                rely -= 100
        else:
            p.drawString(lftcol, rely, relVal)
            rely = rely-10
        p.drawString(lftcol, rely, Inheader.ReleaseLocation)
        p.drawString(lftcol, 250, "LICENCE NO:")
        licence = ((Inheader.License).upper()).split(',')

        p.drawString(lftcol, 240, licence[0])
        p.drawString(lftcol, 230, licence[1])
        p.drawString(lftcol, 220, licence[2])
        p.drawString(lftcol, 210, licence[3])
        p.drawString(lftcol, 200, licence[4])
        p.drawString(
            lftcol, 50,  "--------------------------------------------------------------------------------")
        p.drawString(lftcol, 40,  ("UNIQUE REF : {} {} {}").format((Declarant.cruei).upper(), (Inheader.MSGId[:8]).upper(), (Inheader.MSGId[8:]).upper()))

        rgy = 630
        p.drawString(rgtcol, rgy, ("VALIDITY PERIOD      : {} - ").format(inpstrtdate))
        rgy -= 10
        p.drawString(rgtcol, rgy, ("                       {}").format(inpEndate))
        rgy -= 20

        totalGross = "{:.3f}".format(float(Inheader.TotalGrossWeight))

        p.drawString(rgtcol, rgy, ("TOTAL GROSS WT/UNIT  : {:>18}/{}").format(totalGross, Inheader.TotalGrossWeightUOM))
        rgy -= 10
        p.drawString(rgtcol, rgy, ("TOTAL OUTER PACK/UNIT: {:>18}/{}").format(Inheader.TotalOuterPack, Inheader.TotalOuterPackUOM))
        rgy -= 10
        p.drawString(rgtcol, rgy, ("TOT EXCISE DUT PAYABLE  : S${:>17}").format(Inheader.TotalExDutyAmt))
        rgy -= 10
        p.drawString(rgtcol, rgy, ("TOT CUSTOMS DUT PAYABLE : S${:>17}").format(Inheader.TotalCusDutyAmt))
        rgy -= 10
        p.drawString(rgtcol, rgy, ("TOT OTHER TAX PAYABLE   : S${:>17}").format(Inheader.TotalODutyAmt))
        rgy -= 10
        p.drawString(rgtcol, rgy, ("TOTAL GST AMT           : S${:>17}").format(Inheader.TotalGSTTaxAmt))
        rgy -= 10
        p.drawString(rgtcol, rgy, ("TOTAL AMOUNT PAYABLE    : S${:>17}").format(Inheader.TotalAmtPay))
        rgy -= 10
        p.drawString(rgtcol, rgy, ("CARGO PACKING TYPE: {} ").format(((Inheader.CargoPackType)[3:]).upper()))
        rgy -= 10
        p.drawString(rgtcol, rgy, "IN TRANSPORT IDENTIFIER: ")
        rgy -= 10
        if ((Inheader.InwardTransportMode)[4:]).upper() == "SEA" or ((Inheader.InwardTransportMode)[4:]).upper == "AIR":
            transId = Inheader.VesselName
        else:
            transId = Inheader.TransportId

        if ((Inheader.InwardTransportMode)[4:]).upper() == "SEA":
            CoveyanceNo = Inheader.VoyageNumber
        elif ((Inheader.InwardTransportMode)[4:]).upper() == "AIR":
            CoveyanceNo = Inheader.FlightNO
        else:
            CoveyanceNo = Inheader.ConveyanceRefNo
        p.drawString(rgtcol, rgy, transId.upper())
        rgy -= 10
        p.drawString(rgtcol, rgy, ("CONVEYANCE REFERENCE NO: {} ").format(CoveyanceNo.upper()))
        rgy -= 10
        p.drawString(rgtcol, rgy, "OBL/MAWB NO: ")
        rgy -= 10
        p.drawString(rgtcol, rgy, Inheader.OceanBillofLadingNo)
        rgy -= 10
        p.drawString(rgtcol, rgy, "ARRIVAL DATE         : {}".format((Inheader.ArrivalDate).strftime('%d/%m/%Y')))
        rgy -= 10
        p.drawString(rgtcol, rgy, "OU TRANSPORT IDENTIFIER: ")
        rgy -= 10
        p.drawString(rgtcol, rgy, " ")
        rgy -= 10
        p.drawString(rgtcol, rgy, "CONVEYANCE REFERENCE NO:  ")
        rgy -= 10
        p.drawString(rgtcol, rgy, "OBL/MAWB/UCR NO: ")
        rgy -= 10
        p.drawString(rgtcol, rgy, " ")
        rgy -= 10
        p.drawString(rgtcol, rgy, "DEPARTURE DATE       : ")
        rgy -= 20

        p.drawString(rgtcol, rgy, "CERTIFICATE NO:  ")
        rgy -= 30

        p.drawString(rgtcol, rgy, "PLACE OF RECEIPT:")
        rgy -= 10
        rely = rgy
        recVal = Inheader.RecepitLocName
        chr1 = 0
        if len(recVal) >= 32:
            for i in range(len(recVal)):
                if (i+1) % 32 == 0:
                    p.drawString(rgtcol, rely, recVal[chr1:i])
                    chr1 = i+1
                    rely -= 10
            else:
                p.drawString(rgtcol, rely, recVal[chr1:])
                rely -= 10
        else:
            p.drawString(rgtcol, rely, recVal)
            rely = rely-10
        p.drawString(rgtcol, rely, Inheader.RecepitLocation)
        p.drawString(rgtcol, 250, "CUSTOMS PROCEDURE CODE (CPC) : ")
        rely = 240
        for i in Cpc:
            p.drawString(rgtcol, rely, i['CpcType'])
            rely -= 10
        if Inheader.Cnb == 'true':
            p.drawString(rgtcol, rely, "CNB")
            rely -= 10
        p.drawString(rgtcol, rely, "")

        p.showPage()
        # -----------------------------------------1st page completed-------------------------------------#

        snox = 50
        hscodex = 100
        currentx = 180
        prviousx = 320
        makingx = 50
        cityx = 120
        brandx = 220
        itemy = 820
        def itemyF(itemy):
            global countPage
            if itemy <= 70:
                itemy = 820
                p.showPage()
                p.setFont('Courier', 10)
            else:
                itemy -= 10
            if itemy <= 820 and itemy >= 700:
                p.setFont('Courier', 10)
                p.drawString(rgtcol, itemy, "CARGO CLEARANCE PERMIT ")
                p.drawString(460, itemy, ("PG : {} OF ").format(countPage))
                countPage += 1
                itemy -= 10
                p.drawString(lftcol, itemy, "PERMIT NO : "+draft)
                p.drawString(rgtcol, itemy, "======================")
                itemy -= 10
                p.drawString(rgtcol, itemy, "(CONTINUATION PAGE)")
                itemy -= 20
                p.drawString(lftcol, itemy, "CONSIGNMENT DETAILS")
                itemy -= 10
                p.drawString(
                    lftcol, itemy, "--------------------------------------------------------------------------------")
                itemy -= 10
                p.drawString(snox, itemy, "S/NO ")
                p.drawString(hscodex, itemy, "HS CODE")
                p.drawString(currentx, itemy, "CURRENT LOT NO")
                p.drawString(prviousx, itemy, "PREVIOUS LOT NO")
                itemy -= 10
                p.drawString(makingx, itemy, "MARKING")
                p.drawString(cityx, itemy, "CTY OF ORIGIN")
                p.drawString(brandx, itemy, "BRAND NAME")
                p.drawString(prviousx, itemy, "MODEL")
                itemy -= 10
                # ItemInHAWBOBL = ItemDtl.objects.filter(PermitId=PermitId, InHAWBOBL="").exists()
                for i in ItemDtl.objects.filter(PermitId=PermitId):
                    if i.InHAWBOBL != '':
                        p.drawString(lftcol, itemy, "IN HAWB/HUCR/HBL")
                        p.drawString(prviousx, itemy, "OUT HAWB/HUCR/HBL")
                        itemy -= 10
                        break
                p.drawString(lftcol, itemy, "PACKING/GOODS DESCRIPTION")
                p.drawString(prviousx, itemy, "HS QUANTITY & UNIT ")
                itemy -= 10
                p.drawString(prviousx, itemy, "CIF/FOB VALUE (S$) ")
                itemy -= 10
                for i in ItemDtl.objects.filter(PermitId=PermitId):
                    if float(i.LSPValue) != float("0.00"):
                        p.drawString(prviousx, itemy, "LSP VALUE (S$) ")
                        itemy -= 10
                        break
                p.drawString(prviousx, itemy, 'GST AMOUNT (S$)')
                itemy -= 10
                for i in ItemDtl.objects.filter(PermitId=PermitId):
                    if float(i.TotalDutiableQty) != float("0.0000"):
                        p.drawString(prviousx, itemy, 'DUT QTY/WT/VOL & UNIT')
                        itemy -= 10
                        break
                for i in ItemDtl.objects.filter(PermitId=PermitId):
                    if float(i.ExciseDutyAmount) != float("0.00"):
                        p.drawString(prviousx, itemy, 'EXCISE DUTY PAYABLE (S$)')
                        itemy -= 10
                        break
                for i in ItemDtl.objects.filter(PermitId=PermitId):
                    if float(i.CustomsDutyAmount) != float("0.00"):
                        p.drawString(prviousx, itemy, 'CUSTOMS DUTY PAYABLE(S$)')
                        itemy -= 10
                        break
                for i in ItemDtl.objects.filter(PermitId=PermitId):
                    if float(i.OtherTaxAmount) != float("0.00"):
                        p.drawString(prviousx, itemy, 'OTHER TAX PAYABLE(S$) ')
                        itemy -= 10
                        break
                p.drawString(snox, itemy, 'MANUFACTURER’S NAME ')
                itemy -= 10
                p.drawString( snox, itemy, '-------------------------------------------------------------------------------')
                itemy -= 10
                p.drawString(lftcol, 50,  "--------------------------------------------------------------------------------")
                p.drawString(lftcol, 40,  ("UNIQUE REF : {} {} {}").format(Declarant.cruei, Inheader.MSGId[:8], Inheader.MSGId[8:]))
            return itemy
        for item in ItemDtl.objects.filter(PermitId=PermitId).order_by('ItemNo'):
            itemy = itemyF(itemy)
            p.drawString(snox, itemy, ("   {}").format("%02d" % item.ItemNo))
            p.drawString(hscodex, itemy, str(item.HSCode))
            p.drawString(currentx, itemy, (item.CurrentLot).upper())
            p.drawString(prviousx, itemy, (item.PreviousLot).upper())
            itemy = itemyF(itemy)
            
            if '--SELECT--' != str((item.Making)).upper() and str(item.Making) == "None" :
                p.drawString(makingx, itemy, (str(item.Making)[:2]).upper())
            p.drawString(cityx-40, itemy, (item.Contry).upper())
            p.drawString(brandx-105, itemy, (item.Brand).upper())
            p.drawString(prviousx, itemy, (item.Model).upper())
            itemy = itemyF(itemy)
            if item.InHAWBOBL != '':
                p.drawString(lftcol, itemy, (item.InHAWBOBL).upper())
                itemy = itemyF(itemy)
            ItemDescr = (str(item.Description)).upper()
            if '\n' in ItemDescr:
                itemDesc = ItemDescr.split('\n')
                p.drawString(lftcol, itemy, ((itemDesc)[0]).replace('\r',''))
                p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(item.HSQty), str(item.HSQty).split(".")[1], item.HSUOM))
                itemy = itemyF(itemy)

                p.drawString(lftcol, itemy, ((itemDesc)[1]).replace('\r',''))
                p.drawString(prviousx+100, itemy, ('{:10d}.{}').format( int(item.CIFFOB), str(item.CIFFOB).split(".")[1]))
                itemy = itemyF(itemy)

                if float(item.LSPValue) != float("0.00"):
                    try:p.drawString(lftcol, itemy, ((itemDesc)[2]).repace('\r',''))
                    except:pass
                    p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.LSPValue), str(item.LSPValue).split(".")[1]))
                    itemy = itemyF(itemy)
                else:
                    try:p.drawString(lftcol, itemy, ((itemDesc)[2]).repace('\r',''))
                    except:pass

                p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.GSTAmount), str(item.GSTAmount).split(".")[1]))
                itemy = itemyF(itemy)

                if float(item.TotalDutiableQty) != float("0.0000"):
                    try:p.drawString(lftcol, itemy, ((itemDesc)[3]).repace('\r',''))
                    except:pass
                    p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(item.TotalDutiableQty), str( item.TotalDutiableQty).split(".")[1], item.TotalDutiableUOM))
                    itemy = itemyF(itemy)
                else:
                    if len(itemDesc) >= 3:
                        p.drawString(lftcol, itemy, ((itemDesc)[3]).repace('\r',''))
                        itemy = itemyF(itemy)

                if float(item.ExciseDutyAmount) != float("0.00"):
                    try : p.drawString(lftcol, itemy, ((itemDesc)[4]).repace('\r',''))
                    except:pass
                    p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.ExciseDutyAmount), str(item.ExciseDutyAmount).split(".")[1]))
                    itemy = itemyF(itemy)
                else:
                    if len(itemDesc) >= 4:
                        p.drawString(lftcol, itemy, ((itemDesc)[4]).repace('\r',''))
                        itemy = itemyF(itemy)

                if float(item.CustomsDutyAmount) != float("0.00"):
                    try:p.drawString(lftcol, itemy, ((itemDesc)[5]).repace('\r',''))
                    except:pass
                    p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.CustomsDutyAmount), str(item.CustomsDutyAmount).split(".")[1]))
                    itemy = itemyF(itemy)
                else:
                    if len(itemDesc) >= 5:
                        p.drawString(lftcol, itemy, ((itemDesc)[5]).repace('\r',''))
                        itemy = itemyF(itemy)
                if float(item.OtherTaxAmount) != float("0.00"):
                    try : p.drawString(lftcol, itemy, ((itemDesc)[6]).repace('\r',''))
                    except:pass
                    p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.OtherTaxAmount), str(item.OtherTaxAmount).split(".")[1]))
                    itemy = itemyF(itemy)
                else:
                    if len(itemDesc) >= 6:
                        p.drawString(lftcol, itemy, ((itemDesc)[6]).repace('\r',''))
                        itemy = itemyF(itemy)

            else:
                p.drawString(lftcol, itemy, (ItemDescr)[0:50])
                p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(item.HSQty), str(item.HSQty).split(".")[1], item.HSUOM))
                itemy = itemyF(itemy)

                p.drawString(lftcol, itemy, (ItemDescr)[50:100])
                p.drawString(prviousx+100, itemy, ('{:10d}.{}').format( int(item.CIFFOB), str(item.CIFFOB).split(".")[1]))
                itemy = itemyF(itemy)

                if float(item.LSPValue) != float("0.00"):
                    p.drawString(lftcol, itemy, (ItemDescr)[100:150])
                    p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.LSPValue), str(item.LSPValue).split(".")[1]))
                    itemy = itemyF(itemy)
                else:
                    p.drawString(lftcol, itemy, (ItemDescr)[100:150])

                p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.GSTAmount), str(item.GSTAmount).split(".")[1]))
                itemy = itemyF(itemy)

                if float(item.TotalDutiableQty) != float("0.0000"):
                    p.drawString(lftcol, itemy, (ItemDescr)[150:200])
                    p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(item.TotalDutiableQty), str( item.TotalDutiableQty).split(".")[1], item.TotalDutiableUOM))
                    itemy = itemyF(itemy)
                else:
                    if len(ItemDescr) >= 150:
                        p.drawString(lftcol, itemy, (ItemDescr)[150:200])
                        itemy = itemyF(itemy)

                if float(item.ExciseDutyAmount) != float("0.00"):
                    p.drawString(lftcol, itemy, (ItemDescr)[200:250])
                    p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.ExciseDutyAmount), str(item.ExciseDutyAmount).split(".")[1]))
                    itemy = itemyF(itemy)
                else:
                    if len(ItemDescr) >= 200:
                        p.drawString(lftcol, itemy, (ItemDescr)[200:250])
                        itemy = itemyF(itemy)

                if float(item.CustomsDutyAmount) != float("0.00"):
                    p.drawString(lftcol, itemy, (ItemDescr)[250:300])
                    p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.CustomsDutyAmount), str(item.CustomsDutyAmount).split(".")[1]))
                    itemy = itemyF(itemy)
                else:
                    if len(ItemDescr) >= 250:
                        p.drawString(lftcol, itemy, (ItemDescr)[250:300])
                        itemy = itemyF(itemy)

                if float(item.OtherTaxAmount) != float("0.00"):
                    p.drawString(lftcol, itemy, (ItemDescr)[300:350])
                    p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(item.OtherTaxAmount), str(item.OtherTaxAmount).split(".")[1]))
                    itemy = itemyF(itemy)
                else:
                    if len(ItemDescr) >= 300:
                        p.drawString(lftcol, itemy, (ItemDescr)[300:350])
                        itemy = itemyF(itemy)
            if len(ItemDescr) >= 350:
                p.drawString(lftcol, itemy, (ItemDescr)[350:400])
                itemy = itemyF(itemy)
            if len(ItemDescr) >= 400:
                p.drawString(lftcol, itemy, (ItemDescr)[400:450])
                itemy = itemyF(itemy)
            if len(ItemDescr) >= 450:
                p.drawString(lftcol, itemy, (ItemDescr)[450:500])
                itemy = itemyF(itemy)
            if len(ItemDescr) >= 500:
                p.drawString(lftcol, itemy, (ItemDescr)[500:])
                itemy = itemyF(itemy)

            for man in InvoiceDtl.objects.filter(PermitId=PermitId, InvoiceNo=item.InvoiceNo):
                manf = SUPPLIERMANUFACTURERPARTY.objects.get(code=man.SupplierCode)
                p.drawString(lftcol, itemy, (manf.name)[:50])
                itemy = itemyF(itemy)
                if len(manf.name) >= 50:
                    p.drawString(lftcol, itemy, (manf.name)[50:])

            def CascFunc(sno, cascn):
                global itemy, p
                for casc in Cascdtl.objects.filter(ItemNo=item.ItemNo, PermitId=PermitId, CascId=cascn):
                    p.drawString(lftcol, itemy,  "--------------------------------------------------------------------------------")
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, 'S/NO')
                    p.drawString(lftcol+70, itemy, 'CA/SC PRODUCT CODE ')
                    p.drawString(lftcol+280, itemy, 'CA/SC PRODUCT QTY & UNIT')
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, '   {}'.format(sno))
                    p.drawString(lftcol+70, itemy, (casc.ProductCode).upper())
                    if str(casc.Quantity) != "0.0000":p.drawString(lftcol+280, itemy, ('{:10d}.{} {}').format(int(casc.Quantity), str(casc.Quantity).split(".")[1], casc.ProductUOM))
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy,  "--------------------------------------------------------------------------------")
                    break
            if len(Cascdtl.objects.filter(ItemNo=item.ItemNo, PermitId=PermitId)) != 0:
                CascFunc('01', "Casc1")
                CascFunc('02', "Casc2")
                CascFunc('03', "Casc3")
                CascFunc('04', "Casc4")
                CascFunc('05', "Casc5")
            if item.EngineCapcity != "0.00" and item.EngineCapcity != "":
                p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
                itemy = itemyF(itemy)
                p.drawString(lftcol, itemy, 'S/NO')
                p.drawString(lftcol+70, itemy, 'ENGINE NO/CHASSIS NO ')
                itemy = itemyF(itemy)
                p.drawString(lftcol, itemy, ("   {}").format("%02d" % item.ItemNo))
                p.drawString(lftcol+70, itemy, str(item.EngineCapcity))
                itemy = itemyF(itemy)
                p.drawString(snox, itemy, '-------------------------------------------------------------------------------')

            p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
            itemy = itemyF(itemy)-20
            p.drawString(snox, itemy, '-------------------------------------------------------------------------------')

        def itemyF1(itemy):
            global countPage 
            if itemy <= 60:
                itemy = 820
                p.showPage()
                p.setFont('Courier', 10)
            else:
                itemy -= 10
            if itemy <= 820 and itemy >= 780:
                p.setFont('Courier', 10)
                p.drawString(rgtcol, itemy, "CARGO CLEARANCE PERMIT ")
                p.drawString(460, itemy, ("PG : {} OF").format(countPage))
                countPage += 1
                itemy -= 10
                p.drawString(lftcol, itemy, "PERMIT NO : "+draft)
                p.drawString(rgtcol, itemy, "======================")
                itemy -= 10
                p.drawString(rgtcol, itemy, "(CONTINUATION PAGE)")
                itemy -= 20
                p.drawString(lftcol, itemy, "CONSIGNMENT DETAILS")
                itemy -= 10
                p.drawString(
                    lftcol, itemy, "--------------------------------------------------------------------------------")
                itemy -= 10
                p.drawString(
                    lftcol, 50,  "--------------------------------------------------------------------------------")
                p.drawString(lftcol, 40,  ("UNIQUE REF : {} {} {}").format(Declarant.cruei, Inheader.MSGId[:8], Inheader.MSGId[8:]))
            return itemy
        
        if Inheader.TradeRemarks != "":
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "TRADER’s REMARKS")
            itemy = itemyF1(itemy)
            TradeRe = (Inheader.TradeRemarks).upper()
            TradeRe = (Inheader.TradeRemarks).upper()
            if '\n' in TradeRe:
                for trd in TradeRe.split('\n'):
                    p.drawString(lftcol, itemy, trd)
                    itemy = itemyF1(itemy)
            else:
                p.drawString(lftcol, itemy, TradeRe[:80])
                itemy = itemyF1(itemy)
                if len(TradeRe) >= 80:
                    p.drawString(lftcol, itemy, TradeRe[80:160])
                    itemy = itemyF1(itemy)
                if len(TradeRe) >= 160:
                    p.drawString(lftcol, itemy, TradeRe[160:240])
                    itemy = itemyF1(itemy)
                if len(TradeRe) >= 240:
                    p.drawString(lftcol, itemy, TradeRe[240:320])
                    itemy = itemyF1(itemy)
                if len(TradeRe) >= 320:
                    p.drawString(lftcol, itemy, TradeRe[320:400])
                    itemy = itemyF1(itemy)
                if len(TradeRe) >= 400:
                    p.drawString(lftcol, itemy, TradeRe[400:480])
                    itemy = itemyF1(itemy)
                if len(TradeRe) >= 480:
                    p.drawString(lftcol, itemy, TradeRe[480:])
                    itemy = itemyF1(itemy)
        p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
        if len(ContainerDtl.objects.filter(PermitId=PermitId)) != 0:
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "CONTAINER IDENTIFIERS")
            itemy = itemyF1(itemy)
            for containerv in ContainerDtl.objects.filter(PermitId=PermitId):
                p.drawString(lftcol, itemy, ("   {})").format("%02d" % containerv.RowNo))
                p.drawString(lftcol+50, itemy, str(containerv.ContainerNo).upper())
                p.drawString(
                    lftcol+130, itemy, ("{}  {}").format(containerv.size[:3], containerv.size[3:5]))
                p.drawString(lftcol+200, itemy, (str(containerv.weight))[:3])
                p.drawString(lftcol+240, itemy, str(containerv.SealNo))
                itemy = itemyF1(itemy)

        p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
        itemy = itemyF1(itemy)
        p.drawString(lftcol, itemy, "NO UNAUTHORISED ADDITION/AMENDMENT TO THIS PERMIT MAY BE MADE AFTER APPROVAL")
        itemy = itemyF1(itemy)
        p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
        itemy = itemyF1(itemy)
        p.drawString(lftcol, itemy, "NAME OF COMPANY:")
        p.drawString(lftcol+110, itemy, (Declarant.name)[:67])
        itemy = itemyF1(itemy)
        p.drawString(lftcol+110, itemy, (Declarant.name)[67:])
        itemy = itemyF1(itemy)
        p.drawString(lftcol, itemy, "DECLARANT NAME :")
        p.drawString(lftcol+110, itemy, (Declarant.DeclarantName)[:67])
        itemy = itemyF1(itemy)
        p.drawString(lftcol+110, itemy, (Declarant.DeclarantName)[67:])
        itemy = itemyF1(itemy)
        p.drawString(lftcol, itemy, "DECLARANT CODE :")
        p.drawString(lftcol+110, itemy, "XXXX"+(Declarant.DeclarantCode)[-5:])
        itemy = itemyF1(itemy)
        p.drawString(lftcol, itemy, "TEL NO         : ")
        p.drawString(lftcol+110, itemy, (Declarant.DeclarantTel))
        itemy = itemyF1(itemy)
        p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
        itemy = itemyF1(itemy)
        p.drawString(lftcol, itemy, "CONTROLLING AGENCY/CUSTOMS CONDITIONS ")
        itemy = itemyF1(itemy)
        for pmt in Inpmt.objects.filter(PermitNumber=Inheader.PermitNumber).order_by("id"):
            p.setFont('Courier-Bold', 10)
            p.drawString(lftcol, itemy, pmt.Conditioncode)
            p.drawString(lftcol+30, itemy, "-")
            p.setFont('Courier', 10)
            p.drawString(lftcol+40, itemy, (pmt.ConditionDescription)[:73])
            itemy = itemyF1(itemy)
            if len((pmt.ConditionDescription)) > 73:
                p.drawString(lftcol, itemy, (pmt.ConditionDescription)[73:153])
                itemy = itemyF1(itemy)
            if len((pmt.ConditionDescription)) > 153:
                p.drawString(lftcol, itemy, (pmt.ConditionDescription)[153:233])
                itemy = itemyF1(itemy)
            if len((pmt.ConditionDescription)) > 233:
                p.drawString(lftcol, itemy, (pmt.ConditionDescription)[233:313])
                itemy = itemyF1(itemy)
            if len((pmt.ConditionDescription)) > 313:
                p.drawString(lftcol, itemy, (pmt.ConditionDescription)[313:393])
                itemy = itemyF1(itemy)
            if len((pmt.ConditionDescription)) > 393:
                p.drawString(lftcol, itemy, (pmt.ConditionDescription)[393:473])
                itemy = itemyF1(itemy)
            if len((pmt.ConditionDescription)) > 473:
                p.drawString(lftcol, itemy, (pmt.ConditionDescription)[473:])
                itemy = itemyF1(itemy)
        if draft == "DRAFT":
            draft = f"Draft_{Inheader.MSGId}"
            filename = f"D:/Users/Public/PDFFilesKtt/1{draft}.pdf"
        else:
            filename = f"D:/Users/Public/PDFFilesKtt/1{draft}.pdf"
        p.setTitle(draft)
        p.save()
        try:
            with open(filename, 'wb') as f:
                f.write(buffer.getbuffer())
        except Exception as e:
            pass
        buffer.seek(0)
        buffer.close()



        existing_pdf = PdfFileReader(open(filename, "rb"))
        output = PdfFileWriter()

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(595, 841))
        can.setFont('Courier', 10)
        can.drawString(520, 700, str(len(existing_pdf.pages)))
        can.showPage()
        can.setFont('Courier', 10)
        can.drawString(520, 810, str(len(existing_pdf.pages)))
        can.showPage()
        can.setFont('Courier', 10)
        can.drawString(520, 820, str(len(existing_pdf.pages)))
        can.save()

        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        for i in range(len(existing_pdf.pages)):
            if i == 0:
                page = existing_pdf.pages[i]
                page.merge_page(new_pdf.pages[0])
            elif i == 1:
                page = existing_pdf.pages[i]
                page.merge_page(new_pdf.pages[1])
            else:
                page = existing_pdf.pages[i]
                page.merge_page(new_pdf.pages[2])
            output.add_page(page)

        output_stream = open(f"D:/Users/Public/PDFFilesKtt/{draft}.pdf", "wb")#f"D:/Users/Public/PDFFilesKtt/{draft}.pdf
        output.write(output_stream)
        output_stream.close()

        file_path = f"D:/Users/Public/PDFFilesKtt/{draft}1.pdf"

        if os.path.exists(file_path):
            os.remove(file_path)

        pdfFiles.append(f"D:/Users/Public/PDFFilesKtt/{draft}.pdf")

    pdfWriter = PdfFileWriter()

    for file in pdfFiles:
        pdfFile = open(file, 'rb')
        pdfReader = PdfFileReader(pdfFile)

        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)



    pdfOutputFile = open('D:/Users/Public/PDFFilesKtt/MergedFiles.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)

    pdfOutputFile.close()
    pdfFile.close()


    with open(f"D:/Users/Public/PDFFilesKtt/MergedFiles.pdf", 'rb') as pdf_file:
        pdf_data = pdf_file.read()

    response = HttpResponse(pdf_data, content_type='application/pdf')
    if len(pdfFiles) > 1:
        response['Content-Disposition'] = f'attachment; filename="InpayMultiply.pdf"'
    else:
        response['Content-Disposition'] = f'attachment; filename="{draft}.pdf"'

    return response
