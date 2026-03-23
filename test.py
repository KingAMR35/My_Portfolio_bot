import pyqrcode

big_code = pyqrcode.create('https://www.youtube.com/watch?v=9L4DQhq_mkM&t=4510s')
big_code.png('code.png', scale=6, module_color=[0, 0, 0, 128])
big_code.show()