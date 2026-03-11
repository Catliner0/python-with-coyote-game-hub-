v1.10版本更新
------本次更新重构了dglab_level.py 希望能为你带来更好的体验------
不同于之前的版本 现在你可以直接通过post/posts（url，id，level）函数来直接修改强度
#level的标准格式：{“level_min”：level_min，“level：max”：level_max} 当然我更推荐你使用自带的levels（level_min，level_max）去创建level
------本次重构新增了报错检验功能 ------
posts（）为开启自动检测错误
post（）为不检测是否有错误，但你依然可以通过对其返回值value_return进行以下方式检测：
1.对level_return进行强制bool类型转化 bool（） ，若值为True，则执行成功，反之，执行出现错误。
2.使用test_error（level_return）进行更加细致的检测 ，检测结果会自动打印到终端/控制台
