from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from .data import mongo as imongodata
from .data.Imeili100Result import  Imeili100Result,Imeili100ResultStatus
from django.http import JsonResponse
import bson.json_util
import json
import  pymongo
import uuid
from . import settings
from pymongo.collection import  ReturnDocument
from django import  forms
class UploadFileForm(forms.Form):
    category = forms.IntegerField(max_value=10000);
    name = forms.CharField(max_length=50);
    intr = forms.CharField(max_length=50);
    website = forms.CharField(max_length=500);
    file = forms.ImageField;

def handle_uploaded_file(f,filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    return categoryPage(request)

def categoryPage(request):
    return render(request,'category.html',{"sideBarIndex":0})

def brandsPage(request):
    collection = imongodata.db['t_brands_category'];
    brands = json.loads( bson.json_util.dumps(list(collection.find())))
    return render(request,'brands.html',{"sideBarIndex":1,"brands":brands})

def getNextSequence(name):
    collection = imongodata.db['counters'];
    ret = collection.find_one_and_update({'_id':name},update={"$inc":{'seq':1}},upsert=True,return_document=ReturnDocument.AFTER);
    return ret.get('seq');

@csrf_exempt
def addCategory(request):
    categoryName = None
    if request.method == 'GET':
        categoryName = request.GET.get('name', None)
    elif request.method == 'POST':
        categoryName = request.POST.get('name', None)
    try:
        if categoryName != None:
            collection = imongodata.db['t_brands_category'];
            a = getNextSequence('t_brands_category');
            print(a)
            res = collection.insert_one({'idx':a,'name':categoryName})
        else:
            raise BaseException();
    except BaseException as e:
        print(e)
        imeilires = Imeili100Result()
        imeilires.status = Imeili100ResultStatus.failed.value
        imeilires.msg = "操作失败"
        return render(request,'result.html',imeilires.__dict__)
    else:
        imeilires = Imeili100Result()
        imeilires.status = Imeili100ResultStatus.ok.value
        imeilires.msg = "操作成功"
        return render(request,'result.html',imeilires.__dict__)

@csrf_exempt
def addBrand(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            imgName = uuid.uuid4().hex+".jpg";
            path = settings.UPLOAD_FOLDER+"/"+imgName;
            handle_uploaded_file(request.FILES['file'],path);
            collection = imongodata.db['t_brands'];
            data = form.cleaned_data
            ret = collection.insert_one({'name':data['name'],'category':data['category'],'website':data['website'],'img_name':imgName,'idx':getNextSequence('t_brands')})
    else:
        form = UploadFileForm()
    imeilires = Imeili100Result()
    imeilires.status = Imeili100ResultStatus.ok.value
    imeilires.msg = "操作成功";
    return render(request, 'result.html', imeilires.__dict__)


