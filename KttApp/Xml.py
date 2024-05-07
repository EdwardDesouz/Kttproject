from .models import *
from datetime import datetime
from django.http import JsonResponse
import json

from KttApp.views import SqlDb

def XmlSubmit(request):

    permitNumber1 = json.loads(request.GET.get("PermitNumber"))
    s = SqlDb('SecondDb')
    s1 = SqlDb('default')
    for permitNumber in permitNumber1:
        print("the Permitnumber : ",permitNumber)
        TouchUser = str(request.session['Username']).upper() 
        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")

        s.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(TouchUser))
        ManageUserVal = s.cursor.fetchone()
        AccountId = ManageUserVal[0]
        MailId = ManageUserVal[1]

        s.cursor.execute("SELECT COUNT(*) + 1  FROM InheaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'IPTDEC' ".format(refDate))
        RefId = ("%03d" % s.cursor.fetchone()[0])

        s.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        JobIdCount = s.cursor.fetchone()[0]

        JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % JobIdCount}" 
        MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % JobIdCount}"
        NewPermitId = f"{TouchUser}{refDate}{RefId}"

        TouchTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            s1.cursor.execute(f"SELECT * FROM InheaderTbl WHERE PermitId='{permitNumber}' ")
            Heading = [i[0] for i in s1.cursor.description]
            HeadData = [dict(zip(Heading,row)) for row in s1.cursor.fetchall()]
            HeadQry = ("INSERT INTO InheaderTbl(Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,InwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,HBL,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,ReleaseLocName,RecepitLocation,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,RecepitLocName,Cnb,DeclarningFor,MRDate,MRTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
            for head in HeadData:
                headVal = (RefId,JobId,MsgId,NewPermitId,MailId,head['MessageType'],head['DeclarationType'],head['PreviousPermit'],head['CargoPackType'],head['InwardTransportMode'],head['BGIndicator'],head['SupplyIndicator'],head['ReferenceDocuments'],head['License'],head['Recipient'],head['DeclarantCompanyCode'],head['ImporterCompanyCode'],head['InwardCarrierAgentCode'],head['FreightForwarderCode'],head['ClaimantPartyCode'],head['HBL'],head['ArrivalDate'],head['LoadingPortCode'],head['VoyageNumber'],head['VesselName'],head['OceanBillofLadingNo'],head['ConveyanceRefNo'],head['TransportId'],head['FlightNO'],head['AircraftRegNo'],head['MasterAirwayBill'],head['ReleaseLocation'],head['ReleaseLocName'],head['RecepitLocation'],head['TotalOuterPack'],head['TotalOuterPackUOM'],head['TotalGrossWeight'],head['TotalGrossWeightUOM'],head['GrossReference'],head['BlanketStartDate'],head['TradeRemarks'],head['InternalRemarks'],head['CustomerRemarks'],head['DeclareIndicator'],head['NumberOfItems'],head['TotalCIFFOBValue'],head['TotalGSTTaxAmt'],head['TotalExDutyAmt'],head['TotalCusDutyAmt'],head['TotalODutyAmt'],head['TotalAmtPay'],head['Status'],TouchUser,TouchTime,head['PermitNumber'],head['prmtStatus'],head['RecepitLocName'],head['Cnb'],head['DeclarningFor'],head['MRDate'],head['MRTime'])
                s.cursor.execute(HeadQry,headVal)

            s.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{NewPermitId}','IPTDEC','{AccountId}','{MsgId}','{TouchUser}','{TouchTime}') ")

            InvoiceQry = "INSERT INTO InvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime,ChkOtherInv) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM InvoiceDtl WHERE PermitId='{permitNumber}' ")
            InvoiceHead = [i[0] for i in s1.cursor.description]
            InvoiceData = [dict(zip(InvoiceHead,row)) for row in s1.cursor.fetchall()]
            for invoice in InvoiceData:
                InvoiceVal= (invoice['SNo'],invoice['InvoiceNo'],invoice['InvoiceDate'],invoice['TermType'],invoice['AdValoremIndicator'],invoice['PreDutyRateIndicator'],invoice['SupplierImporterRelationship'],invoice['SupplierCode'],invoice['ImportPartyCode'],invoice['TICurrency'],invoice['TIExRate'],invoice['TIAmount'],invoice['TISAmount'],invoice['OTCCharge'],invoice['OTCCurrency'],invoice['OTCExRate'],invoice['OTCAmount'],invoice['OTCSAmount'],invoice['FCCharge'],invoice['FCCurrency'],invoice['FCExRate'],invoice['FCAmount'],invoice['FCSAmount'],invoice['ICCharge'],invoice['ICCurrency'],invoice['ICExRate'],invoice['ICAmount'],invoice['ICSAmount'],invoice['CIFSUMAmount'],invoice['GSTPercentage'],invoice['GSTSUMAmount'],invoice['MessageType'],NewPermitId,TouchUser,TouchTime,invoice['ChkOtherInv'])
                s.cursor.execute(InvoiceQry,InvoiceVal)

            ItemQry = "INSERT INTO ItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,VehicleType,EngineCapcity,EngineCapUOM,orignaldatereg,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM ItemDtl WHERE PermitId='{permitNumber}' ")
            ItemHead = [i[0] for i in s1.cursor.description]
            ItemData = [dict(zip(ItemHead,row)) for row in s1.cursor.fetchall()]
            for invoice in ItemData:
                ItemVal= (invoice['ItemNo'],NewPermitId,invoice['MessageType'],invoice['HSCode'],invoice['Description'],invoice['DGIndicator'],invoice['Contry'],invoice['Brand'],invoice['Model'],invoice['InHAWBOBL'],invoice['DutiableQty'],invoice['DutiableUOM'],invoice['TotalDutiableQty'],invoice['TotalDutiableUOM'],invoice['InvoiceQuantity'],invoice['HSQty'],invoice['HSUOM'],invoice['AlcoholPer'],invoice['InvoiceNo'],invoice['ChkUnitPrice'],invoice['UnitPrice'],invoice['UnitPriceCurrency'],invoice['ExchangeRate'],invoice['SumExchangeRate'],invoice['TotalLineAmount'],invoice['InvoiceCharges'],invoice['CIFFOB'],invoice['OPQty'],invoice['OPUOM'],invoice['IPQty'],invoice['IPUOM'],invoice['InPqty'],invoice['InPUOM'],invoice['ImPQty'],invoice['ImPUOM'],invoice['PreferentialCode'],invoice['GSTRate'],invoice['GSTUOM'],invoice['GSTAmount'],invoice['ExciseDutyRate'],invoice['ExciseDutyUOM'],invoice['ExciseDutyAmount'],invoice['CustomsDutyRate'],invoice['CustomsDutyUOM'],invoice['CustomsDutyAmount'],invoice['OtherTaxRate'],invoice['OtherTaxUOM'],invoice['OtherTaxAmount'],invoice['CurrentLot'],invoice['PreviousLot'],invoice['LSPValue'],invoice['Making'],invoice['ShippingMarks1'],invoice['ShippingMarks2'],invoice['ShippingMarks3'],invoice['ShippingMarks4'],TouchUser,TouchTime,invoice['VehicleType'],invoice['EngineCapcity'],invoice['EngineCapUOM'],invoice['orignaldatereg'],invoice['OptionalChrgeUOM'],invoice['Optioncahrge'],invoice['OptionalSumtotal'],invoice['OptionalSumExchage'])
                s.cursor.execute(ItemQry,ItemVal)

            ItemCascQry = "INSERT INTO Cascdtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM Cascdtl WHERE PermitId='{permitNumber}' ")
            ItemCascHead = [i[0] for i in s1.cursor.description]
            ItemCascData = [dict(zip(ItemCascHead,row)) for row in s1.cursor.fetchall()]
            for head in ItemCascData:
                ItemCascVal= (head['ItemNo'],head['ProductCode'],head['Quantity'],head['ProductUOM'],head['RowNo'],head['CascCode1'],head['CascCode2'],head['CascCode3'],NewPermitId,head['MessageType'],TouchUser,TouchTime,head['CASCId'])
                s.cursor.execute(ItemCascQry,ItemCascVal)

            ContainerQry = "INSERT INTO ContainerDtl (PermitId,RowNo,ContainerNo,Size,Weight,SealNo,MessageType,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM ContainerDtl WHERE PermitId='{permitNumber}' ")
            ContainerHead = [i[0] for i in s1.cursor.description]
            ContainerData = [dict(zip(ContainerHead,row)) for row in s1.cursor.fetchall()]
            for container in ContainerData:
                ContainerVal= (NewPermitId,container['RowNo'],container['ContainerNo'],container['Size'],container['Weight'],container['SealNo'],container['MessageType'],TouchUser,TouchTime)
                s.cursor.execute(ContainerQry,ContainerVal)

            CpcQry = "INSERT INTO CpcDtl (PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM CpcDtl WHERE PermitId='{permitNumber}' ")
            CpcHead = [i[0] for i in s1.cursor.description]
            CpcData = [dict(zip(CpcHead,row)) for row in s1.cursor.fetchall()]
            for cpc in CpcData:
                CpcVal= (NewPermitId,cpc['MessageType'],cpc['RowNo'],cpc['CPCType'],cpc['ProcessingCode1'],cpc['ProcessingCode2'],cpc['ProcessingCode3'],TouchUser,TouchTime)
                s.cursor.execute(CpcQry,CpcVal) 

            InfileQry = "INSERT INTO InFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,filePath,Size,PermitId,Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM InFile WHERE PermitId='{permitNumber}' ")
            InFileHead = [i[0] for i in s1.cursor.description]
            InFileData = [dict(zip(InFileHead,row)) for row in s1.cursor.fetchall()]
            for infile in InFileData:
                InfileVal= (infile['Sno'],infile['Name'],infile['ContentType'],infile['Data'],infile['DocumentType'],infile['InPaymentId'],TouchUser,TouchTime,infile['filePath'],infile['Size'],NewPermitId,infile['Type'])
                s.cursor.execute(InfileQry,InfileVal)

            s.conn.commit()
            print("saved SuccessFully")
        except Exception as e:
            print("the Error is : ",e)
        finally:
            return JsonResponse({"Success":"Genrate"})

    return JsonResponse({"Success":"Genrate"})
 