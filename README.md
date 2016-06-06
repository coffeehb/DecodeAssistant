# DecodeAssistant
DecodeAssistant  中文名: 解码助手 
不知道你是不是也我一样，期望有一款工具可以自动识别文本中各种字符串的编码类型，然后给出解码后的字符串。

既然上天给了我们双手，哪么为何不自己造一款呢？？？

本工具为代理工具BurpSuite的插件，如果你有兴趣或建议欢迎提出！
开发与测试环境：
   1、 Python2.7.8
   2、Jython2.5.3
   3、BurpSuite Pro 1.6.27
   4、JDK 1.7.013
   5、PyCharm
期望实现：
   1、识别Unicode编码，支持\u8fd9\u662f 、%u6211%u662F 两种形式解码.
   2、识别Hex编码，支持\x22\x5B 、 0x220x5B 、 0x225B64 、\x225B64四种形式解码.
   3、识别Base64编码，支持ZW5jb2RlLGRlY29kZQ==形式编码
   4、识别URL编码
   5、识别HTML编码
   6、识别Char()形式编码
   7、再补充

开发日志：
<一> 2016.06.06 初始化项目
    1. 实现Unicode识别和解码
    2. 实现Hex的识别和解码
	  3. 正在实现Base64支持部分
	
	
