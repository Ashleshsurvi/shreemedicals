
# Create your views here.
# from asyncio import exceptions
# from asyncio.windows_events import NULL
from asyncio.windows_events import NULL
import csv
from datetime import date
# from genericpath import exists
from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from shreemedicals.settings import *
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd
import datetime
import calendar


class index(APIView):
    def post(self,request):
        return Response('post')
    def get(self,request):
        return HttpResponse('get')
    


class Cad(APIView):
    def get(self,request):
        return HttpResponse("API does not exist contact developer")
    
    def post(self,request):
        f = request.FILES['file']
        filename=f.name
        filename=os.path.splitext(filename)
        filename=filename[0]
        
        data = pd.read_csv(f)
        vendor=[]
        disc=[]
        amt=[]
        inv_number=[]
        inv_date=[]
        # main start #
        try:
            vendor_name=request.data['vendor_name']
            vendor.append(vendor_name)
        except:
            vendor_name=None
            vendor.append(vendor_name)

        try:
            discount=request.data['Discount']
            if discount == NULL:
                discount==0     
                disc.append(discount)
            else:
                disc.append(discount)
        except:
            discount=0
            disc.append(discount)

        try:
            Amount=request.data['Amount']
            if Amount == None:
                Amount==0     
                amt.append(Amount)
            else:
                amt.append(Amount)
        except:
            Amount=0
            amt.append(Amount)


        invoice_number=data['feed_no_invoice_number'].astype('int64') 
        invoice_number=invoice_number.unique()[0]
        #invoice_number=float(invoice_number)
        invoice_number = f'{invoice_number:f}'
        inv_number.append(invoice_number)
        
        invoice_date=data['feeddate']
        invoice_date=invoice_date.unique()[0]
        dt=invoice_date
        dt_day=dt[0:2]
        dt_month=dt[3:5]
        dt_month = calendar.month_name[int(dt_month)]
        dt_year=dt[6:10]
        update_date=dt_day+'-'+dt_month+'-'+dt_year
        inv_date.append(update_date)

        #inv_date.append(invoice_date)
        #print(invoice_date)

        # main end #

        # table start #
        
        product=[]
        batchno=[]
        expiry=[]
        gst=[]
        packing=[]
        qty=[]
        rate=[]
        mrp=[]
        freeqty=[]
        discount_table=[]
        hsn=[]
        rack=[]
        box=[]

        product_data=data['prodname']
        for i in range(len(product_data)):
            product.append(product_data[i])
        
        batchno_data=data['batchno']
        for i in range(len(batchno_data)):
            batchno.append(batchno_data[i])
        
        expiry_data=data['expirys']
        for i in range(len(expiry_data)):
            dt=expiry_data[i]
            dt_day=dt[0:2]
            dt_month=dt[3:5]
            dt_month = calendar.month_name[int(dt_month)]
            dt_year=dt[6:10]
            update_date=dt_day+'-'+dt_month+'-'+dt_year
            expiry.append(update_date)
        
        sgst_data=data['sgstper']
        cgst_data=data['cgstper']
        for i in range(len(sgst_data)):
            gst.append(sgst_data[i]+cgst_data[i])

        packing_data=data['packing']
        for i in range(len(packing_data)):
            if 'm' in packing_data[i] or 'M' in packing_data[i]:
                updated_packing='1'
            else:
                updated_packing=packing_data[i]
                
            packing.append(updated_packing)
        
        qty_data=data['qty']
        for i in range(len(qty_data)):
            qty.append(qty_data[i])
        
        rate_data=data['rate']
        for i in range(len(rate_data)):
            rate.append(rate_data[i])
        
        mrp_data=data['mrp']
        for i in range(len(mrp_data)):
            mrp.append(mrp_data[i])
        
        freeqty_data=data['freeqty']
        for i in range(len(freeqty_data)):
            freeqty.append(freeqty_data[i])
        
        discount_table_data=data['prodname']
        for i in range(len(discount_table_data)):
            discount_table.append(discount)
        
        hsn_data=data['hsn']
        for i in range(len(hsn_data)):
            hsn.append(hsn_data[i])
        
        rack_data=data['prodname']
        for i in range(len(rack_data)):
            rack.append(0)
        
        box_data=data['prodname']
        for i in range(len(box_data)):
            box.append(0)

        main = {" VENDOR NAME": vendor, "INVOICE NO": inv_number, "INVOICE DATE": inv_date, "DISCOUNT": disc, "AMOUNT": amt}
        table={"PRODUCT NAME":product, "BATCH NO":batchno, "EXPIRY":expiry, "GST":gst, "UNIT/STRIP":packing, "NO OF STRIP":qty, "PRICE/STRIP":rate, "MRP":mrp, "FREE QTY":freeqty, "DISCOUNT":discount, "HSN":hsn, "RACK NO":rack, "BOX NO":box}
        df_main = pd.DataFrame(main)
        df_table = pd.DataFrame(table)
        filepath = str(BASE_DIR)+'/csvfiles/output.csv'
        

        if os.path.exists(filepath):
            print(filepath+'------------------------------------------exists')
        else:
            print(filepath+'-----------------------------------not-------exists')
            os.mkdir()

        df_main.to_csv(filepath,index=False)
        df_table.to_csv(filepath,index=False,mode='a')

        with open(filepath) as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename='+filename+'_output.csv'
            return response