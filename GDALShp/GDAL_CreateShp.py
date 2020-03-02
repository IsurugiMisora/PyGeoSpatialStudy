#-*- coding: cp936 -*-
try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import gdal
    import ogr

def WriteVectorFile():
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING","GB2312")

    strVectorFile ="D:\\GitHub\PyGdalStudy\\GDALShp\\Data\\TestPolygon.shp"

    # 注册所有的驱动
    ogr.RegisterAll()

    # 创建数据，这里以创建ESRI的shp文件为例
    strDriverName = "ESRI Shapefile"
    oDriver =ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("%s 驱动不可用！\n", strDriverName)
        return

    # 创建数据源
    oDS =oDriver.CreateDataSource(strVectorFile)
    if oDS == None:
        print("创建文件【%s】失败！", strVectorFile)
        return

    #定义投影
    targetSR = osr.SpatialReference()
    targetSR.ImportFromEPSG(4326) #Geo WGS84
    # 创建图层，创建一个多边形图层，这里没有指定空间参考，如果需要的话，需要在这里进行指定
    papszLCO = []
    oLayer =oDS.CreateLayer("TestPolygon", targetSR, ogr.wkbPolygon, papszLCO)
    if oLayer == None:
        print("图层创建失败！\n")
        return

    # 下面创建属性表
    # 先创建一个叫FieldID的整型属性
    oFieldID =ogr.FieldDefn("FieldID", ogr.OFTInteger)
    oLayer.CreateField(oFieldID, 1)

    # 再创建一个叫FeatureName的字符型属性，字符长度为100
    oFieldName =ogr.FieldDefn("FieldName", ogr.OFTString)
    oFieldName.SetWidth(100)
    oLayer.CreateField(oFieldName, 1)

    oDefn = oLayer.GetLayerDefn()

    # 创建三角形要素
    oFeatureTriangle = ogr.Feature(oDefn)
    oFeatureTriangle.SetField(0, 0)
    oFeatureTriangle.SetField(1, "三角形")
    geomTriangle =ogr.CreateGeometryFromWkt("POLYGON ((0 0,20 0,10 15,0 0))")
    oFeatureTriangle.SetGeometry(geomTriangle)
    oLayer.CreateFeature(oFeatureTriangle)

    # 创建矩形要素
    oFeatureRectangle = ogr.Feature(oDefn)
    oFeatureRectangle.SetField(0, 1)
    oFeatureRectangle.SetField(1, "矩形")
    geomRectangle =ogr.CreateGeometryFromWkt("POLYGON ((30 0,60 0,60 30,30 30,30 0))")
    oFeatureRectangle.SetGeometry(geomRectangle)
    oLayer.CreateFeature(oFeatureRectangle)

    # 创建点要素
    # oFeaturePoint = ogr.Feature(oDefn)
    # oFeaturePoint.SetField(0, 2)
    # oFeaturePoint.SetField(1, "点")
    # #geomPoint =ogr.CreateGeometryFromWkt("Point(10,20)")
    # geomPoint = ogr.Geometry(ogr.wkbPoint)
    # geomPoint.AddPoint(10,20)
    # oFeaturePoint.SetGeometry(geomPoint)
    # oLayer.CreateFeature(oFeaturePoint)

    oDS.Destroy()
    print("数据集创建完成！\n")

#测试
WriteVectorFile()