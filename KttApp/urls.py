from django.urls import path
from KttApp import views
from KttApp import InpaymentSaveModel
from KttApp import Xml
from KttApp import PrintGst
from KttApp import CopyInpayment
from KttApp import PrintStatus
from KttApp import DownloadCcp
from KttApp import DownloadData
from KttApp import PrintCcp
from .views import *


from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("InpaymentList/",views.Inpayment),
    path("InpaymentNew/<arg>/",views.InpaymentNew),
    path("InpaymentHeaderUrl/",views.InpaymentHeader),
    path("InvoiceSave/",InpaymentSaveModel.InvoiceSave),
    path('InvoiceDelete/',InpaymentSaveModel.InvoiceDelete),
    path('ItemSaveUrl/',InpaymentSaveModel.ItemSave),
    path('CascDelete/',InpaymentSaveModel.CascDelete),
    path('ItemDelete/',InpaymentSaveModel.ItemDelete), 
    path('ItemAllDelte/',InpaymentSaveModel.ItemAllDelte),
    path('ItemExcelDownload/',views.ItemExcelDownload),
    path('ItemExcelUpload/',views.ItemExcelUpload),
    path('AllItemUpdate/',views.AllItemUpdate),
    path('InpaymentConsolidate/',views.ItemConsolidate),
    path('HeaderDocumentSave/',InpaymentSaveModel.DocumentSave),
    path('DocumentDelete/',InpaymentSaveModel.DocumentDelete),
    path('DocumentDeletePermitId/',InpaymentSaveModel.DocumentDeletPermitId),
    path('InpaymentSave/',InpaymentSaveModel.FinalSubmit),
    path('InpaymentXml/',Xml.XmlSubmit),
    path('PrintGst/<PermitId>/',PrintGst.PrintGst),
    path('CopytInpayment/',CopyInpayment.CopyInpayment),
    path('TransmitDataUrl/',CopyInpayment.TransmitDataFunction),
    path('EditInpayment/',views.EditInpayment),
    path('RefundLoad/',views.RefundLoad),
    path('CancelLoad/',views.CanceLoad), 
    path('AmendLoad/',views.AmendLoad),
    path('DeleteAllUrl/',views.DeleteAllFunction),
    path('headAttachDownload/<ID>/',views.headAttachDownloadFunction),
    path('InpaymentPrintStatus/<PermitId>/',PrintStatus.PrintStatus),
    path('InpaymentDownloadCcpZip/<data>/',DownloadCcp.InpaymentDownload),
    path('InpaymentDownloadData/<data>/',DownloadData.InpaymentDownloadData),
    # path('InpaymentCcpPdfUrl/<Data>/',PrintCcp.PdfCcp),
    path('LoadingPartyModels/',views.LoadingPartyModels),
    path('inpaymentItemDelHblHawb/',views.InpaymentItemDelHblHawb),
    path('ContainerDel/<arg>/',views.ContainerDel),
    path("CargoSave/",CargoPageSave.as_view()),
    path("Container/",ContainerSave.as_view()),
    path("PartyLoadDatas/",PartyPage.as_view()), 
    path("CpcLoad/",CpcLoadClass.as_view()),
    path("InvoiceInpayment/<PermitId>/",InvoiceInpayment.as_view()),
    path("ItemInpayment/<PermitId>/",ItemInpayment.as_view()),
    path("InPaymentItemLoad/",InPaymentItemLoad.as_view()),
    path("InpaymentCcpPdfUrl/<Data>/",InPaymentCcp.as_view())

]
 
router = DefaultRouter()

router.register("Inpayment/CascProductCodes",views.CascProductCodesViewSets,basename="CascProductCodes")
router.register("Inpayment/HsCode",views.HsCodeCodesViewSets,basename="HsCode")


urlpatterns += router.urls