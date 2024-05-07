
from django.http import JsonResponse
from .models import *
import json


def InvoiceSave(request):
    PermitId = request.POST.get('PermitId')
    SNo = request.POST.get('SNo')

    if InvoiceDtl.objects.filter(PermitId=PermitId, SNo=SNo).exists():
        try:
            InvoiceDtl.objects.filter(PermitId=PermitId, SNo=SNo).update(
                SNo=request.POST.get('SNo'),
                InvoiceNo=request.POST.get('InvoiceNo'),
                InvoiceDate=request.POST.get('InvoiceDate'),
                TermType=request.POST.get('TermType'),
                AdValoremIndicator=request.POST.get('AdValoremIndicator'),
                PreDutyRateIndicator=request.POST.get('PreDutyRateIndicator'),
                SupplierImporterRelationship=request.POST.get(
                    'SupplierImporterRelationship'),
                SupplierCode=request.POST.get('SupplierCode'),
                ImportPartyCode=request.POST.get('ImportPartyCode'),
                TICurrency=request.POST.get('TICurrency'),
                TIExRate=request.POST.get('TIExRate'),
                TIAmount=request.POST.get('TIAmount'),
                TISAmount=request.POST.get('TISAmount'),
                OTCCharge=request.POST.get('OTCCharge'),
                OTCCurrency=request.POST.get('OTCCurrency'),
                OTCExRate=request.POST.get('OTCExRate'),
                OTCAmount=request.POST.get('OTCAmount'),
                OTCSAmount=request.POST.get('OTCSAmount'),
                FCCharge=request.POST.get('FCCharge'),
                FCCurrency=request.POST.get('FCCurrency'),
                FCExRate=request.POST.get('FCExRate'),
                FCAmount=request.POST.get('FCAmount'),
                FCSAmount=request.POST.get('FCSAmount'),
                ICCharge=request.POST.get('ICCharge'),
                ICCurrency=request.POST.get('ICCurrency'),
                ICExRate=request.POST.get('ICExRate'),
                ICAmount=request.POST.get('ICAmount'),
                ICSAmount=request.POST.get('ICSAmount'),
                CIFSUMAmount=request.POST.get('CIFSUMAmount'),
                GSTPercentage=request.POST.get('GSTPercentage'),
                GSTSUMAmount=request.POST.get('GSTSUMAmount'),
                MessageType=request.POST.get('MessageType'),
                PermitId=request.POST.get('PermitId'),
                TouchUser=request.POST.get('TouchUser'),
                TouchTime=request.POST.get('TouchTime'),
                ChkOtherInv=request.POST.get('ChkOtherInv')
            )
            Result = "Invoice Updated Success"
        except Exception as e:
            Result = "Inoice Data Already Exists SNo"+str(e)
    else:
        try:
            invoice = InvoiceDtl(
                SNo=request.POST.get('SNo'),
                InvoiceNo=request.POST.get('InvoiceNo'),
                InvoiceDate=request.POST.get('InvoiceDate'),
                TermType=request.POST.get('TermType'),
                AdValoremIndicator=request.POST.get('AdValoremIndicator'),
                PreDutyRateIndicator=request.POST.get('PreDutyRateIndicator'),
                SupplierImporterRelationship=request.POST.get(
                    'SupplierImporterRelationship'),
                SupplierCode=request.POST.get('SupplierCode'),
                ImportPartyCode=request.POST.get('ImportPartyCode'),
                TICurrency=request.POST.get('TICurrency'),
                TIExRate=request.POST.get('TIExRate'),
                TIAmount=request.POST.get('TIAmount'),
                TISAmount=request.POST.get('TISAmount'),
                OTCCharge=request.POST.get('OTCCharge'),
                OTCCurrency=request.POST.get('OTCCurrency'),
                OTCExRate=request.POST.get('OTCExRate'),
                OTCAmount=request.POST.get('OTCAmount'),
                OTCSAmount=request.POST.get('OTCSAmount'),
                FCCharge=request.POST.get('FCCharge'),
                FCCurrency=request.POST.get('FCCurrency'),
                FCExRate=request.POST.get('FCExRate'),
                FCAmount=request.POST.get('FCAmount'),
                FCSAmount=request.POST.get('FCSAmount'),
                ICCharge=request.POST.get('ICCharge'),
                ICCurrency=request.POST.get('ICCurrency'),
                ICExRate=request.POST.get('ICExRate'),
                ICAmount=request.POST.get('ICAmount'),
                ICSAmount=request.POST.get('ICSAmount'),
                CIFSUMAmount=request.POST.get('CIFSUMAmount'),
                GSTPercentage=request.POST.get('GSTPercentage'),
                GSTSUMAmount=request.POST.get('GSTSUMAmount'),
                MessageType=request.POST.get('MessageType'),
                PermitId=request.POST.get('PermitId'),
                TouchUser=request.POST.get('TouchUser'),
                TouchTime=request.POST.get('TouchTime'),
                ChkOtherInv=request.POST.get('ChkOtherInv'),
            )
            invoice.save()
            Result = "Invoice Data Saved"
        except Exception as e:
            Result = "Invoice Data Saved Failed"+str(e)

    Invoice = list(InvoiceDtl.objects.filter(
        PermitId=PermitId).order_by('SNo').values())
    return JsonResponse({'Invoice': Invoice, "Result": Result})


def InvoiceDelete(request):
    SNo = request.GET.get('SNo')
    PermitId = request.GET.get('PermitId')
    InvoiceDtl.objects.filter(SNo=SNo, PermitId=PermitId).delete()
    invoice = InvoiceDtl.objects.filter(PermitId=PermitId).order_by('SNo')
    c = 1
    for i in invoice:
        InvoiceDtl.objects.filter(PermitId=PermitId, SNo=i.SNo).update(SNo=c)
        c += 1
    Invoice = list(InvoiceDtl.objects.filter(PermitId=PermitId).order_by('SNo').values())
    return JsonResponse({'Invoice': Invoice})


def ItemSave(request): 
    PermitId = request.POST.get('PermitId')
    ItemNumber = request.POST.get('ItemNo')
    Result = ''

    if ItemDtl.objects.filter(PermitId=PermitId, ItemNo=ItemNumber).exists():
        Code = ItemDtl.objects.filter(
            PermitId=PermitId, ItemNo=ItemNumber).update
    else:
        Code = ItemDtl.objects.create
    try:
        Code(
            ItemNo=request.POST.get('ItemNo'),
            PermitId=request.POST.get('PermitId'),
            MessageType=request.POST.get('MessageType'),
            HSCode=request.POST.get('HSCode'),
            Description=request.POST.get('Description'),
            DGIndicator=request.POST.get('DGIndicator'),
            Contry=request.POST.get('Contry'),
            Brand=request.POST.get('Brand'),
            Model=request.POST.get('Model'),
            InHAWBOBL=request.POST.get('InHAWBOBL'),
            DutiableQty=request.POST.get('DutiableQty'),
            DutiableUOM=request.POST.get('DutiableUOM'),
            TotalDutiableQty=request.POST.get('TotalDutiableQty'),
            TotalDutiableUOM=request.POST.get('TotalDutiableUOM'),
            InvoiceQuantity=request.POST.get('InvoiceQuantity'),
            HSQty=request.POST.get('HSQty'),
            HSUOM=request.POST.get('HSUOM'),
            AlcoholPer=request.POST.get('AlcoholPer'),
            InvoiceNo=request.POST.get('InvoiceNo'),
            ChkUnitPrice=request.POST.get('ChkUnitPrice'),
            UnitPrice=request.POST.get('UnitPrice'),
            UnitPriceCurrency=request.POST.get('UnitPriceCurrency'),
            ExchangeRate=request.POST.get('ExchangeRate'),
            SumExchangeRate=request.POST.get('SumExchangeRate'),
            TotalLineAmount=request.POST.get('TotalLineAmount'),
            InvoiceCharges=request.POST.get('InvoiceCharges'),
            CIFFOB=request.POST.get('CIFFOB'),
            OPQty=request.POST.get('OPQty'),
            OPUOM=request.POST.get('OPUOM'),
            IPQty=request.POST.get('IPQty'),
            IPUOM=request.POST.get('IPUOM'),
            InPqty=request.POST.get('InPqty'),
            InPUOM=request.POST.get('InPUOM'),
            ImPQty=request.POST.get('ImPQty'),
            ImPUOM=request.POST.get('ImPUOM'),
            PreferentialCode=request.POST.get('PreferentialCode'),
            GSTRate=request.POST.get('GSTRate'),
            GSTUOM=request.POST.get('GSTUOM'),
            GSTAmount=request.POST.get('GSTAmount'),
            ExciseDutyRate=request.POST.get('ExciseDutyRate'),
            ExciseDutyUOM=request.POST.get('ExciseDutyUOM'),
            ExciseDutyAmount=request.POST.get('ExciseDutyAmount'),
            CustomsDutyRate=request.POST.get('CustomsDutyRate'),
            CustomsDutyUOM=request.POST.get('CustomsDutyUOM'),
            CustomsDutyAmount=request.POST.get('CustomsDutyAmount'),
            OtherTaxRate=request.POST.get('OtherTaxRate'),
            OtherTaxUOM=request.POST.get('OtherTaxUOM'),
            OtherTaxAmount=request.POST.get('OtherTaxAmount'),
            CurrentLot=request.POST.get('CurrentLot'),
            PreviousLot=request.POST.get('PreviousLot'),
            LSPValue=request.POST.get('LSPValue'),
            Making=request.POST.get('Making'),
            ShippingMarks1=request.POST.get('ShippingMarks1'),
            ShippingMarks2=request.POST.get('ShippingMarks2'),
            ShippingMarks3=request.POST.get('ShippingMarks3'),
            ShippingMarks4=request.POST.get('ShippingMarks4'),
            TouchUser=request.POST.get('TouchUser'),
            TouchTime=request.POST.get('TouchTime'),
            VehicleType=request.POST.get('VehicleType'),
            EngineCapcity=request.POST.get('EngineCapcity'),
            EngineCapUOM=request.POST.get('EngineCapUOM'),
            orignaldatereg=request.POST.get('orignaldatereg'),
            OptionalChrgeUOM=request.POST.get('OptionalChrgeUOM'),
            Optioncahrge=request.POST.get('Optioncahrge'),
            OptionalSumtotal=request.POST.get('OptionalSumtotal'),
            OptionalSumExchage=request.POST.get('OptionalSumExchage')
        )
        Result = "Item Data Saved"
    except Exception as e:
        Result = "Item Did Not Saved Data Saved"
    try:
        if Cascdtl.objects.filter(PermitId=PermitId, ItemNo=ItemNumber).exists():
            Cascdtl.objects.filter(
                PermitId=PermitId, ItemNo=ItemNumber).delete()
        CascValue = json.loads(request.POST.get('CascDatas'))
        for Casc in CascValue:
            CascData = Cascdtl(
                ItemNo=Casc['ItemNo'],
                ProductCode=Casc['ProductCode'],
                Quantity=Casc['Quantity'],
                ProductUOM=Casc['ProductUOM'],
                RowNo=Casc['RowNo'],
                CascCode1=Casc['CascCode1'],
                CascCode2=Casc['CascCode2'],
                CascCode3=Casc['CascCode3'],
                PermitId=Casc['PermitId'],
                MessageType=Casc['MessageType'],
                TouchUser=Casc['TouchUser'],
                TouchTime=Casc['TouchTime'],
                CascId=Casc['CascId'],
            )
            CascData.save()
    except Exception as e:pass

    # CascDatas = request.POST.get('CascDatas')
    Item = Item = list(ItemDtl.objects.filter(
        PermitId=PermitId).order_by('ItemNo').values())
    ItemCasc = list(Cascdtl.objects.filter(
        PermitId=PermitId).order_by('ItemNo').values())
    return JsonResponse({'Item': Item, 'ItemCasc': ItemCasc, "Result": Result})


def CascDelete(request):
    ID = request.GET.get('ID')
    PermitId = request.GET.get('PermitID')
    Cascdtl.objects.get(id=ID).delete()
    ItemCasc = list(Cascdtl.objects.filter(
        PermitId=PermitId).order_by('ItemNo').values())
    return JsonResponse({'ItemCasc': ItemCasc, "Result": "Deleted"})


def ItemDelete(request):
    PermitId = request.GET.get('PermitId')
    for i in json.loads(request.GET.get('ItemNo')):
        ItemDtl.objects.filter(PermitId=PermitId, ItemNo=i).delete()
        Cascdtl.objects.filter(PermitId=PermitId, ItemNo=i).delete()

    item = ItemDtl.objects.filter(PermitId=PermitId).order_by('ItemNo')
    count = 1
    for i in item:
        Cascdtl.objects.filter(PermitId=PermitId, ItemNo=i.ItemNo).update(ItemNo=count)
        ItemDtl.objects.filter(PermitId=PermitId, ItemNo=i.ItemNo).update(ItemNo=count)
        count += 1

    Item = Item = list(ItemDtl.objects.filter(PermitId=PermitId).order_by('ItemNo').values())
    ItemCasc = list(Cascdtl.objects.filter(PermitId=PermitId).order_by('ItemNo').values())
    return JsonResponse({'Item': Item, 'ItemCasc': ItemCasc, "Result": "Deleted"})

def ItemAllDelte(request):
    PermitId = request.GET.get('PermitId')
    ItemDtl.objects.filter(PermitId=PermitId).delete()
    Cascdtl.objects.filter(PermitId=PermitId).delete()
    Item = Item = list(ItemDtl.objects.filter(
        PermitId=PermitId).order_by('ItemNo').values())
    ItemCasc = list(Cascdtl.objects.filter(
        PermitId=PermitId).order_by('ItemNo').values()) 
    return JsonResponse({'Item': Item, 'ItemCasc': ItemCasc, "Result": "Deleted"})


def DocumentSave(request):
    PermitId = request.POST.get('PermitId')
    headLen = len(InFile.objects.filter(PermitId=PermitId))+1 
    myfile = request.FILES.get('file')
    path1 = request.POST.get('FilePath')
    fileFormat = request.POST.get('ContentType').split('/')
    with open(path1+request.POST.get('Name')+'.'+fileFormat[1], 'wb+') as destination:
        for chunk in myfile.chunks():
            destination.write(chunk)
    InFile(
        Sno=headLen,
        Name=request.POST.get('Name')+'.'+fileFormat[1],
        ContentType=request.POST.get('ContentType'),
        Data=None,
        DocumentType=request.POST.get('DocumentType'),
        InPaymentId=request.POST.get('InPaymentId'),
        TouchUser=request.POST.get('UserName'),
        TouchTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        FilePath=path1,
        Size=request.POST.get('Size'),
        PermitId=PermitId,
        Type=request.POST.get('Type')
    ).save()
    Infile = list(InFile.objects.filter(PermitId=PermitId).values())
    return JsonResponse({'Infile': Infile, 'Result': "Success"})


def DocumentDelete(request):
    PermitId = request.GET.get('PermitID')
    ID = request.GET.get('ID')
    InFile.objects.get(id=ID).delete()
    Infile = list(InFile.objects.filter(PermitId=PermitId).values())
    return JsonResponse({'Infile': Infile, 'Result': "Success"})


def DocumentDeletPermitId(request):
    PermitId = request.GET.get('PermitID')
    InFile.objects.filter(PermitId=PermitId).delete()
    Infile = list(InFile.objects.filter(PermitId=PermitId).values())
    return JsonResponse({'Infile': Infile, 'Result': "Success"})


def FinalSubmit(request):
    PermitId = request.POST.get('PermitId')
    UserName = request.POST.get('TouchUser')
    try:
        Cpc = json.loads(request.POST.get('Cpc'))
        CpcDtl.objects.filter(PermitId=PermitId).delete()
        for cp in Cpc:
            CpcDtl.objects.create(
                PermitId=cp['PermitId'],
                MessageType=cp['MessageType'],
                RowNo=cp['RowNo'],
                CpcType=cp['CpcType'],
                ProcessingCode1=cp['ProcessingCode1'],
                ProcessingCode2=cp['ProcessingCode2'],
                ProcessingCode3=cp['ProcessingCode3'],
                TouchUser=cp['TouchUser'],
                TouchTime=cp['TouchTime'],
            )
    except Exception as e:pass

    for i in ManageUser.objects.filter(UserName=UserName):
        AccountId = i.AccountId

    if "RFD" == request.POST.get('UpdateIndicator'):
        refundItemSum = json.loads(request.POST.get("RefundDatas"))
        try:ReundItemSumm.objects.filter(MsgId=request.POST.get("MSGId")).delete()
        except Exception as e:pass
        for item in refundItemSum:
            refunditemsuum = ReundItemSumm(
                PermitId=request.POST.get("PermitId"),
                ItemNo=item[1],
                HsCode=item[2],
                TotalGstAmt=item[3],
                TotalExciseAmt=item[4],
                TxtCusdutyAmt=item[5],
                TxtOtherAmt=item[6],
                Sno=item[0],
                MsgId=request.POST.get("MSGId"),
            )
            refunditemsuum.save()
        
        if InpaymentRefund.objects.filter(MsgId=request.POST.get('MSGId')).exists():
            InpaymentRefund1 = InpaymentRefund.objects.filter().update
        else:
            InpaymentRefund1 = InpaymentRefund.objects.create
        InpaymentRefund1(
            PermitNo=request.POST.get("PermitNo"),
            UpdateIndicator=request.POST.get("UpdateIndicator"),
            ReplacementPermitno=request.POST.get("ReplacementPermitno"),
            TypeOfRefund=request.POST.get("TypeOfRefund"),
            ResonForRefund=request.POST.get("ResonForRefund"),
            DescriptionOfReason=request.POST.get("DescriptionOfReason"),
            DeclarationIndigator=request.POST.get("DeclareIndicator"),
            AdditionalInfo=request.POST.get("AdditionalInfo"),
            TouchUser=request.POST.get("TouchUser"),
            TouchTme=request.POST.get('TouchTime'),
            MsgId=request.POST.get('MSGId'),
        )
        if RefundValSummary.objects.filter(MsgId=request.POST.get('MSGId')).exists():
            RefundValSummary1 = RefundValSummary.objects.filter(MsgId=request.POST.get('MSGId')).update
        else:
            RefundValSummary1 = RefundValSummary.objects.create
        RefundValSummary1(
            PermitId=request.POST.get("PermitId"),
            TotalGstAmt=request.POST.get("TotalGstAmt"),
            TotalExciseAmt=request.POST.get("TotalExciseAmt"),
            TxtCusdutyAmt=request.POST.get("TxtCusdutyAmt"),
            TxtOtherAmt=request.POST.get("TxtOtherAmt"),
            MsgId=request.POST.get('MSGId'),
        )

    if "CNL" == request.POST.get('CancelUpdateIndicator'):
        if InpaymentCancel.objects.filter(MsgId=request.POST.get('MSGId')).exists():
            cancelData = InpaymentCancel.objects.filter(MsgId=request.POST.get('MSGId')).update
        else:
            cancelData = InpaymentCancel.objects.create
        cancelData(
            PermitNo=request.POST.get('CancelPermitNo'),
            UpdateIndicator=request.POST.get('CancelUpdateIndicator'),
            ReplacementPermitno=request.POST.get('CancelReplacementPermitno'),
            ResonForCancel=request.POST.get('ResonForCancel'),
            DescriptionOfReason=request.POST.get('CancelDescriptionOfReason'),
            DeclarationIndigator=request.POST.get('DeclareIndicator'),
            TouchUser=request.POST.get("TouchUser"),
            TouchTme=request.POST.get('TouchTime'),
            MsgId=request.POST.get('MSGId'),
            CancelType=request.POST.get('CancelType')
        )
    if "AME" == request.POST.get('AmendUpdateIndicator'):
        if InpaymentAmend.objects.filter(MsgId=request.POST.get("MSGId")).exists():
            amend = InpaymentAmend.objects.filter(MsgId=request.POST.get("MSGId")).update
        else:
            amend = InpaymentAmend.objects.create
        amend(
            PermitNo=request.POST.get("AmendPermitNo"),
            AmendMentCount=request.POST.get("AmendMentCount"),
            UpdateIndicator=request.POST.get("AmendUpdateIndicator"),
            ReplacementPermitno=request.POST.get("AmendReplacementPermitno"),
            DescriptionOfReason=request.POST.get("AmendDescriptionOfReason"),
            PermitExtension=request.POST.get("AmendPermitExtension"),
            ExtendImportPeriod=request.POST.get("AmendExtendImportPeriod"),
            DeclarationIndigator=request.POST.get("DeclareIndicator"),
            TouchUser=request.POST.get("TouchUser"),
            TouchTme=request.POST.get('TouchTime'),
            MsgId=request.POST.get("MSGId"),
            AmendType=request.POST.get("AmendType")
        )

    if InheaderTbl.objects.filter(PermitId=PermitId).exists():
        Update = InheaderTbl.objects.filter(PermitId=PermitId).update
        PCount = PermitCount.objects.filter(PermitId=PermitId).update
    else:
        Update = InheaderTbl.objects.create
        PCount = PermitCount.objects.create
    Update(
        Refid=request.POST.get('Refid'),
        JobId=request.POST.get('JobId'),
        MSGId=request.POST.get('MSGId'),
        PermitId=request.POST.get('PermitId'),
        TradeNetMailboxID=request.POST.get('TradeNetMailboxID'),
        MessageType=request.POST.get('MessageType'),
        DeclarationType=request.POST.get('DeclarationType'),
        PreviousPermit=request.POST.get('PreviousPermit'),
        CargoPackType=request.POST.get('CargoPackType'),
        InwardTransportMode=request.POST.get('InwardTransportMode'),
        BGIndicator=request.POST.get('BGIndicator'),
        SupplyIndicator=request.POST.get('SupplyIndicator'),
        ReferenceDocuments=request.POST.get('ReferenceDocuments'),
        License=request.POST.get('License'),
        Recipient=request.POST.get('Recipient'),
        DeclarantCompanyCode=request.POST.get('DeclarantCompanyCode'),
        ImporterCompanyCode=request.POST.get('ImporterCompanyCode'),
        InwardCarrierAgentCode=request.POST.get('InwardCarrierAgentCode'),
        FreightForwarderCode=request.POST.get('FreightForwarderCode'),
        ClaimantPartyCode=request.POST.get('ClaimantPartyCode'),
        HBL=request.POST.get('HBL'),
        ArrivalDate=request.POST.get('ArrivalDate'),
        LoadingPortCode=request.POST.get('LoadingPortCode'),
        VoyageNumber=request.POST.get('VoyageNumber'),
        VesselName=request.POST.get('VesselName'),
        OceanBillofLadingNo=request.POST.get('OceanBillofLadingNo'),
        ConveyanceRefNo=request.POST.get('ConveyanceRefNo'),
        TransportId=request.POST.get('TransportId'),
        FlightNO=request.POST.get('FlightNO'),
        AircraftRegNo=request.POST.get('AircraftRegNo'),
        MasterAirwayBill=request.POST.get('MasterAirwayBill'),
        ReleaseLocation=request.POST.get('ReleaseLocation'),
        ReleaseLocName=request.POST.get('ReleaseLocName'),
        RecepitLocation=request.POST.get('RecepitLocation'),
        TotalOuterPack=request.POST.get('TotalOuterPack'),
        TotalOuterPackUOM=request.POST.get('TotalOuterPackUOM'),
        TotalGrossWeight=request.POST.get('TotalGrossWeight'),
        TotalGrossWeightUOM=request.POST.get('TotalGrossWeightUOM'), 
        GrossReference=request.POST.get('GrossReference'),
        BlanketStartDate=request.POST.get('BlanketStartDate'),
        TradeRemarks=request.POST.get('TradeRemarks'),
        InternalRemarks=request.POST.get('InternalRemarks'),
        CustomerRemarks=request.POST.get('CustomerRemarks'),
        DeclareIndicator=request.POST.get('DeclareIndicator'),
        NumberOfItems=request.POST.get('NumberOfItems'),
        TotalCIFFOBValue=request.POST.get('TotalCIFFOBValue'),
        TotalGSTTaxAmt=request.POST.get('TotalGSTTaxAmt'),
        TotalExDutyAmt=request.POST.get('TotalExDutyAmt'),
        TotalCusDutyAmt=request.POST.get('TotalCusDutyAmt'),
        TotalODutyAmt=request.POST.get('TotalODutyAmt'),
        TotalAmtPay=request.POST.get('TotalAmtPay'),
        Status=request.POST.get('Status'),
        TouchUser=request.POST.get('TouchUser'),
        TouchTime=request.POST.get('TouchTime'),
        PermitNumber=request.POST.get('PermitNumber'),
        prmtStatus=request.POST.get('prmtStatus'),
        RecepitLocName=request.POST.get('RecepitLocName'),
        Cnb=request.POST.get('Cnb'),
        DeclarningFor=request.POST.get('DeclarningFor'),
        MRDate=request.POST.get('MRDate'),
        MRTime=request.POST.get('MRTime'),
    )
    PCount(
        PermitId=request.POST.get('PermitId'),
        MessageType=request.POST.get('MessageType'),
        AccountId=AccountId,
        MsgId=request.POST.get('MSGId'),
        TouchUser=request.POST.get('TouchUser'),
        TouchTime=request.POST.get('TouchTime')
    )

    return JsonResponse({'Result': "Saved"})
