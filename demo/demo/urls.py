from django.conf.urls import include, url

from demo.views import common
from demo.views.visadirect import fundstransfer, mvisa, reports, watchlist
from demo.views.pav import pav
from demo.views.dcas import cardinquiry
from demo.views.merchantsearch import search
from demo.views.paai.fundstransferattinq.cardattributes.fundstransferinquiry import funds_transfer_inquiry
from demo.views.paai.generalattinq.cardattributes.generalinquiry import general_inquiry

urlpatterns = [
    url(r'^$', common.index),
    # Payment Account Attributes Inquiry
    url(r'^paai$', common.paai, name='paai'),
    url(r'^paai/', include([
        url(r'^fundstransferattinq/cardattributes/fundstransferinquiry$', funds_transfer_inquiry, name='paai_fti'),
        url(r'^generalattinq/cardattributes/generalinquiry$', general_inquiry, name='paai_gi')
    ])),
    # Merchant search
    url(r'^merchantsearch$', common.merchantsearch, name='merchantsearch'),
    url(r'^merchantsearch/', include([
        url(r'^search$', search.merchant_search, name='merchantsearch_search'),
    ])),
    # Payment account validation methods urls
    url(r'^pav$', common.pav, name='pav'),
    url(r'^pav/', include([
        url(r'^cardvalidation$', pav.card_validation, name='pav_cardvalidation')
    ])),
    # Digital card and account services
    url(r'^dcas$', common.dcas, name='dcas'),
    url(r'^dcas/', include([
        url(r'^cardinquiry$', cardinquiry.debit_card_inquiry, name='dcas_debitcardinquiry')
    ])),
    # VISA Direct methods urls
    url(r'^visadirect$', common.visa_direct, name='vd'),
    url(r'^visadirect/', include([
        # FundsTransfer API
        url(r'^fundstransfer$', fundstransfer.index, name='vd_ft'),
        url(r'^fundstransfer/', include([
            url(r'^pullfunds$', fundstransfer.pull, name='vd_ft_pullfunds'),
            url(r'^pushfunds$', fundstransfer.push, name='vd_ft_pushfunds'),
            url(r'^reversefunds$', fundstransfer.reverse, name='vd_ft_reversefunds'),
        ])),
        # mVISA API
        url(r'^mvisa$', mvisa.index, name='vd_mvisa'),
        url(r'^mvisa/', include([
            url(r'^cashinpushpayments$', mvisa.cipp, name='vd_mvisa_cipp'),
            url(r'^cashoutpushpayments$', mvisa.copp, name='vd_mvisa_copp'),
            url(r'^merchantpushpayments$', mvisa.mpp, name='vd_mvisa_mpp'),
        ])),
        # Reports API
        url(r'^reports$', reports.index, name='vd_reports'),
        url(r'^reports/', include([
            url(r'^transactiondata$', reports.transactiondata, name='vd_reports_transactiondata'),
        ])),
        # WatchList Inquiry methods urls
        url(r'^watchlist$', watchlist.index, name='vd_wl'),
        url(r'^watchlist/', include([
            url(r'^inquiry$', watchlist.inquiry, name='vd_wl_inquiry')
        ]))
    ])),
]
