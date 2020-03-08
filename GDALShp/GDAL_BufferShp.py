#-*- coding: cp936 -*-
import os
try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import gdal
    import ogr


def shpBuffer(strVectorFile,bufferVectorFile,layername):
    #-----------------------------GDAL����ע��-------------
    # Ϊ��֧������·�������������������
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
    # Ϊ��ʹ���Ա��ֶ�֧�����ģ�������������
    gdal.SetConfigOption("SHAPE_ENCODING","GB2312")
    # ע�����е�����
    ogr.RegisterAll()
    # �������ݣ������Դ���ESRI��shp�ļ�Ϊ��
    strDriverName = "ESRI Shapefile"
    oDriver =ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("%s ���������ã�\n", strDriverName)
        return
    #------------------------------------------------------

    #------------------------������----------------------
    ds = ogr.Open(strVectorFile, 0)
    #�ж��ļ��Ƿ����
    if ds == None:
        print("���ļ���%s��ʧ�ܣ�", strVectorFile)
        return
    #��ʾ�򿪳ɹ�
    print("���ļ���%s���ɹ���", strVectorFile)
    #------------------------------------------------------

    #-----------------��ȡָ��ͼ��-------------------------
    oLayer = ds.GetLayer('SpecialTown')
    if oLayer == None:
        print("��ȡ��%d��ͼ��ʧ�ܣ�\n", 0)
        return
    #ͼ�����
    oDefn = oLayer.GetLayerDefn()
    #------------------------------------------------------

    #------------------# ��������������Դ��ͼ��---------------------
    # �����������ļ�����Դ
    bufferDS =oDriver.CreateDataSource(bufferVectorFile)
    if bufferDS == None:
        print("�����ļ���%s��ʧ�ܣ�", bufferVectorFile)
        return
    #��ȡ�������ݵ�ͶӰ��Ϣ
    targetSR =oLayer.GetSpatialRef()
    papszLCO = []
    #��������ͼ��
    bufferLayer =bufferDS.CreateLayer(layername, targetSR, ogr.wkbPolygon, papszLCO)
    if bufferLayer == None:
        print("ͼ�㴴��ʧ�ܣ�\n")
        return
    #��ȡ������ͼ���Ҫ��
    buff_feat  = ogr.Feature(bufferLayer.GetLayerDefn())
    #------------------------------------------------------------

    #����ͼ���е�Ҫ��
    oLayer.ResetReading()
    for feat in oLayer:
        #����ÿһ��Ҫ�ز�����1KM�Ļ�����
        buff_geom = feat.geometry().Buffer(1000)
        #���建�����������ԴҪ�صļ�����ϢΪ�����������Ϣ
        bufferDS = buff_feat.SetGeometry(buff_geom)
        #���������Դ����ͼ�㣬��������Ҫ�ظ�ֵ��ͼ��
        bufferDS = bufferLayer.CreateFeature(buff_feat)



    bufferDS.Destroy()
    print("�������ļ�������ɣ�\n")






#������
if __name__ == '__main__':
    #��ȡ���̸�Ŀ¼��·��
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #print('rootPath:'+rootPath)
    #�����ļ�·��
    dataPath = os.path.abspath(rootPath + r'\ShpData')
    #print('dataPath:'+dataPath)
    #�л�Ŀ¼
    os.chdir(dataPath)
    strVectorFile =r"SpecialTown.shp"
    bufferVectorFile=r"SpecialTown_buffer.shp"
    layername='SpecialTown_buffer'
    shpBuffer(strVectorFile,bufferVectorFile,layername)