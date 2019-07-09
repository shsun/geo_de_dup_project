# geo_de_dup_project

## 目录结构
### main.py
### app
* GEODistanceStrategy.py 
计算两个经纬度之间的距离,小于 200 米则认为是同一个地址
* LALPctStrategy.py 
通过对经纬度的比较，相差百分之一或更小以内的视为同一地址，否则视为两个地址，将地址重复的去掉。
生成出地址库。当新地址收录时，通过正向地址编码到高德或百度得到经纬度再与已有经纬度进行匹配比较
* StringDiffStrategy.py 
判断'详细地址（拼接省市区）'的相似度, 大于等于 0.8,则认为是同一个地址
* Address.py
* XUtils.py 
读写excel
### resources
* receiving_address_input_1.xlsx 
原始的地址信息excel
* receiving_address_output_1.xlsx 
去重后生成的地址信息excel
### doc
* algorithm.docx 
算法文档