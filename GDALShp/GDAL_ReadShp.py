# -*- coding: cp936 -*-


try:
    from osgeo import gdal
    from osgeo import ogr
except ImportError:
    import gdal
    import ogr

def ReadVectorFile():
    # Ϊ��֧������·�������������������
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # Ϊ��ʹ���Ա��ֶ�֧�����ģ������������䣬���ñ��뷽ʽΪGB2312
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    #SHP�ļ�·��
    strVectorFile = "D:\\tmpdata\\boundary\\ChinaProvince\\ChinaProvince.shp"
    # ע�����е�����
    ogr.RegisterAll()
    # ������
    ds = ogr.Open(strVectorFile, 0)
    #�ж��ļ��Ƿ����
    if ds == None:
        print("���ļ���%s��ʧ�ܣ�", strVectorFile)
        return
    #��ʾ�򿪳ɹ�
    print("���ļ���%s���ɹ���", strVectorFile)

    # ��ȡ������Դ�е�ͼ�������һ��shp����ͼ��ֻ��һ���������mdb��dxf��ͼ��ͻ��ж��
    iLayerCount = ds.GetLayerCount()

    # ��ȡ��һ��ͼ��
    oLayer = ds.GetLayerByIndex(0)
    if oLayer == None:
        print("��ȡ��%d��ͼ��ʧ�ܣ�\n", 0)
        return

    # ��ͼ����г�ʼ���������ͼ������˹��˲�����ִ������֮ǰ�Ĺ���ȫ�����
    oLayer.ResetReading()

    # ͨ�����Ա��SQL����ͼ���е�Ҫ�ؽ���ɸѡ���ⲿ����ϸ�ο�SQL��ѯ�½�����
    #oLayer.SetAttributeFilter("\"NAME\"LIKE \"Hubei\"")

    # ͨ��ָ���ļ��ζ����ͼ���е�Ҫ�ؽ���ɸѡ
    # oLayer.SetSpatialFilter()

    # ͨ��ָ����������Χ��ͼ���е�Ҫ�ؽ���ɸѡ
    # oLayer.SetSpatialFilterRect()

    # ��ȡͼ���е����Ա��ͷ�����
    print("���Ա�ṹ��Ϣ��")
    #ͼ�����
    oDefn = oLayer.GetLayerDefn()
    #�ֶθ���
    iFieldCount = oDefn.GetFieldCount()
    print('�ֶθ���:'+ str(iFieldCount))
    #���������ֶ�
    for iAttr in range(iFieldCount):
        #�ֶζ���
        oField = oDefn.GetFieldDefn(iAttr)
        #����ֶ���Ϣ��python�нϳ���������һ��д��������á�\�������Ӷ������
        #Python��ʽ�����%s��%d �ɲο�����https://www.cnblogs.com/linguansheng/p/10184102.html

        print("%s: %s(%d.%d)" % ( \
            #�ֶ�����
            oField.GetNameRef(), \
            #�ֶ�����
            oField.GetFieldTypeName(oField.GetType()), \
            #�ֶγ���
            oField.GetWidth(), \
            #�ֶξ���
            oField.GetPrecision()))

    # ���ͼ���е�Ҫ�ظ���
    print("Ҫ�ظ��� = %d", oLayer.GetFeatureCount(0))
    #������Ҫ�ض���
    oFeature = oLayer.GetNextFeature()
    # ���濪ʼ����ͼ���е�Ҫ��
    while oFeature is not None:
        print("��ǰ����� %d ��: \n����ֵ��", oFeature.GetFID())
        # ��ȡҪ���е����Ա�����
        for iField in range(iFieldCount):
            #�ֶζ����������Ϣ
            oFieldDefn = oDefn.GetFieldDefn(iField)
            #��������ʾ��ʽ���ֶ�����+�ֶ�����
            line = " %s (%s) = " % ( \
                #�ֶ�����
                oFieldDefn.GetNameRef(), \
                #�ֶ�����
                ogr.GetFieldTypeName(oFieldDefn.GetType()))

            #�ж�Ҫ�ص��ֶμ�
            if oFeature.IsFieldSet(iField):
                #��Ҫ������תΪ�ֶδ���ʽ
                line = line + "%s" % (oFeature.GetFieldAsString(iField))
            else:
                line = line + "(null)"

            print('line:' + line)
            #print('line:' + line.encode('gbk','ignore').decode('cp936'))
            #print('line:' + line.encode('gbk','ignore').decode('cp936'))
            #print('line:'+line.encode('UTF-8', 'ignore').decode('UTF-8'))

        # ��ȡ��һ��Ҫ��
        oFeature = oLayer.GetNextFeature()
    print("���ݼ��رգ�")

#���ò��Ժ���
ReadVectorFile()