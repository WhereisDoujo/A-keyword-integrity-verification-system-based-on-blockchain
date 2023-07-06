import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
from PyQt5.QtWidgets import QWidget, QApplication
from qt_material import apply_stylesheet
import client
import Encrypt_Decrypt
from PyQt5.QtGui import *
from tkinter import filedialog
import hashlib
import hmac
import random
import ast
import cryptocode
from pyDes import des, CBC, PAD_PKCS5
import binascii
def des_encrypt(s,KEY):
	while(len(KEY)%8!=0):
		KEY = KEY +'0'
	secret_key = KEY  # 密码
	iv = secret_key  # 偏移
	# secret_key:加密密钥，CBC:加密模式，iv:偏移, padmode:填充
	des_obj = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
	# 返回为字节
	secret_bytes = des_obj.encrypt(s, padmode=PAD_PKCS5)
	# 返回为16进制
	return binascii.b2a_hex(secret_bytes)

class Ui_Form(object):

	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(1400, 1000)

		self.pushButton_upload_file = QtWidgets.QPushButton(Form)#选择要上传的文件
		self.pushButton_upload_file.setGeometry(QtCore.QRect(70, 70, 150, 40))
		self.pushButton_upload_file.setObjectName("pushButton0")

		self.pushButton_upload = QtWidgets.QPushButton(Form)#上传文件
		self.pushButton_upload.setGeometry(QtCore.QRect(270, 140, 150, 40))
		self.pushButton_upload.setObjectName("pushButton1")

		self.pushButton_Search_file = QtWidgets.QPushButton(Form)#选择要下载的文件
		self.pushButton_Search_file.setGeometry(QtCore.QRect(70, 200, 150, 40))
		self.pushButton_Search_file.setObjectName("pushButton2")

		self.pushButton_download = QtWidgets.QPushButton(Form)#下载文件
		self.pushButton_download.setGeometry(QtCore.QRect(70, 260, 150, 40))
		self.pushButton_download.setObjectName("pushButton3")

		self.pushButton_vertify = QtWidgets.QPushButton(Form)#验证下载的文件
		self.pushButton_vertify.setGeometry(QtCore.QRect(470, 320, 150, 40))
		self.pushButton_vertify.setObjectName("pushButton4")

		self.pushButton_delete = QtWidgets.QPushButton(Form)#删除选择的文件
		self.pushButton_delete.setGeometry(QtCore.QRect(270, 320, 150, 40))
		self.pushButton_delete.setObjectName("pushButton5")

		self.pushButton_confirm_key = QtWidgets.QPushButton(Form)#确定密钥
		self.pushButton_confirm_key.setGeometry(QtCore.QRect(750, 910, 150, 40))
		self.pushButton_confirm_key.setObjectName("pushButton6")

		self.pushButton_show_file = QtWidgets.QPushButton(Form)#显示所有文件
		self.pushButton_show_file.setGeometry(QtCore.QRect(520, 910, 150, 40))
		self.pushButton_show_file.setObjectName("pushButton6")

		self.pushButton_coppy_text = QtWidgets.QPushButton(Form)#复制显示栏内容
		self.pushButton_coppy_text.setGeometry(QtCore.QRect(560, 360, 40, 40))
		self.pushButton_coppy_text.setObjectName("copy")
		self.pushButton_coppy_text.setStyleSheet(
			'QPushButton{border:1px solid blue}'
            'QPushButton{border-radius:20px}'
		    'QPushButton{border-image: url(img.png)}')

		self.pushButton_delete_text = QtWidgets.QPushButton(Form)#删除显示栏内容
		self.pushButton_delete_text.setGeometry(QtCore.QRect(630, 360, 40, 40))
		self.pushButton_delete_text.setObjectName("copy")
		self.pushButton_delete_text.setStyleSheet(
			'QPushButton{border:1px solid blue}'
			'QPushButton{border-radius:20px}'
			'QPushButton{border-image: url(delete.png)}')

		self.upload_file_path = QtWidgets.QLabel(Form)#显示要上传的文件路径
		self.upload_file_path.setGeometry(QtCore.QRect(270, 70, 400,40))
		self.upload_file_path.setStyleSheet("QLabel{background-color:rgb(215,215,215);}")

		self.download_file_keyword = QtWidgets.QLineEdit(Form)#根据关键词搜索要下载的文件
		self.download_file_keyword.setGeometry(QtCore.QRect(270, 200, 400,40))
		self.download_file_keyword.setStyleSheet("QLineEdit{background-color:rgb(215,215,215);}")

		self.download_file_name = QtWidgets.QComboBox(Form)  #输入要下载的文件的文件名
		self.download_file_name.setGeometry(QtCore.QRect(270, 260, 400, 40))
		self.download_file_name.setStyleSheet("QComboBox{background-color:rgb(215,215,215);}")



		self.Key_title = QtWidgets.QLabel(Form)#密钥输入栏标题
		self.Key_title.setGeometry(QtCore.QRect(850, 800, 120, 40))
		self.Key_title.setStyleSheet(
			'QLabel{background-color:rgb(230,230,230);}'
			'QLabel{font-size: 18pt;}'
			'QLabel{color:rgb(41,121,255);}'
		)

		self.Error_title = QtWidgets.QLabel(Form)#Error输入栏标题
		self.Error_title.setGeometry(QtCore.QRect(850, 420, 120, 40))
		self.Error_title.setStyleSheet(
			'QLabel{background-color:rgb(230,230,230);}'
			'QLabel{font-size: 18pt;}'
			'QLabel{color:rgb(41,121,255);}'
		)

		font = QtGui.QFont() #字体
		font.setPointSize(10)

		self.file_text = QtWidgets.QLabel(Form)#文件显示栏
		self.file_text.setFont(font)
		self.file_text.setStyleSheet("QLabel{background-color:rgb(215,215,215);}")
		self.file_text.setMinimumSize(QSize(2000,2000))
		self.file_text.setMaximumSize(QSize(2000,2000))
		self.file_text.setAlignment(Qt.AlignJustify)

		self.scrollare = QtWidgets.QScrollArea(Form)#布置滑动栏区域
		self.scrollare.setWidget(self.file_text)
		self.scrollare.setContentsMargins(0, 0, 0, 0)
		self.scrollare.verticalScrollBar().setStyleSheet(
			'QScrollBar{background-color:rgba(30,30,30,30)}'
			'QScrollBar::add-line:vertical{height: 0px;}'
			'QScrollBar::sub-line:vertical{height: 0px;}'
		)
		self.scrollare.setMinimumSize(QSize(600,500))
		self.scrollare.setMaximumSize(QSize(600,500))
		self.scrollare.setGeometry(QtCore.QRect(70, 400, 600, 500))
		self.scrollare.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

		self.key = QtWidgets.QLineEdit(Form)#密钥输入栏
		self.key.setFont(font)
		self.key.setStyleSheet("QLineEdit{background-color:rgb(215,215,215);}")
		self.key.setGeometry(QtCore.QRect(750, 850, 370, 40))

		self.error = QtWidgets.QLabel(Form)#Error报错栏
		self.error.setFont(font)
		self.error.setStyleSheet("QLabel{background-color:rgb(215,215,215);}")
		self.error.setMinimumSize(QSize(300,270))
		self.error.setMaximumSize(QSize(300,270))
		self.error.setAlignment(Qt.AlignJustify)
		self.error.setGeometry(QtCore.QRect(750, 500, 300, 270))

		self.warnning_photo = QtWidgets.QLabel(Form)#警告标识图案
		self.warnning_photo.setGeometry(QtCore.QRect(750, 400, 70, 70))
		self.warnning_photo.setStyleSheet("QLabel{border-image: url(warning.png)}")
		self.warnning_photo.setText("")

		self.key_photo = QtWidgets.QLabel(Form)#密钥标识图案
		self.key_photo.setGeometry(QtCore.QRect(750, 775, 70, 70))
		self.key_photo.setStyleSheet("QLabel{border-image: url(key.png)}")
		self.key_photo.setText("")

		self.select_model = QtWidgets.QLabel(Form)#模式选择栏
		self.select_model.setGeometry(QtCore.QRect(750, 70, 300, 300))
		self.select_model.setFont(QFont("Arial",12))
		self.select_model.setStyleSheet(
			"QLabel{background-color:rgb(215,215,215);}"
			"QLabel{color:rgb(166,166,166);}"
			"QLabel{font-size:23px;}")
		self.select_model.setAlignment(Qt.AlignJustify)

		self.rb1 = QRadioButton('ECB', self)#加密模式按钮
		self.rb2 = QRadioButton('CBC', self)
		self.rb3 = QRadioButton('CFB', self)
		self.rb4 = QRadioButton('OFB', self)
		self.rb5 = QRadioButton('CTR', self)

		self.bg1 = QtWidgets.QButtonGroup(Form)#按钮组
		self.rb1.setGeometry(QtCore.QRect(780, 130, 60, 50))
		self.rb2.setGeometry(QtCore.QRect(780, 170, 60, 50))
		self.rb3.setGeometry(QtCore.QRect(780, 210, 60, 50))
		self.rb4.setGeometry(QtCore.QRect(780, 250, 60, 50))
		self.rb5.setGeometry(QtCore.QRect(780, 290, 60, 50))
		self.bg1.addButton(self.rb1, 1)
		self.bg1.addButton(self.rb2, 2)
		self.bg1.addButton(self.rb3, 3)
		self.bg1.addButton(self.rb4, 4)
		self.bg1.addButton(self.rb5, 5)

		self.retranslateUi(Form)#垂直布局
		QtCore.QMetaObject.connectSlotsByName(Form)
	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Form"))
		self.pushButton_confirm_key.setText(_translate("Form", "Sure"))
		self.pushButton_upload_file.setText(_translate("Form", "Upload file"))
		self.pushButton_upload.setText(_translate("Form", "Upload"))
		self.pushButton_Search_file.setText(_translate("Form", "Search"))
		self.pushButton_download.setText(_translate("Form", "Download"))
		self.pushButton_vertify.setText(_translate("Form", "Vertify"))
		self.select_model.setText(_translate("Form", '''
			Model'''))
		self.Key_title.setText("Key")
		self.Error_title.setText("Error")
		self.pushButton_delete.setText("Delete")
		self.pushButton_show_file.setText("SHOW")

class MyMainForm(QMainWindow, Ui_Form):
	def find_upload_file_path(self):#寻找文件显示文件路径
		f_path = filedialog.askopenfilename()
		self.upload_file_path.setText(f_path)

	def input_key(self):
		if self.key.text() == '':
			self.error.setText("No Key")
		else:
			self.key_content=self.key.text()#获取输入的密码
			msgBox = QMessageBox()
			msgBox.setStyleSheet(
				"QLabel{"
				"min-width: 300px;"
				"min-height: 200px; "
				"font-size: 20px;"
				"}")
			msgBox.setText("密钥输入成功")
			msgBox.setWindowTitle("密钥")
			msgBox.exec_()

	def get_file_information(self):
		root = os.getcwd()
		f_name = open(root + r'\file_name.txt') #读取文件内容获取已上传的文件名和id
		f_id = open(root + r'\file_id.txt')
		self.file_name = ast.literal_eval(f_name.read())
		self.file_id = ast.literal_eval(f_id.read())
		f_name.close()
		f_id.close()

	def upload_file(self):
		file_path = self.upload_file_path.text()
		if file_path == '':
			self.error.setText("I can not find ,because you do not input file_path")
			return 0
		if len(self.key_content) == 0:
			self.error.setText("You do not input a key")
			return 0

		file = open(file_path, 'rb')
		bytes = file.read()
		bytes = Encrypt_Decrypt.PadTest(bytes)
		new_key = Encrypt_Decrypt.PadKey(self.key_content.encode())  # 将密钥转换位字节列表并补齐密钥
		model = self.bg1.checkedId()	#获取加密模式
		if model < 6 and model > 0:
			if os.path.basename(file_path) in self.file_name:
				self.error.setText("This file already exists")	#如果是已经上传的文件进行提示
			else:
				if len(self.file_name) == 0:
					file_id = 1
					self.file_id.append(str(file_id))
					self.file_name.append(str(os.path.basename(file_path)))	#将新的上传文件标题与序号记录下来
					file_ids = open(os.getcwd() + r"\file_id.txt", 'w')
					file_ids.write(str(self.file_id))
					file_names = open(os.getcwd() + r"\file_name.txt", 'w')
					file_names.write(str(self.file_name))
					file_ids.close()
					file_names.close()

				else:
					file_id = int(self.file_id[-1]) + 1	#获取新上传文件的序号
					if file_id>9999:
						file_id = 1
						while file_id in self.file_id:
							file_id+=1
						self.file_id.append(str(file_id))
						self.file_name.append(str(os.path.basename(file_path)))
						sort_list = []
						for f in range(len(self.file_id)):
							sort_list.append([int(self.file_id[f]), self.file_name[f]])
						sort_list = sorted(sort_list, key=lambda x: x[0])
						file_i = []
						file_n = []
						for l in range(len(sort_list)):
							file_i.append(str(sort_list[l][0]))
							file_n.append(sort_list[l][1])
							file_ids = open(os.getcwd() + r"\file_id.txt", 'w')  ##将新的上传文件标题与序号记录下来
							file_ids.write(str(file_i))
							file_names = open(os.getcwd() + r"\file_name.txt", 'w')
							file_names.write(str(file_n))
							file_ids.close()
							file_names.close()
					else:
						self.file_id.append(str(file_id))
						self.file_name.append(str(os.path.basename(file_path)))
						file_ids = open(os.getcwd() + r"\file_id.txt", 'w')  ##将新的上传文件标题与序号记录下来
						file_ids.write(str(self.file_id))
						file_names = open(os.getcwd() + r"\file_name.txt", 'w')
						file_names.write(str(self.file_name))
						file_ids.close()
						file_names.close()

			encrypt_file = Encrypt_Decrypt.EnCrypt(new_key, bytes, model)	#加密上传文件
			file.close()
			file = open(file_path, 'r',encoding = 'UTF-8')
			key_words = client.TF(file.read())	#获取文章关键字
			self.file_text.setText(str(key_words))
			file.close()
			new_keywords = []
			for k in range(len(key_words)):
				print(key_words[k])
				print(key_words[k].encode())
				new_keywords.append(des_encrypt(key_words[k].encode(),self.key_content))	#加密关键字
				print(156)
			print(key_words)
			print('new_key')
			print(new_keywords)
			T_w = []
			random_numbers = []
			for p in range(len(new_keywords)):
				random_number = random.randint(1, 9999999)  # 获取可搜索加密的随机数
				random_numbers.append(random_number)
				T_w.append(hmac.new(new_keywords[p],str(random_number).encode(),hashlib.md5).hexdigest())	#利用加密关键字进行可搜索加密
			try:
				file_hash_f = hashlib.sha256()  # 获取上传文件的hash值
				file_hash_f.update(encrypt_file)
				print(encrypt_file)
				file_hash = file_hash_f.hexdigest()
				print(file_hash)
				client.socket_client(file_path, encrypt_file, file_id, T_w, random_numbers)
				client.upload(file_id,file_hash)	#更新Merkle树

				msgBox = QMessageBox()
				msgBox.setStyleSheet(
					"QLabel{"
					"min-width: 300px;"
					"min-height: 200px; "
					"font-size: 20px;"
					"}")
				msgBox.setText("上传文件成功")
				msgBox.setWindowTitle("上传文件")
				msgBox.exec_()
			except:
				msgBox = QMessageBox()
				msgBox.setStyleSheet(
					"QLabel{"
					"min-width: 300px;"
					"min-height: 200px; "
					"font-size: 20px;"
					"}")
				msgBox.setText("上传文件失败")
				msgBox.setWindowTitle("上传文件")
				msgBox.exec_()
		else:
			self.error.setText('Pattern selection error')







	def search_file(self):
		self.download_file_name.clear()	#清空下拉框中上次搜索结果
		input_keyword = self.download_file_keyword.text()	#获取输入的关键字
		if input_keyword == '':
			self.error.setText("You do not input a keyword")
			return 0

		if self.bg1.checkedId()>6 or self.bg1.checkedId()<=0:
			self.error.setText('Pattern selection error')
			return 0

		if len(self.key_content) == 0:
			self.error.setText("You do not input a key")
			return 0
		file_hash_f = hashlib.sha256()  # 获取上传文件的hash值
		file_hash_f.update(('厄瓜多尔').encode())
		file_hash = file_hash_f.hexdigest()
		client.upload(random.randint(200000, 9999999), file_hash)  # 更新Merkle树

		new_keyword = des_encrypt(input_keyword.encode(),self.key_content)	#进行过关键字加密
		print(new_keyword)
		try:
			files = client.search_by_keyword(new_keyword)
			print(files)
			for i in range(len(files)):
				index = files[i][0]
				item =  files[i][1]
				self.download_file_name.addItem(str(item)+' '+str(index))	#再下来框中添加搜索到的结果
			msgBox = QMessageBox()
			msgBox.setStyleSheet(
				"QLabel{"
				"min-width: 300px;"
				"min-height: 200px; "
				"font-size: 20px;"
				"}")
			msgBox.setText("查询到相关文件%d个"%len(files))
			msgBox.setWindowTitle("查询文件")
			msgBox.exec_()
		except:
			msgBox = QMessageBox()
			msgBox.setStyleSheet(
				"QLabel{"
				"min-width: 300px;"
				"min-height: 200px; "
				"font-size: 20px;"
				"}")
			msgBox.setText("查询文件失败")
			msgBox.setWindowTitle("查询文件")
			msgBox.exec_()



	def show_files(self):
		try:
			text = ''	#清空上次显示结果
			for i in range(len(self.file_name)):
				text = text + self.file_name[i] + ' ' + self.file_id[i] + '\n'
				self.download_file_name.addItem(str(self.file_name[i]) + ' ' + str(self.file_id[i]))
			self.file_text.setText(text)
			msgBox = QMessageBox()
			msgBox.setStyleSheet(
				"QLabel{"
				"min-width: 300px;"
				"min-height: 200px; "
				"font-size: 20px;"
				"}")
			msgBox.setText("已上传文件共%d个"%len(self.file_name))
			msgBox.setWindowTitle("查询文件")
			msgBox.exec_()
		except:
			msgBox = QMessageBox()
			msgBox.setStyleSheet(
				"QLabel{"
				"min-width: 300px;"
				"min-height: 200px; "
				"font-size: 20px;"
				"}")
			msgBox.setText("查询上传文件失败")
			msgBox.setWindowTitle("查询文件")
			msgBox.exec_()


	def download_file(self):
		file_name_and_index = self.download_file_name.currentText()	#从搜索得到的下拉框中选取要下载的文件
		if file_name_and_index == '':
			self.error.setText("You do not select download file")
			return 0

		if self.bg1.checkedId() > 6 or self.bg1.checkedId() <= 0:
			self.error.setText('Pattern selection error')
			return 0

		if len(self.key_content) == 0:
			self.error.setText("You do not input a key")
			return 0
		files = file_name_and_index.split(' ')
		index = files[1]
		print(123)
		cipher= client.download_file(index)	#上传文件序号进行下载
		print('下载')
		new_key = Encrypt_Decrypt.PadKey(self.key_content.encode())
		print(5156132)
		cipher = Encrypt_Decrypt.PadTest(cipher)
		text = Encrypt_Decrypt.DeCrypt(new_key,cipher,self.bg1.checkedId())	#进行解密
		print(text)
		curr_dir = os.getcwd()
		new_file_name = self.file_name[self.file_id.index(str(index))]
		fp = open('./' + str(new_file_name), 'wb')
		fp.write(text)
		msgBox = QMessageBox()
		msgBox.setStyleSheet(
			"QLabel{"
			"min-width: 300px;"
			"min-height: 200px; "
			"font-size: 20px;"
			"}")
		msgBox.setText("下载文件成功")
		msgBox.setWindowTitle("下载文件")
		msgBox.exec_()

	def Verify_file(self):
		file_name_and_index = self.download_file_name.currentText()	#从搜索得到的下拉框中选取要验证的文件
		files = file_name_and_index.split(' ')
		file_name = files[0]
		index = files[1]
		signal=client.Verify(file_name, index)
		if signal == 1:
			print(15951)
			msgBox = QMessageBox()
			msgBox.setStyleSheet(
				"QLabel{"
				"min-width: 300px;"
				"min-height: 200px; "
				"font-size: 20px;"
				"}")
			msgBox.setText("文件校验正确")
			msgBox.setWindowTitle("校验文件")
			msgBox.exec_()
		else:
			if signal ==2:
				msgBox = QMessageBox()
				msgBox.setStyleSheet(
					"QLabel{"
					"min-width: 300px;"
					"min-height: 200px; "
					"font-size: 20px;"
					"}")
				msgBox.setText("文件校验正确服务器安全遭到威胁")
				msgBox.setWindowTitle("校验文件")
				msgBox.exec_()
			else:
				msgBox = QMessageBox()
				msgBox.setStyleSheet(
					"QLabel{"
					"min-width: 300px;"
					"min-height: 200px; "
					"font-size: 20px;"
					"}")
				msgBox.setText("文件校验错误")
				msgBox.setWindowTitle("校验文件")
				msgBox.exec_()

	def Delete_file(self):
		try:
			file_name_and_index = self.download_file_name.currentText()	#从搜索得到的下拉框中选取要删除的文件
			if file_name_and_index == '':
				self.error.setText("You do not select delete file")
				return 0
			files = file_name_and_index.split(' ')
			file_name = files[0]
			index = files[1]
			client.delete_service_file(index)	#从云端删除文件
			i = self.file_name.index(file_name)
			del self.file_name[i]
			del self.file_id[i]

			file_hash_f = hashlib.sha256()  # 获取上传文件的hash值
			file_hash_f.update(('0').encode())
			file_hash = file_hash_f.hexdigest()
			client.upload(random.randint(29999, 9999999), file_hash)  # 更新Merkle树

			curr_dir = os.getcwd()
			file_n = open(curr_dir + r'\file_name.txt','w', encoding='utf-8')	#从本地记录中删除
			file_i = open(curr_dir + r'\file_id.txt','w', encoding='utf-8')
			file_i.write(str(self.file_id))
			file_n.write(str(self.file_name))
			file_n.close()
			file_i.close()
			self.download_file_name.clear()  # 清空下拉框中上次搜索结果
			msgBox = QMessageBox()
			msgBox.setStyleSheet(
				"QLabel{"
				"min-width: 300px;"
				"min-height: 200px; "
				"font-size: 20px;"
				"}")
			msgBox.setText("文件删除成功")
			msgBox.setWindowTitle("删除文件")
			msgBox.exec_()
		except:
			msgBox = QMessageBox()
			msgBox.setStyleSheet(
				"QLabel{"
				"min-width: 300px;"
				"min-height: 200px; "
				"font-size: 20px;"
				"}")
			msgBox.setText("文件删除失败")
			msgBox.setWindowTitle("删除文件")
			msgBox.exec_()


	def delete_text(self):
		self.file_text.setText('')	#清除显示框内容

	def coppy_text(self):
		self.clipboard = QApplication.clipboard()	#复制显示框内容
		self.clipboard.setText(self.file_text.text())

	def __init__(self, parent=None):
		super(MyMainForm, self).__init__(parent)
		self.get_file_information()
		self.key_content=''
		self.setupUi(self)
		self.pushButton_upload_file.clicked.connect(self.find_upload_file_path)
		self.pushButton_confirm_key.clicked.connect(self.input_key)
		self.pushButton_upload.clicked.connect(self.upload_file)
		self.pushButton_coppy_text.clicked.connect(self.coppy_text)
		self.pushButton_delete_text.clicked.connect(self.delete_text)
		self.pushButton_delete.clicked.connect(self.Delete_file)
		self.pushButton_vertify.clicked.connect(self.Verify_file)
		self.pushButton_show_file.clicked.connect(self.show_files)
		self.pushButton_Search_file.clicked.connect(self.search_file)
		self.pushButton_download.clicked.connect(self.download_file)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	apply_stylesheet(app, theme='light_blue.xml')
	#初始化
	myWin = MyMainForm()
	#将窗口控件显示在屏幕上
	myWin.show()
	#程序运行，sys.exit方法确保程序完整退出。
	sys.exit(app.exec_())