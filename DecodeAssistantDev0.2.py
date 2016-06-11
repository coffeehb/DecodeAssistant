#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 实现一个GUI版的混合解码插件
#1.已支持 Unicode
#2.已支持hex解码
#3.base64解码
#4.html解码
#5.ascii解码
#6.url解码
#7.
# 导入burp的库
from burp import IBurpExtender
from burp import IBurpExtenderCallbacks
from burp import ITab
# 导入java库
from javax import swing
from java import awt
# 导入python库
import zlib, base64, re, xml.dom.minidom, struct, binascii
import traceback

class BurpExtender(IBurpExtender, ITab):

    #
    # 实现扩展类 IBurpExtender
    #
    def	registerExtenderCallbacks(self, callbacks):
        print "Install Successful...."
        # 测试文本
        testtext = u'''
admin u'\u8fd9\u662f\u4e00\u4e2a\u6d4b\u8bd5\u9875\u9762'
root u'\u4f60\u4ee5\u4e3a\u6709\u91cd\u8981\u4fe1\u606f\u4e48\uff1f'
\u6211\u662F\u4E00\u4E2A\u7C89\u5237\u5320\uFF0C\u7C89\u5237\u672C\u9886\u5F3A\uFF0C
\u6211\u8981\u628A\u90A3\u5C0F\u623F\u5B50\uFF0C\u5237\u7684\u5F88\u6F02\u4EAE\u3002
%u6211%u662F%u4E00%u4E2A%u7C89%u5237%u5320%uFF0C%u7C89%u5237%u672C%u9886%u5F3A%uFF0C
%u6211%u8981%u628A%u90A3%u5C0F%u623F%u5B50%uFF0C%u5237%u7684%u5F88%u6F02%u4EAE%u3002
\x31\x2C\x31\x29\x3B\x75\x70\x64\x61\x74\x65\x20\x5B\x64\x76\x5F\x75\x73\x65\x72\x5D\x20\x73\x65\x74\x20\x75\x73\x65\x72\x67\x72\x6F\x75\x70\x69\x64\x3D\x31\x20\x77\x68\x65\x72\x65\x20\x75\x73\x65\x72\x69\x64\x3D\x32\x3B\x2D\x2D\x20
\x75\x73\x65\x72\x69\x64\x3D\x32\x3B\x2D\x2D\x20
0x310x2C0x310x290x3B0x750x700x640x610x740x650x200x5B0x640x760x5F0x750x730x650x720x5D0x200x730x650x740x200x750x730x650x720x670x720x6F0x750x700x690x640x3D0x310x200x770x680x650x720x650x200x750x730x650x720x690x640x3D0x320x3B0x2D0x2D0x20
0x312C31293B757064617465205B64765F757365725D20736574207573657267726F757069643D31207768657265207573657269643D323B2D2D20
 闲话不说了，base64模块真正用的上的方法只有8个，分别是encode, decode,
 ZW5jb2Rlc3RyaW5n, ZGVjb2Rlc3RyaW5n, YjY0ZW5jb2Rl,b64decode,
  dXJsc2FmZV9iNjRkZWNvZGUsdXJsc2FmZV9iNjRlbmNvZGXjgII=他们8个可以两两分为4组，
  ZW5jb2RlLGRlY29kZQ==一组，专门用来编码和 解码文件的,也可以对StringIO里的数据做编解码；
 ZW5jb2Rlc3RyaW5nLGRlY29kZXN0cmluZw==一组，专门用来编码和解码字符串；
'''
        # 保持对象的引用
        self._callbacks = callbacks
        # 获得扩展辅助对象
        self._helpers = callbacks.getHelpers()
        # 设置Extender里面显示的插件名
        callbacks.setExtensionName("DecodeAssistantDev0.2")
        # 用java的swing库创建一个标签
        self._jPanel = swing.JPanel()
        self._jPanel.setLayout(swing.BoxLayout(self._jPanel, swing.BoxLayout.Y_AXIS))
        # 文本框
        self._jTextIn = swing.JTextArea(testtext, 20, 120)
        self._jTextIn.setLineWrap(True)
        self._jScrollPaneIn = swing.JScrollPane(self._jTextIn)
        self._jScrollPaneIn.setVerticalScrollBarPolicy(swing.JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
        self._jScrollPaneIn.setPreferredSize(awt.Dimension(20, 120))
        # 定义2个按钮,编码和解码
        self._jButtonPanel = swing.JPanel()
        self._jButtonEncode = swing.JButton('Encode', actionPerformed=self.encode)
        self._jButtonDecode = swing.JButton('Decode', actionPerformed=self.decode)
        self._jButtonPanel.add(self._jButtonEncode)
        self._jButtonPanel.add(self._jButtonDecode)
        self._jPanel.add(self._jScrollPaneIn)
        self._jPanel.add(self._jButtonPanel)

        callbacks.customizeUiComponent(self._jPanel)

        # register ourselves as a message editor tab factory
        callbacks.addSuiteTab(self)
        return

    def getTabCaption(self):
        return "DecodeAssistantDev0.2"

    def getUiComponent(self):
        return self._jPanel

    def decode(self, button):
        try:
            encrypt_string = self._jTextIn.getText()
            # Unicode解码
            decrypt_string = self.decodeUnicode(encrypt_string)
            # Hex解码
            decrypt_string = self.decodeHex(decrypt_string)
            # # Base64解码
            decrypt_string = self.decodeBase64(decrypt_string)
            # # 输出到文本框

            message_info = "==="*25 + u"Encode Text" + "==="*25+"\n"
            message_info = message_info + encrypt_string + "\n"
            message_info = message_info + "===="*45+"\n"
            message_info = message_info + "==="*25 + u"Decode Text" + "==="*25+"\n"
            message_info = message_info + decrypt_string
            self._jTextIn.setText(message_info)
            # self._jTextIn.setText("Error is fuck ")
        except Exception, e:
            return

    # 输出调试日志
    def help_out(self, type, encrypt_string, decrypt_string):
        if len(decrypt_string) > 0:
            print "===="*39
            print "Encryption_String : "
            print encrypt_string.strip()
            print ""
            print "Decryption By ["+type+"]."
            print decrypt_string.strip()
            print "===="*39

    # Unicode解码
    def decodeUnicode(self, encrypt_string):
        decrypt_string = encrypt_string
        # remodle = re.compile(r'(?:\\u[\d\w]{4})+')
        remodle = re.compile(r'(?:[\\%]u\S{4})+')
        u_char_escape = remodle.findall(encrypt_string)
        # \u2211\u343d3 形式
        if len(u_char_escape) > 0:
            for item in u_char_escape:
                try:
                    itemTemp = item.replace("%", "\\")
                    u_char = (itemTemp).decode('unicode_escape').encode('utf8')
                    self.help_out(type="Unicode", encrypt_string=item, decrypt_string=u_char)
                except:
                    u_char = (item).decode('unicode_escape').encode('gbk')
                    self.help_out(type="Unicode", encrypt_string=item, decrypt_string=u_char)
                # decrypt_string = decrypt_string.replace(item, u_char)
                decrypt_string = decrypt_string.replace(item, u_char.decode("utf8"))
        return decrypt_string

    # Hex解码
    def decodeHex(self, encrypt_string):
        decrypt_string = encrypt_string
        try:
            # remodle_one = re.compile(r'(?:\\x[\d\w]{2})+')
            # 匹配四种形式的: \x22\x5B 和 0x220x5B 和 0x225B64 和 \x225B64
            remodle_one = re.compile(r'(?:[\\0]x[\S]{2,})+')
            list_hex = remodle_one.findall(decrypt_string)
            if len(list_hex) > 0:
                for item in list_hex:
                    if '0x' in item:
                        itemtemp = item.replace("0x", "")
                        u_char = binascii.a2b_hex(itemtemp)
                    else:
                        # u_char = binascii.a2b_hex(item.encode('hex'))
                        u_char = item.replace("\n", "")
                        u_char = binascii.a2b_hex(u_char.replace("\\x", "")).decode()
                    self.help_out(type="Hex", encrypt_string=item, decrypt_string=u_char)
                    decrypt_string = decrypt_string.replace(item, u_char)
        except Exception, e:
            print e
            return str(e)
        return decrypt_string

    # Base64解码
    def decodeBase64(self, encrypt_string):
        decrypt_string = encrypt_string
        try:
            # remodle_one = re.compile(r'(?:\\x[\d\w]{2})+')
            # 匹配四种形式的: \x22\x5B 和 0x220x5B 和 0x225B64 和 \x225B64
            remodle = re.compile(r'[A-Za-z0-9+/]{2,}==|[A-Za-z0-9+/]{2,}=|[A-Za-z0-9+/]{2,}')
            list_base64 = remodle.findall(decrypt_string)
            if len(list_base64) > 0:
                for item in list_base64:
                    try:
                        base64string = base64.b64decode(item)
                        is_decode_right = True
                        for temp in base64string:
                            if not (ord(temp) in range(32, 127)):
                                print "Found:"+item+" is not encode by base64."
                                is_decode_right = False
                                break
                        if is_decode_right:
                            base64string = (base64string).decode('unicode_escape').encode('utf8')
                            self.help_out(type="Base64", encrypt_string=item, decrypt_string=base64string)
                            decrypt_string = decrypt_string.replace(item, base64string)
                    except:
                        continue
            return decrypt_string
        except Exception, e:
            return str(e)

    def encode(self, button):
        body_string = self._jTextIn.getText()
        print type(body_string)
        try:
            unicode_string = body_string.decode('utf8').encode('unicode_escape')
        except:
            unicode_string = body_string.decode('gbk').encode('unicode_escape')
        print unicode_string
        print "========"
        print unicode(body_string, "utf-8")
        self._jTextIn.setText(unicode(body_string, "utf-8"))
