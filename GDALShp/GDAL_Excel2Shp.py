#-*- coding: cp936 -*-
#������ؿ��
import osgeo,gdal,os,ogr,osr
import pandas as pd
from GDALShp.GDAL_ShowShp import showShp

#��ȡExcel�������
def readExcelbyFileNameAndSheetName(filename,sheetname):
    #����ͨ��sheet_name��ָ����ȡ�ı�
    df=pd.read_excel(filename,sheet_name=sheetname)
    columns = df.columns.values
    print("����б���",columns)
    data=df.values#��ȡȫ������
    print("��ȡ�����е�ֵ:\n{0}".format(data))#��ʽ�����
    return columns,data


#path��EXCEL�ļ�Ŀ¼��ExcelName��EXCEL�ļ�����shpfilename�������shp�ļ���
#Lng_columns_num����������������Lat_columns_numγ����������
def Excel2Shp(path,ExcelName,shpfilename,Lng_columns_num,Lat_columns_num):
    # Ϊ��֧������·�������������������
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
    # Ϊ��ʹ���Ա��ֶ�֧�����ģ�������������
    gdal.SetConfigOption("SHAPE_ENCODING","GB2312")
    # ע�����е�����
    ogr.RegisterAll()
    #�������shp
    driver = ogr.GetDriverByName('ESRI Shapefile')
    os.chdir(path)
    if os.path.exists(shpfilename):
        driver.DeleteDataSource(shpfilename)
    outds = driver.CreateDataSource(shpfilename)
    if outds == None:
        print('�����ļ�ʧ�ܣ�')
    #����ͼ��
    dst_osr = osr.SpatialReference()
    dst_osr.ImportFromEPSG(4326)
    #��ȡ�ļ�������������չ��
    layername = os.path.splitext(shpfilename)[0]
    print('layername:=='+layername)
    outlayer = outds.CreateLayer(layername,dst_osr,geom_type = ogr.wkbPoint)
    #��ȡEXCEL��ͷ������
    columns,data=readExcelbyFileNameAndSheetName(ExcelName,'Sheet1')
    #��ȡ��ͷ����
    columns_count = len(columns)
    print('columns_count==='+str(columns_count))

    #--------------------------�������Ա��ֶ�----------------------------------------
    #�������б�ͷ���������Ա��ֶ�
    for i in range(columns_count):
        FieldName = columns[i]
        print('FieldName==='+FieldName)

        #�����ֶ�����
        fieldDefn = ogr.FieldDefn(FieldName,ogr.OFTString)
        fieldDefn.SetWidth(100)
        #ͼ�㴴������
        outlayer.CreateField(fieldDefn)

    #---------------------------����Ҫ��-----------------------------------------------
    #��ȡҪ��ͳһ����
    featuredefn = outlayer.GetLayerDefn()

    #��ȡ��������
    rows_count = len(data)
    print('rows_count==='+str(rows_count))

    #�������������в���������д��shp�ֶ���
    for row in range(rows_count):
        #��ȡÿһ�е�X����WGS84_Lng������Ĳ����ǹ̶��ģ�Ӧ�ðѲ��������ȥ��д�
        # #���򻻸�������澭γ���ֶεı���˳�򣬾ͻ����
        point_x=float(data[row][Lng_columns_num-1])
        print('point_x==='+str(point_x))
        #��ȡÿһ�е�Y����WGS84_Lat
        point_y=float(data[row][Lat_columns_num-1])
        print('point_y==='+str(point_y))

        # ������Ҫ��
        oFeaturePoint = ogr.Feature(featuredefn)
        #---------------------------�����е�Ҫ�ص�����һһ��Ӧ���и�ֵ-----------------
        #���������У������е�Ҫ�ص�����һһ��Ӧ���и�ֵ
        for column in range(columns_count):
            #���������ֶ���������Ӧ�ö�ȡSHP���ֶ�����������EXCEL��ͷ�����ܻ��д����ֶ�ʱ��Ϊ�ֶ���̫������ʧ�����ֶ���
            FieldName = columns[column]
            print('FieldName==='+FieldName)
            #ÿ��cell������ֵ
            FieldValue = data[row][column]
            print('FieldValue==='+str(FieldValue))
            #�����ֶθ�ֵ
            oFeaturePoint.SetField(FieldName, FieldValue)

        #����ʸ��Ҫ��Ϊ��
        geomPoint = ogr.Geometry(ogr.wkbPoint)
        #������X,Y����ֵ
        geomPoint.AddPoint(point_x,point_y)
        #��Ҫ�����ü��ε���Ϣ
        oFeaturePoint.SetGeometry(geomPoint)
        #����Ҫ��
        outlayer.CreateFeature(oFeaturePoint)

    outds.Destroy()

#��������Ŀ¼
path ="D:\\GitHub\PyGdalStudy\\GDALShp\\Data"
#Ŀ¼�л�
os.chdir(path)
#EXCEL�ļ���
ExcelName='SpecialTownList.xlsx'
#���SHP�ļ���
shpfilename='SpecialTown.shp'
#���ú������������У�������23�У�γ����24��
Excel2Shp(path,ExcelName,shpfilename,23,24)
#��ʾSHP
showShp(shpfilename)
