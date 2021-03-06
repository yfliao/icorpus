
from 文章.models import 何澤政文章
from 臺灣言語工具.斷詞.中研院工具.官方斷詞剖析工具 import 官方斷詞剖析工具
from 臺灣言語工具.斷詞.中研院工具.斷詞結構化工具 import 斷詞結構化工具
from 臺灣言語工具.字詞組集句章.解析整理.物件譀鏡 import 物件譀鏡
import time
from 文章.文章整理 import 文章整理

'''
使用方法
python3 manage.py shell
from 文章.產生翻譯用平行語料 import 產生翻譯用平行語料
產生翻譯用平行語料()
'''

class 產生翻譯用平行語料():
	__斷詞工具 = 官方斷詞剖析工具()
	__斷詞結構化 = 斷詞結構化工具()
	__譀鏡 = 物件譀鏡()
	__文章整理 = 文章整理()
	def __init__(self,
				國語斷詞組檔名='臺華.國語斷詞組.txt', 國語斷詞檔名='臺華.國語斷詞.txt',
				教羅檔名='臺華.教羅檔案.txt'):
		國語斷詞組檔案 = open(國語斷詞組檔名, 'w')
		國語斷詞檔案 = open(國語斷詞檔名, 'w')
		教羅檔案 = open(教羅檔名, 'w')
		for 文章 in 何澤政文章.objects.order_by('pk'):
			國語 = 文章.斷詞標題 + '\n' + 文章.斷詞內容
			教羅 = 文章.教羅標題 + '\n' + 文章.教羅內容
			國語 = 國語.strip()
			教羅 = 教羅.strip()
			文章國語 = self.__文章整理.轉語句陣列空白(國語.split('\n'))
			文章音標 = self.__文章整理.轉語句陣列空白(教羅.split('\n'))
			if len(文章國語) != len(文章音標):
				print('國語佮音標對無齊：{0}'.format(文章.pk))
				continue
			for 一逝國語, 一逝音標 in zip(文章國語, 文章音標):
				愛斷詞 = True
				while 愛斷詞:
					try:
						斷詞結果 = self.__斷詞工具.斷詞(一逝國語)
						愛斷詞 = False
					except Exception as 問題:
						print('「{}」出現「{}」'
							.format(一逝國語, 問題))
						time.sleep(10)
				if len(斷詞結果) != 1:
					raise RuntimeError("斷詞怪怪")
				章物件 = self.__斷詞結構化.斷詞轉章物件(斷詞結果)
				斷詞結果 = self.__譀鏡.看型(章物件, 物件分詞符號=' ')
				print(斷詞結果, file=國語斷詞檔案)
				if len(一逝國語.split()) >= len(一逝音標.split()) / 2:
					print(一逝國語, file=國語斷詞組檔案)
				else:
					print(斷詞結果, file=國語斷詞組檔案)
			print(self.__文章整理.轉文章空白(教羅), file=教羅檔案)


if __name__ == '__main__':
	產生翻譯用平行語料()
