# -*- coding: utf-8 -*-
"""
Spyder Editor

2015-12-6
[iMatch screen print script ]
# To Generate the screen printed jpg and
save the diary page

#
written by  github  @yondjune

"""
import time
from datetime import datetime
i = time.strftime('%Y-%m-%d %H-%M-%S')
print str(i)
# show diary file name

import ImageGrab
img = ImageGrab.grab()
img.show()
img.save(i+".jpg")

# img.save(i+".jpg") - save to default path / directory
# If assign to another path 
# img.save('H:/005.jpg','JPEG') why I failed ???


 