
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import pymssql
import json
from KttApp.views import SqlDb

def CopyInpayment(request):

    nowRefId = datetime.now().strftime("%Y%m%d")
    nowJobId = datetime.now().strftime("%Y-%m-%d") 

    UserName =  request.session['Username']
    TOUCHTIME = request.POST.get('TOUCHTIME')

    Carc = request.POST.get('val')

    s = SqlDb()
    

    # conn = pymssql.connect(server='ec2-54-179-0-97.ap-southeast-1.compute.amazonaws.com',user='KTTUSER', password='Ktt@2021', database='TestPortal')
    # cursor = conn.cursor()

    for i in ManageUser.objects.filter(UserName=UserName):
        AccountId = i.AccountId
        MailBoxId = i.MailBoxId

    inHeaderReId = len(InheaderTbl.objects.filter( MSGId__icontains=nowRefId, MessageType="IPTDEC"))+1
    inHeaderReId = ("%03d" % inHeaderReId)
    inHeaderJobId1 = len(PermitCount.objects.filter( TouchTime__icontains=nowJobId, AccountId=AccountId))+1
    inHeaderJobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % inHeaderJobId1}"
    inHeaderMsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % inHeaderJobId1}"
    inHeaderPermitId = f"{UserName}{nowRefId}{inHeaderReId}"

    request.session['Permit_Id'] = inHeaderPermitId

    s.cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'InFile'")
    for i in s.cursor.fetchall():
        pass

    val = "NEW"
    if Carc == "REFUND":
        val = "RFD"
    if Carc == "AMEND":
        val = "AME"
    if Carc == "CANCEL":
        val = "CNL"
     

    #---------------------------------------------------------------- COPY ----------------------------------------------------------------#


    s.cursor.execute(f"INSERT INTO InheaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,InwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,HBL,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,ReleaseLocName,RecepitLocation,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,RecepitLocName,Cnb,DeclarningFor,MRDate,MRTime) SELECT '{inHeaderReId}','{inHeaderJobId}','{inHeaderMsgId}','{inHeaderPermitId}','{MailBoxId}',MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,InwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,HBL,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,ReleaseLocName,RecepitLocation,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,'DRF','{UserName}','{TOUCHTIME}',{'NULL' if Carc == 'COPY' else 'PermitNumber'},'{val}',RecepitLocName,Cnb,'--Select--',MRDate,MRTime FROM InheaderTbl WHERE PermitId = '{request.POST.get('Permitid')}'")

    s.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{inHeaderPermitId}','IPTDEC','{AccountId}','{inHeaderMsgId}','{UserName}','{TOUCHTIME}')")
    
    s.cursor.execute(f"INSERT INTO InvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime,ChkOtherInv) SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,'{inHeaderPermitId}','{UserName}','{TOUCHTIME}',ChkOtherInv FROM InvoiceDtl WHERE PermitId = '{request.POST.get('Permitid')}'")

    s.cursor.execute(f"INSERT INTO ItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,VehicleType,EngineCapcity,EngineCapUOM,orignaldatereg,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) SELECT ItemNo,'{inHeaderPermitId}',MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,'{UserName}','{TOUCHTIME}',VehicleType,EngineCapcity,EngineCapUOM,orignaldatereg,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage From ItemDtl WHERE PermitId = '{request.POST.get('Permitid')}'")

    s.cursor.execute(f"INSERT INTO ContainerDtl (PermitId,RowNo,ContainerNo,Size,Weight,SealNo,MessageType,TouchUser,TouchTime) SELECT '{inHeaderPermitId}',RowNo,ContainerNo,Size,Weight,SealNo,MessageType,'{UserName}','{TOUCHTIME}' From ContainerDtl Where PermitId = '{request.POST.get('Permitid')}'")
    
    s.cursor.execute(f"INSERT INTO CpcDtl (PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) SELECT '{inHeaderPermitId}',MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,'{UserName}','{TOUCHTIME}' FROM CpcDtl Where PermitId = '{request.POST.get('Permitid')}'")
    
    s.cursor.execute(f"INSERT INTO InFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,filePath,Size,PermitId,Type) SELECT Sno,Name,ContentType,Data,DocumentType,InPaymentId,'{UserName}','{TOUCHTIME}',filePath,Size,'{inHeaderPermitId}',Type FROM InFile Where PermitId = '{request.POST.get('Permitid')}'")

    s.conn.commit()

    

    return JsonResponse({"Checking Values  ": 'true'})

def TransmitDataFunction(request):
    nowRefId = datetime.now().strftime("%Y%m%d")
    nowJobId = datetime.now().strftime("%Y-%m-%d")

    s = SqlDb()

    for permitID in json.loads(request.POST.get("my_data")):
        maiId = request.POST.get('mailId')
        UserName = request.POST.get('UserName')
        for i in InheaderTbl.objects.filter(TradeNetMailboxID=maiId).order_by('id'):
            UserName = i.TouchUser
            break
        for i in ManageUser.objects.filter(UserName=UserName):
            AccountId = i.AccountId
        inHeaderReId = len(InheaderTbl.objects.filter(MSGId__icontains=nowRefId, MessageType="IPTDEC"))+1
        inHeaderReId = ("%03d" % inHeaderReId)
        inHeaderJobId1 = len(PermitCount.objects.filter(TouchTime__icontains=nowJobId, AccountId=AccountId))+1
        inHeaderJobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % inHeaderJobId1}"
        inHeaderMsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % inHeaderJobId1}"
        inHeaderPermitId = f"{UserName}{nowRefId}{inHeaderReId}"

        TOUCHTIME = datetime.now()

        s.cursor.execute(f"INSERT INTO InheaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,InwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,HBL,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,ReleaseLocName,RecepitLocation,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,RecepitLocName,Cnb,DeclarningFor,MRDate,MRTime) SELECT '{inHeaderReId}','{inHeaderJobId}','{inHeaderMsgId}','{inHeaderPermitId}','{maiId}',MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,InwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,HBL,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,ReleaseLocName,RecepitLocation,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,'DRF','{UserName}','{TOUCHTIME}',PermitNumber,prmtStatus,RecepitLocName,Cnb,'--Select--',MRDate,MRTime FROM InheaderTbl WHERE PermitId = '{permitID}'")

        s.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{inHeaderPermitId}','IPTDEC','{AccountId}','{inHeaderMsgId}','{UserName}','{TOUCHTIME}')")
        
        s.cursor.execute(f"INSERT INTO InvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime,ChkOtherInv) SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,'{inHeaderPermitId}','{UserName}','{TOUCHTIME}',ChkOtherInv FROM InvoiceDtl WHERE PermitId = '{permitID}'")

        s.cursor.execute(f"INSERT INTO ItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,VehicleType,EngineCapcity,EngineCapUOM,orignaldatereg,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) SELECT ItemNo,'{inHeaderPermitId}',MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,'{UserName}','{TOUCHTIME}',VehicleType,EngineCapcity,EngineCapUOM,orignaldatereg,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage From ItemDtl WHERE PermitId = '{permitID}'")

        s.cursor.execute(f"INSERT INTO ContainerDtl (PermitId,RowNo,ContainerNo,Size,Weight,SealNo,MessageType,TouchUser,TouchTime) SELECT '{inHeaderPermitId}',RowNo,ContainerNo,Size,Weight,SealNo,MessageType,'{UserName}','{TOUCHTIME}' From ContainerDtl Where PermitId = '{permitID}'")
        
        s.cursor.execute(f"INSERT INTO CpcDtl (PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) SELECT '{inHeaderPermitId}',MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,'{UserName}','{TOUCHTIME}' FROM CpcDtl Where PermitId = '{permitID}'")
        
        s.cursor.execute(f"INSERT INTO InFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,filePath,Size,PermitId,Type) SELECT Sno,Name,ContentType,Data,DocumentType,InPaymentId,'{UserName}','{TOUCHTIME}',filePath,Size,'{inHeaderPermitId}',Type FROM InFile Where PermitId = '{permitID}'")

        s.conn.commit()