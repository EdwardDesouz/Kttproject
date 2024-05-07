

from django.http.response import HttpResponse
import xlwt
from .models import *


def InpaymentDownloadData(request, data):
    Headerrow_num = 0
    Containerrow_num = 0 
    InvoiceWorkrow_num = 0
    ItemWorkRow_num = 0
    CascRow_num = 0
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    headerWork = wb.add_sheet('Header')

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    bg_color = xlwt.Pattern()
    bg_color.pattern = xlwt.Pattern.SOLID_PATTERN
    bg_color.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
    font_style.pattern = bg_color

    columns = ['Id', 'Refid', 'JobId', 'MSGId', 'PermitId', 'TradeNetMailboxID', 'MessageType', 'DeclarationType', 'PreviousPermit', 'CargoPackType', 'InwardTransportMode', 'BGIndicator', 'SupplyIndicator', 'ReferenceDocuments', 'License', 'Recipient', 'DeclarantCompanyCode', 'ImporterCompanyCode', 'InwardCarrierAgentCode', 'FreightForwarderCode', 'ClaimantPartyCode', 'HBL', 'ArrivalDate', 'LoadingPortCode', 'VoyageNumber', 'VesselName', 'OceanBillofLadingNo', 'ConveyanceRefNo', 'TransportId', 'FlightNO', 'AircraftRegNo',
               'MasterAirwayBill', 'ReleaseLocation', 'ReleaseLocName', 'RecepitLocation', 'TotalOuterPack', 'TotalOuterPackUOM', 'TotalGrossWeight', 'TotalGrossWeightUOM', 'GrossReference', 'BlanketStartDate', 'TradeRemarks', 'InternalRemarks', 'CustomerRemarks', 'DeclareIndicator', 'NumberOfItems', 'TotalCIFFOBValue', 'TotalGSTTaxAmt', 'TotalExDutyAmt', 'TotalCusDutyAmt', 'TotalODutyAmt', 'TotalAmtPay', 'Status', 'TouchUser', 'TouchTime', 'PermitNumber', 'prmtStatus', 'RecepitLocName', 'Cnb', 'DeclarningFor', 'MRDate', 'MRTime']

    for col_num in range(len(columns)):
        headerWork.write(Headerrow_num, col_num, columns[col_num], font_style)

    ContainerWork = wb.add_sheet('Container')

    columns = ['Id', 'PermitId', 'RowNo', 'ContainerNo', 'size','weight', 'SealNo', 'MessageType', 'TouchUser', 'TouchTime']

    for col_num in range(len(columns)):
        ContainerWork.write(Containerrow_num, col_num,columns[col_num], font_style)

    InvoiceWork = wb.add_sheet('Invoice')

    columns = ['Id', "SNo", "InvoiceNo", "InvoiceDate", "TermType", "AdValoremIndicator", "PreDutyRateIndicator", "SupplierImporterRelationship", "SupplierCode", "ImportPartyCode", "TICurrency", "TIExRate", "TIAmount", "TISAmount", "OTCCharge", "OTCCurrency", "OTCExRate",
               "OTCAmount", "OTCSAmount", "FCCharge", "FCCurrency", "FCExRate", "FCAmount", "FCSAmount", "ICCharge", "ICCurrency", "ICExRate", "ICAmount", "ICSAmount", "CIFSUMAmount", "GSTPercentage", "GSTSUMAmount", "MessageType", "PermitId", "TouchUser", "TouchTime", "ChkOtherInv",]

    for col_num in range(len(columns)):
        InvoiceWork.write(InvoiceWorkrow_num, col_num,columns[col_num], font_style)

    ItemWork = wb.add_sheet('Item')

    columns = ["Id", "ItemNo", "PermitId", "MessageType", "HSCode", "Description", "DGIndicator", "Contry", "Brand", "Model", "InHAWBOBL", "DutiableQty", "DutiableUOM", "TotalDutiableQty", "TotalDutiableUOM",
               "HSQty", "HSUOM", "AlcoholPer", "InvoiceNo", "ChkUnitPrice", "UnitPrice", "UnitPriceCurrency", "ExchangeRate", "SumExchangeRate", "TotalLineAmount", "InvoiceCharges", "CIFFOB",
               "OPQty", "OPUOM", "IPQty", "IPUOM", "InPqty", "InPUOM", "ImPQty", "ImPUOM", "PreferentialCode", "GSTRate", "GSTUOM", "GSTAmount", "ExciseDutyRate", "ExciseDutyUOM", "ExciseDutyAmount",
               "CustomsDutyRate", "CustomsDutyUOM", "CustomsDutyAmount", "OtherTaxRate", "OtherTaxUOM", "OtherTaxAmount", "CurrentLot", "PreviousLot", "LSPValue", "Making",
               "ShippingMarks1", "ShippingMarks2", "ShippingMarks3", "ShippingMarks4", "TouchUser", "TouchTime", "VehicleType", "EngineCapcity", "EngineCapUOM", "orignaldatereg",
               "OptionalChrgeUOM", "Optioncahrge", "OptionalSumtotal", "OptionalSumExchage", "InvoiceQuantity"]

    for col_num in range(len(columns)):
        ItemWork.write(ItemWorkRow_num, col_num, columns[col_num], font_style)

    
    CascWork = wb.add_sheet('Casc')

    columns = ["Id","ItemNo","ProductCode", "Quantity","ProductUOM", "RowNo","CascCode1","CascCode2","CascCode3","PermitId", "MessageType","TouchUser","TouchTime","CascId"]

    for col_num in range(len(columns)):
        CascWork.write(CascRow_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    font_style.font.bold = False
    odd_row_style = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue;')
    even_row_style = xlwt.easyxf('pattern: pattern solid, fore_colour white;')

    for PermitId in data.split(','):
        rows = InheaderTbl.objects.filter(PermitId=PermitId).values_list('id', 'Refid', 'JobId', 'MSGId', 'PermitId', 'TradeNetMailboxID', 'MessageType', 'DeclarationType', 'PreviousPermit', 'CargoPackType', 'InwardTransportMode',
                                                                         'BGIndicator', 'SupplyIndicator', 'ReferenceDocuments', 'License', 'Recipient', 'DeclarantCompanyCode', 'ImporterCompanyCode', 'InwardCarrierAgentCode', 'FreightForwarderCode',
                                                                         'ClaimantPartyCode', 'HBL', 'ArrivalDate', 'LoadingPortCode', 'VoyageNumber', 'VesselName', 'OceanBillofLadingNo', 'ConveyanceRefNo', 'TransportId', 'FlightNO',
                                                                         'AircraftRegNo', 'MasterAirwayBill', 'ReleaseLocation', 'ReleaseLocName', 'RecepitLocation', 'TotalOuterPack', 'TotalOuterPackUOM', 'TotalGrossWeight',
                                                                         'TotalGrossWeightUOM', 'GrossReference', 'BlanketStartDate', 'TradeRemarks', 'InternalRemarks', 'CustomerRemarks', 'DeclareIndicator', 'NumberOfItems', 'TotalCIFFOBValue',
                                                                         'TotalGSTTaxAmt', 'TotalExDutyAmt', 'TotalCusDutyAmt', 'TotalODutyAmt', 'TotalAmtPay', 'Status', 'TouchUser', 'TouchTime', 'PermitNumber', 'prmtStatus', 'RecepitLocName', 'Cnb',
                                                                         'DeclarningFor', 'MRDate', 'MRTime')
        for row in rows:
            Headerrow_num += 1
            style = odd_row_style if Headerrow_num % 2 == 0 else even_row_style
            for col_num in range(len(row)):
                headerWork.write(Headerrow_num, col_num,row[col_num], style)

        rows = ContainerDtl.objects.filter(PermitId=PermitId).order_by('RowNo').values_list('id', 'PermitId', 'RowNo', 'ContainerNo', 'size', 'weight', 'SealNo', 'MessageType', 'TouchUser', 'TouchTime')
        for row in rows:
            Containerrow_num += 1
            style = odd_row_style if Containerrow_num % 2 == 0 else even_row_style
            for col_num in range(len(row)):
                ContainerWork.write(Containerrow_num, col_num,row[col_num], style)

        rows = InvoiceDtl.objects.filter(PermitId=PermitId).order_by('SNo').values_list('id', "SNo", "InvoiceNo", "InvoiceDate", "TermType", "AdValoremIndicator", "PreDutyRateIndicator", "SupplierImporterRelationship", "SupplierCode", "ImportPartyCode", "TICurrency", "TIExRate", "TIAmount", "TISAmount", "OTCCharge",
                                                                        "OTCCurrency", "OTCExRate", "OTCAmount", "OTCSAmount", "FCCharge", "FCCurrency", "FCExRate", "FCAmount", "FCSAmount", "ICCharge", "ICCurrency", "ICExRate", "ICAmount", "ICSAmount", "CIFSUMAmount", "GSTPercentage", "GSTSUMAmount", "MessageType", "PermitId", "TouchUser", "TouchTime", "ChkOtherInv")
        for row in rows:
            InvoiceWorkrow_num += 1
            style = odd_row_style if InvoiceWorkrow_num % 2 == 0 else even_row_style
            for col_num in range(len(row)):
                InvoiceWork.write(InvoiceWorkrow_num, col_num,row[col_num], style)

        rows = ItemDtl.objects.filter(PermitId=PermitId).order_by('ItemNo').values_list("id", "ItemNo", "PermitId", "MessageType", "HSCode", "Description", "DGIndicator", "Contry", "Brand", "Model", "InHAWBOBL", "DutiableQty", "DutiableUOM", "TotalDutiableQty", "TotalDutiableUOM",
                                                                     "HSQty", "HSUOM", "AlcoholPer", "InvoiceNo", "ChkUnitPrice", "UnitPrice", "UnitPriceCurrency", "ExchangeRate", "SumExchangeRate", "TotalLineAmount", "InvoiceCharges", "CIFFOB",
                                                                     "OPQty", "OPUOM", "IPQty", "IPUOM", "InPqty", "InPUOM", "ImPQty", "ImPUOM", "PreferentialCode", "GSTRate", "GSTUOM", "GSTAmount", "ExciseDutyRate", "ExciseDutyUOM", "ExciseDutyAmount",
                                                                     "CustomsDutyRate", "CustomsDutyUOM", "CustomsDutyAmount", "OtherTaxRate", "OtherTaxUOM", "OtherTaxAmount", "CurrentLot", "PreviousLot", "LSPValue", "Making",
                                                                     "ShippingMarks1", "ShippingMarks2", "ShippingMarks3", "ShippingMarks4", "TouchUser", "TouchTime", "VehicleType", "EngineCapcity", "EngineCapUOM", "orignaldatereg",
                                                                     "OptionalChrgeUOM", "Optioncahrge", "OptionalSumtotal", "OptionalSumExchage", "InvoiceQuantity")
        for row in rows:
            ItemWorkRow_num += 1
            style = odd_row_style if ItemWorkRow_num % 2 == 0 else even_row_style
            for col_num in range(len(row)):
                ItemWork.write(ItemWorkRow_num, col_num,row[col_num], style)

        rows = Cascdtl.objects.filter(PermitId=PermitId).order_by('ItemNo').values_list("id","ItemNo","ProductCode", "Quantity","ProductUOM", "RowNo","CascCode1","CascCode2","CascCode3","PermitId", "MessageType","TouchUser","TouchTime","CascId")
        for row in rows:
            CascRow_num += 1
            style = odd_row_style if CascRow_num % 2 == 0 else even_row_style
            for col_num in range(len(row)):
                CascWork.write(CascRow_num, col_num,row[col_num], style)

    wb.save(response)

    return response
