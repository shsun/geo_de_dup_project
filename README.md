# geo_de_dup_project

## 目录结构
### main.py
### app
* GEODistanceStrategy.py 计算两个经纬度之间的距离,小于 200 米则认为是同一个地址
* LALPctStrategy.py 通过对经纬度的比较，相差百分之一或更小以内的视为同一地址，否则视为两个地址
* StringDiffStrategy.py 判断'详细地址（拼接省市区）'的相似度, 大于等于 0.8,则认为是同一个地址
* Address.py
* XUtils.py 
读写excel
### resources
* receiving_address_input_1.xlsx 表1地址信息excel
* receiving_address_increment_1.xlsx 增量地址信息excel
* receiving_address_group_by_1.xls 根据表1地址信息excel生成的表2
* receiving_address_group_by_2.xls 根据(表1地址信息excel+增量地址信息excel)生成的表2
* receiving_address_filtered_1.xls 根据表1地址信息excel生成的表3
* receiving_address_filtered_2.xls 根据(表1地址信息excel+增量地址信息excel)生成的表3
### doc
* algorithm.docx 
算法文档

### ps w2g49m