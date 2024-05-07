from django.db import models

class ManageUser(models.Model):
    AccountId = models.CharField(max_length=550)
    UserId = models.CharField(max_length=550)
    UserName = models.CharField(max_length=550)
    Password = models.CharField(max_length=550)
    ConfirmPassword = models.CharField(max_length=550) 
    Department = models.CharField(max_length=550)
    Telephone = models.CharField(max_length=550) 
    Fax = models.CharField(max_length=550)
    Mobile = models.CharField(max_length=550)
    Email = models.CharField(max_length=550)
    Status = models.CharField(max_length=550)
    LoginStatus = models.CharField(max_length=550)
    AccountAdmin = models.CharField(max_length=550)
    B2BDocAdmin = models.CharField(max_length=550)
    DataEntryClerk = models.CharField(max_length=550)
    Declarent = models.CharField(max_length=550)
    OperationManager = models.CharField(max_length=550)
    UserCreated = models.CharField(max_length=550)
    DateCreated = models.CharField(max_length=550)
    UserLastUpdated = models.CharField(max_length=550)
    DateLastUpdated = models.CharField(max_length=550)
    Activeuser = models.CharField(max_length=550)
    MailBoxId = models.CharField(max_length=550)
    SeqPool = models.CharField(max_length=550)
    Customer = models.CharField(max_length=550)

    class Meta:
        db_table = "ManageUser"
        managed = True

from django.db import models

from datetime import *
import os


class CommonMaster(models.Model):
    Id = models.IntegerField()
    Name = models.CharField(max_length=500)
    Description = models.CharField(max_length=550)
    TypeId = models.IntegerField(null=True)
    TypeName = models.CharField(max_length=50)
    StatusId = models.IntegerField(null=True)
    StatusName = models.CharField(max_length=50)
    TouchUser = models.CharField(max_length=50)
    TouchTime = models.DateField(null=True)

    class Meta:
        db_table = 'CommonMaster'
        managed = True


class DeclarantCompany(models.Model):
    code = models.CharField(max_length=500)
    cruei = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    name1 = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    accountid = models.CharField(max_length=500)
    tradenetmailboxId = models.CharField(max_length=500)
    CurrentPassword = models.CharField(max_length=500)
    TradenetAccount = models.CharField(max_length=500)
    DeclarantName = models.CharField(max_length=500)
    DeclarantCode = models.CharField(max_length=500)
    DeclarantTel = models.CharField(max_length=500)
    AccountID = models.CharField(max_length=500)
    TouchUser = models.CharField(max_length=500)
    TouchTime = models.CharField(max_length=500)
    ValididityDate = models.CharField(max_length=500)
    Cmduser = models.CharField(max_length=500)

    class Meta:
        db_table = 'DeclarantCompany'
        managed = True


class Importer(models.Model):
    code = models.CharField(max_length=500)
    cruei = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    name1 = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    TouchUser = models.CharField(max_length=500)
    TouchTime = models.CharField(max_length=500)

    class Meta:
        db_table = 'Importer'
        managed = True


class InwardCarrierAgent(models.Model):
    code = models.CharField(max_length=500)
    cruei = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    name1 = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    TouchUser = models.CharField(max_length=500)
    TouchTime = models.CharField(max_length=500)

    class Meta:
        db_table = 'InwardCarrierAgent'
        managed = True


class FreightForwarder(models.Model):
    code = models.CharField(max_length=500)
    cruei = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    name1 = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    TouchUser = models.CharField(max_length=500)
    TouchTime = models.CharField(max_length=500)

    class Meta:
        db_table = 'FreightForwarder'
        managed = True


class ClaimantParty(models.Model):
    ClaimantCode = models.CharField(max_length=500)
    cruei = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    name1 = models.CharField(max_length=500)
    name2 = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    ClaimantName = models.CharField(max_length=500)
    ClaimantName1 = models.CharField(max_length=500)
    TouchUser = models.CharField(max_length=500)
    TouchTime = models.CharField(max_length=500)

    class Meta:
        db_table = 'ClaimantParty'
        managed = True


class LoadingPort(models.Model):
    portcode = models.CharField(max_length=500)
    portname = models.CharField(max_length=500)
    Country = models.CharField(max_length=500)

    class Meta:
        db_table = 'LoadingPort'
        managed = True
        managed = True


class ReleaseLocation(models.Model):
    locationCode = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    code = models.CharField(max_length=500)

    class Meta:
        db_table = 'ReleaseLocation'
        managed = True


class ReceiptLocation(models.Model):
    locationCode = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    code = models.CharField(max_length=500)

    class Meta:
        db_table = 'ReceiptLocation'
        managed = True


class SUPPLIERMANUFACTURERPARTY(models.Model):
    code = models.CharField(max_length=500)
    cruei = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    name1 = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    TouchUser = models.CharField(max_length=500)
    TouchTime = models.CharField(max_length=500)

    class Meta:
        db_table = 'SUPPLIERMANUFACTURERPARTY'
        managed = True


class Currency(models.Model):
    Id = models.CharField(max_length=500)
    Currency = models.CharField(max_length=500)
    CurrencyRate = models.CharField(max_length=500)
    CurrencyCountry = models.CharField(max_length=500)

    class Meta:
        db_table = 'Currency'
        managed = True

class InhouseItemCode(models.Model):
    InhouseCode = models.CharField(max_length=500)
    Hscode = models.CharField(max_length=500)
    Description = models.CharField(max_length=500)
    Brand = models.CharField(max_length=500)
    Model = models.CharField(max_length=500)
    DgIndicator = models.CharField(max_length=500)
    DeclType = models.CharField(max_length=500)
    ProductCode = models.CharField(max_length=500)
    TouchUser = models.CharField(max_length=500)
    TouchTime = models.CharField(max_length=500)
    class Meta:
        db_table = 'InhouseItemCode'


class InvoiceDtl(models.Model):
    SNo = models.CharField(max_length=500)
    InvoiceNo = models.CharField(max_length=550)
    InvoiceDate = models.CharField(max_length=500)
    TermType = models.CharField(max_length=500)
    AdValoremIndicator = models.CharField(max_length=500)
    PreDutyRateIndicator = models.CharField(max_length=500)
    SupplierImporterRelationship = models.CharField(max_length=500)
    SupplierCode = models.CharField(max_length=500)
    ImportPartyCode = models.CharField(max_length=500)
    TICurrency = models.CharField(max_length=550)
    TIExRate = models.CharField(max_length=500)
    TIAmount = models.CharField(max_length=500)
    TISAmount = models.CharField(max_length=500)
    OTCCharge = models.CharField(max_length=500)
    OTCCurrency = models.CharField(max_length=500)
    OTCExRate = models.CharField(max_length=500)
    OTCAmount = models.CharField(max_length=500)
    OTCSAmount = models.CharField(max_length=500)
    FCCharge = models.CharField(max_length=500)
    FCCurrency = models.CharField(max_length=500)
    FCExRate = models.CharField(max_length=550)
    FCAmount = models.CharField(max_length=500)
    FCSAmount = models.CharField(max_length=500)
    ICCharge = models.CharField(max_length=500)
    ICCurrency = models.CharField(max_length=500)
    ICExRate = models.CharField(max_length=500)
    ICAmount = models.CharField(max_length=500)
    ICSAmount = models.CharField(max_length=500)
    CIFSUMAmount = models.CharField(max_length=500)
    GSTPercentage = models.CharField(max_length=500)
    GSTSUMAmount = models.CharField(max_length=500)
    MessageType = models.CharField(max_length=500)
    PermitId = models.CharField(max_length=550)
    TouchUser = models.CharField(max_length=500)
    TouchTime = models.CharField(max_length=500)
    ChkOtherInv = models.CharField(max_length=500)
 
    class Meta:
        db_table = 'InvoiceDtl'
        managed = True


class HsCode(models.Model):
    HSCode = models.CharField(max_length=550)
    Description = models.CharField(max_length=500)
    Uom = models.CharField(max_length=500)
    Typeid = models.CharField(max_length=500)
    DUTYTYPID = models.CharField(max_length=500)
    Inpayment = models.CharField(max_length=500)
    InnonPayment = models.CharField(max_length=500)
    Out = models.CharField(max_length=500)
    Co = models.CharField(max_length=500)
    Transhipment = models.CharField(max_length=500)
    DuitableUom = models.CharField(max_length=500)
    Excisedutyuom = models.CharField(max_length=550)
    Excisedutyrate = models.CharField(max_length=500)
    Customsdutyuom = models.CharField(max_length=500)
    Customsdutyrate = models.CharField(max_length=500)
    Kgmvisible = models.CharField(max_length=500)

    class Meta:
        db_table = 'hsCode'
        managed = True


class ChkHsCode(models.Model):
    HsCode = models.CharField(
        max_length=550, db_column='HsCode', blank=True, primary_key=True)

    class Meta:
        db_table = 'ChkHsCode'
        managed = True


class COUNTRY(models.Model):
    CountryCode = models.CharField(max_length=500)
    Description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'COUNTRY'
        managed = True


class ItemDtl(models.Model):
    ItemNo = models.CharField(max_length=550)
    PermitId = models.CharField(max_length=550)
    MessageType = models.CharField(max_length=550)
    HSCode = models.CharField(max_length=550)
    Description = models.CharField(max_length=550)
    DGIndicator = models.CharField(max_length=550)
    Contry = models.CharField(max_length=550)
    Brand = models.CharField(max_length=550)
    Model = models.CharField(max_length=550)
    InHAWBOBL = models.CharField(max_length=550)
    DutiableQty = models.CharField(max_length=550)
    DutiableUOM = models.CharField(max_length=550)
    TotalDutiableQty = models.CharField(max_length=550)
    TotalDutiableUOM = models.CharField(max_length=550)
    HSQty = models.CharField(max_length=550)
    HSUOM = models.CharField(max_length=550)
    AlcoholPer = models.CharField(max_length=550)
    InvoiceNo = models.CharField(max_length=550)
    ChkUnitPrice = models.CharField(max_length=550)
    UnitPrice = models.CharField(max_length=550)
    UnitPriceCurrency = models.CharField(max_length=550)
    ExchangeRate = models.CharField(max_length=550)
    SumExchangeRate = models.CharField(max_length=550)
    TotalLineAmount = models.CharField(max_length=550)
    InvoiceCharges = models.CharField(max_length=550)
    CIFFOB = models.CharField(max_length=550)
    OPQty = models.CharField(max_length=550)
    OPUOM = models.CharField(max_length=550)
    IPQty = models.CharField(max_length=550)
    IPUOM = models.CharField(max_length=550)
    InPqty = models.CharField(max_length=550)
    InPUOM = models.CharField(max_length=550)
    ImPQty = models.CharField(max_length=550)
    ImPUOM = models.CharField(max_length=550)
    PreferentialCode = models.CharField(max_length=550)
    GSTRate = models.CharField(max_length=550)
    GSTUOM = models.CharField(max_length=550)
    GSTAmount = models.CharField(max_length=550)
    ExciseDutyRate = models.CharField(max_length=550)
    ExciseDutyUOM = models.CharField(max_length=550)
    ExciseDutyAmount = models.CharField(max_length=550)
    CustomsDutyRate = models.CharField(max_length=550)
    CustomsDutyUOM = models.CharField(max_length=550)
    CustomsDutyAmount = models.CharField(max_length=550)
    OtherTaxRate = models.CharField(max_length=550)
    OtherTaxUOM = models.CharField(max_length=550)
    OtherTaxAmount = models.CharField(max_length=550)
    CurrentLot = models.CharField(max_length=550)
    PreviousLot = models.CharField(max_length=550)
    LSPValue = models.CharField(max_length=550)
    Making = models.CharField(max_length=550)
    ShippingMarks1 = models.CharField(max_length=550)
    ShippingMarks2 = models.CharField(max_length=550)
    ShippingMarks3 = models.CharField(max_length=550)
    ShippingMarks4 = models.CharField(max_length=550)
    TouchUser = models.CharField(max_length=550)
    TouchTime = models.CharField(max_length=550)
    VehicleType = models.CharField(max_length=550)
    EngineCapcity = models.CharField(max_length=550)
    EngineCapUOM = models.CharField(max_length=550)
    orignaldatereg = models.CharField(max_length=550)
    OptionalChrgeUOM = models.CharField(max_length=550)
    Optioncahrge = models.CharField(max_length=550) 
    OptionalSumtotal = models.CharField(max_length=550)
    OptionalSumExchage = models.CharField(max_length=550)
    InvoiceQuantity = models.CharField(max_length=550)

    class Meta:
        db_table = 'ItemDtl'
        managed = True


class InheaderTbl(models.Model):
    Refid = models.CharField(max_length=550)
    JobId = models.CharField(max_length=550)
    MSGId = models.CharField(max_length=550)
    PermitId = models.CharField(max_length=550)
    TradeNetMailboxID = models.CharField(max_length=550)
    MessageType = models.CharField(max_length=550)
    DeclarationType = models.CharField(max_length=550)
    PreviousPermit = models.CharField(max_length=550)
    CargoPackType = models.CharField(max_length=550)
    InwardTransportMode = models.CharField(max_length=550)
    BGIndicator = models.CharField(max_length=550)
    SupplyIndicator = models.CharField(max_length=550)
    ReferenceDocuments = models.CharField(max_length=550)
    License = models.CharField(max_length=550)
    Recipient = models.CharField(max_length=550)
    DeclarantCompanyCode = models.CharField(max_length=550)
    ImporterCompanyCode = models.CharField(max_length=550)
    InwardCarrierAgentCode = models.CharField(max_length=550)
    FreightForwarderCode = models.CharField(max_length=550)
    ClaimantPartyCode = models.CharField(max_length=550)
    HBL = models.CharField(max_length=550)
    ArrivalDate = models.CharField(max_length=550)
    LoadingPortCode = models.CharField(max_length=550)
    VoyageNumber = models.CharField(max_length=550)
    VesselName = models.CharField(max_length=550)
    OceanBillofLadingNo = models.CharField(max_length=550)
    ConveyanceRefNo = models.CharField(max_length=550)
    TransportId = models.CharField(max_length=550)
    FlightNO = models.CharField(max_length=550)
    AircraftRegNo = models.CharField(max_length=550)
    MasterAirwayBill = models.CharField(max_length=550)
    ReleaseLocation = models.CharField(max_length=550)
    ReleaseLocName = models.CharField(max_length=550)
    RecepitLocation = models.CharField(max_length=550)
    TotalOuterPack = models.CharField(max_length=550)
    TotalOuterPackUOM = models.CharField(max_length=550)
    TotalGrossWeight = models.CharField(max_length=550)
    TotalGrossWeightUOM = models.CharField(max_length=550)
    GrossReference = models.CharField(max_length=550)
    BlanketStartDate = models.CharField(max_length=550)
    TradeRemarks = models.CharField(max_length=550)
    InternalRemarks = models.CharField(max_length=550)
    CustomerRemarks = models.CharField(max_length=550)
    DeclareIndicator = models.CharField(max_length=550)
    NumberOfItems = models.CharField(max_length=550)
    TotalCIFFOBValue = models.CharField(max_length=550)
    TotalGSTTaxAmt = models.CharField(max_length=550)
    TotalExDutyAmt = models.CharField(max_length=550)
    TotalCusDutyAmt = models.CharField(max_length=550)
    TotalODutyAmt = models.CharField(max_length=550)
    TotalAmtPay = models.CharField(max_length=550)
    Status = models.CharField(max_length=550)
    TouchUser = models.CharField(max_length=550)
    TouchTime = models.CharField(max_length=550)
    PermitNumber = models.CharField(max_length=550)
    prmtStatus = models.CharField(max_length=550)
    RecepitLocName = models.CharField(max_length=550)
    Cnb = models.CharField(max_length=550)
    DeclarningFor = models.CharField(max_length=550)
    MRDate = models.CharField(max_length=550)
    MRTime = models.CharField(max_length=550)

    class Meta:
        db_table = "InHeaderTbl"
        managed = True


class PermitCount(models.Model):
    PermitId = models.CharField(max_length=550)
    MessageType = models.CharField(max_length=550)
    AccountId = models.CharField(max_length=550)
    MsgId = models.CharField(max_length=550)
    TouchUser = models.CharField(max_length=550)
    TouchTime = models.CharField(max_length=550)

    class Meta:
        db_table = "PermitCount"
        managed = True


class CascProductCodes(models.Model):
    CASCCode = models.CharField(max_length=550)
    Description = models.CharField(max_length=550) 
    UOM = models.CharField(max_length=550)
    HSCode = models.CharField(max_length=550)

    class Meta:
        db_table = "CascProductCodes"
        managed = True


class Cascdtl(models.Model):
    ItemNo = models.CharField(max_length=100)
    ProductCode = models.CharField(max_length=400)
    Quantity = models.CharField(max_length=400)
    ProductUOM = models.CharField(max_length=400)
    RowNo = models.CharField(max_length=400)
    CascCode1 = models.CharField(max_length=400)
    CascCode2 = models.CharField(max_length=400)
    CascCode3 = models.CharField(max_length=400)
    PermitId = models.CharField(max_length=400)
    MessageType = models.CharField(max_length=400)
    TouchUser = models.CharField(max_length=400)
    TouchTime = models.CharField(max_length=400)
    CascId = models.CharField(max_length=400)

    class Meta:
        db_table = 'CascDtl'
        managed = True


class ContainerDtl(models.Model):
    PermitId = models.CharField(max_length=400)
    RowNo = models.CharField(max_length=100)
    ContainerNo = models.CharField(max_length=400)
    size = models.CharField(max_length=400)
    weight = models.CharField(max_length=400)
    SealNo = models.CharField(max_length=400)
    MessageType = models.CharField(max_length=400)
    TouchUser = models.CharField(max_length=400)
    TouchTime = models.CharField(max_length=400)

    class Meta:
        db_table = 'ContainerDtl'
        managed = True


class CpcDtl(models.Model):
    PermitId = models.CharField(max_length=400)
    MessageType = models.CharField(max_length=400)
    RowNo = models.CharField(max_length=100)
    CpcType = models.CharField(max_length=100)
    ProcessingCode1 = models.CharField(max_length=100)
    ProcessingCode2 = models.CharField(max_length=100)
    ProcessingCode3 = models.CharField(max_length=100)
    TouchUser = models.CharField(max_length=400)
    TouchTime = models.CharField(max_length=400)

    class Meta:
        db_table = 'CpcDtl'
        managed = True


def INFILE(request, filename):
    nowTime = date.now().strftime('%d:%m:%y:%H:%M')
    newFile = ('%s%s' % (nowTime, filename))
    return os.path.join('uploads/', newFile)


class InFile(models.Model):  # models.FileField(upload_to = INFILE)
    Sno = models.CharField(max_length=400)
    Name = models.CharField(max_length=400)
    ContentType = models.CharField(max_length=400)
    Data = models.CharField(max_length=400)
    DocumentType = models.CharField(max_length=400)
    InPaymentId = models.CharField(max_length=400)
    TouchUser = models.CharField(max_length=400)
    TouchTime = models.CharField(max_length=400)
    FilePath = models.CharField(max_length=400)
    Size = models.CharField(max_length=400)
    PermitId = models.CharField(max_length=400)
    Type = models.CharField(max_length=100)

    class Meta:
        db_table = 'InFile'
        managed = True


class Inpmt(models.Model):
    Sno = models.CharField(max_length=400)
    PermitNumber = models.CharField(max_length=400)
    CertificateNumber = models.CharField(max_length=400)
    StartDate = models.CharField(max_length=400)
    EndDate = models.CharField(max_length=400)
    CAApprovalDatetime = models.CharField(max_length=400)
    PermitApprovalDatetime = models.CharField(max_length=400)
    AgencyCode = models.CharField(max_length=400)
    Conditioncode = models.CharField(max_length=400)
    ConditionDescription = models.CharField(max_length=400)
    class Meta:
        db_table = "Inpmt"
        managed = True   

class RejectStatus(models.Model):
    Sno = models.CharField(max_length=400)
    MsgId = models.CharField(max_length=400)
    IssuingAuthorityId = models.CharField(max_length=400)
    CommonAccessReference = models.CharField(max_length=400)
    StatusType = models.CharField(max_length=400)
    ErrorId = models.CharField(max_length=400)
    ErrorDescription = models.CharField(max_length=400)
    ErrorSno = models.CharField(max_length=400)
    MailBoxId = models.CharField(max_length=400)
    Rtype = models.CharField(max_length=400)
    class Meta:
        db_table = "RejectStatus"
        managed = True   

class InCancel(models.Model):
    Sno = models.CharField(max_length=400)
    MsgId = models.CharField(max_length=400)
    PermitNumber = models.CharField(max_length=400)
    CancelDate = models.CharField(max_length=400)
    ConditionCde = models.CharField(max_length=400)
    ConditionDes = models.CharField(max_length=400)
    MailBoxId = models.CharField(max_length=400)
    class Meta:
        db_table = "InCancel"
        managed = True   

class CustomiseReport(models.Model):
    ReportName = models.CharField(max_length=400)
    Sno = models.CharField(max_length=400,blank=True, primary_key=True)
    FiledName = models.CharField(max_length=400)
    FiledValue = models.CharField(max_length=400)
    UserName = models.CharField(max_length=400)
    class Meta:
        db_table = "CustomiseReport"
        managed = True   


        
class InpaymentRefund(models.Model):
    PermitNo = models.CharField(max_length=400)
    UpdateIndicator = models.CharField(max_length=400)
    ReplacementPermitno = models.CharField(max_length=400)
    TypeOfRefund = models.CharField(max_length=400)
    ResonForRefund = models.CharField(max_length=400)
    DescriptionOfReason = models.CharField(max_length=400)
    DeclarationIndigator = models.CharField(max_length=400)
    AdditionalInfo = models.CharField(max_length=400)
    TouchUser = models.CharField(max_length=400)
    TouchTme = models.CharField(max_length=400)
    MsgId = models.CharField(max_length=400)
    class Meta:
        db_table = "InpaymentRefund"
        managed = True  

class RefundValSummary(models.Model):
    PermitId = models.CharField(max_length=400)
    TotalGstAmt = models.CharField(max_length=400)
    TotalExciseAmt = models.CharField(max_length=400)
    TxtCusdutyAmt = models.CharField(max_length=400)
    TxtOtherAmt = models.CharField(max_length=400)
    MsgId = models.CharField(max_length=400, primary_key=True)
    class Meta:
        db_table = "RefundValSummary"
        managed = True  

class ReundItemSumm(models.Model):
    PermitId = models.CharField(max_length=400)
    ItemNo = models.CharField(max_length=400)
    HsCode = models.CharField(max_length=400)
    TotalGstAmt = models.CharField(max_length=400)
    TotalExciseAmt = models.CharField(max_length=400)
    TxtCusdutyAmt = models.CharField(max_length=400)
    TxtOtherAmt = models.CharField(max_length=400)
    Sno = models.CharField(max_length=400 , primary_key=True)
    MsgId = models.CharField(max_length=400)
    class Meta:
        db_table = "ReundItemSumm"
        managed = False  

class InpaymentCancel(models.Model):
    PermitNo = models.CharField(max_length=400)
    UpdateIndicator = models.CharField(max_length=400)
    ReplacementPermitno = models.CharField(max_length=400)
    ResonForCancel = models.CharField(max_length=400)
    DescriptionOfReason = models.CharField(max_length=400)
    DeclarationIndigator = models.CharField(max_length=400)
    TouchUser = models.CharField(max_length=400)
    TouchTme = models.CharField(max_length=400)
    MsgId = models.CharField(max_length=400)
    CancelType = models.CharField(max_length=400)
    class Meta:
        db_table = "InpaymentCancel"
        managed = True  

class InpaymentAmend(models.Model):
    PermitNo = models.CharField(max_length=400)
    AmendMentCount = models.CharField(max_length=400)
    UpdateIndicator = models.CharField(max_length=400)
    ReplacementPermitno = models.CharField(max_length=400)
    DescriptionOfReason = models.CharField(max_length=400)
    PermitExtension = models.CharField(max_length=400)
    ExtendImportPeriod = models.CharField(max_length=400)
    DeclarationIndigator = models.CharField(max_length=400)
    TouchUser = models.CharField(max_length=400)
    TouchTme = models.CharField(max_length=400)
    MsgId = models.CharField(max_length=400)
    AmendType = models.CharField(max_length=400)
    class Meta:
        db_table = "InpaymentAmend"
        managed = True  


