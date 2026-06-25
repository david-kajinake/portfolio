from django.contrib import admin
from  .models import *

# Register your models here.
admin.site.register([
    Project ,
    Technology ,
    Contacter , 
    Message ,
    ExtraImage , 
    MyPhoneNumber , 
    MyEmail ,
    Service ,
    CustomQuestion
])
