# scr2txt

#### 介绍
通过截屏快速实现图片转文字，基于百度飞桨paddleocr

#### 软件架构
py3实现，基于百度飞桨paddleocr平台，主要采用
* pyqt
* pillow

#### 直接下载
* win10版本  [src2txt.zip](https://pan.baidu.com/s/1lx9-1NIwRUZfAQKvHObasA)   提取码: ui9f
* 其他系统 暂无


#### 使用说明
解压缩，运行src2txt.exe
1.  alt+c，实现截屏识别
2.  alt+q，退出


#### 安装教程

1.  安装必要依赖包
    ```
    pip install -r requirements.txt
    pip install -e packages/Shapely-1.7.1-cp37-cp37m-win_amd64.whl
    ```
2.  软件打包
    1. 调试打包
    ```
    pyinstaller -D -w --clean --exclude matplotlib -p C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddleocr;C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddle\libs scr2txt.py -i scr2txt.ico --add-binary C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddle\libs;. --add-data C:\opencode\ocr\scr2txt\model;.\model --add-data C:\opencode\ocr\scr2txt\model\scr2txt.ico;.\ --additional-hooks-dir=.
    ```
    2. 正式打包
    ```
    pyinstaller -F -w --clean --exclude matplotlib -p C:\Anaconda2\envs\paddleocr\Lib\shite-packages\paddleocr;C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddle\libs scr2txt.py -i scr2txt.ico --add-binary C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddle\libs;. --add-data C:\opencode\ocr\scr2txt\model;.\model --add-data C:\opencode\ocr\scr2txt\model\scr2txt.ico;.\ --additional-hooks-dir=.    
    ```

---------------------------------------
#### 其他注意事项
---------------------------------------

#### pyinstall 打包问题总结

* 1 找不到资源问题和matplotlib报错

matplotlib报错，通过 --exclude 屏蔽matplotlib（我的项目不用）
资源找不到，通过打包 --add-binary  --add-data 解决

```
pyinstaller -D -w --clean --exclude matplotlib -p C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddleocr;C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddle\libs textshot.py -i textshot.ico --add-binary C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddle\libs;. --add-data C:\opencode\ocr\textshot_paddle\model;.\model --additional-hooks-dir=.
```

* 2 进程无线启动问题

* 2.1 分析

经过多次排除法尝试，只要存在以下语句"from paddleocr import PaddleOCR"就会导致进程不停启动
通过命令行运行打包进程“txt.exe", 手动强杀进程（Ctrl+C）发现以下报错：

```
c:\opencode\ocr\textshot_paddle>C:\opencode\ocr\textshot_paddle\dist\txt\txt.exe
Traceback (most recent call last):
  File "txt.py", line 200, in <module>
    out, err = import_cv2_proc.communicate()
  File "subprocess.py", line 964, in communicate
  File "subprocess.py", line 1296, in _communicate
  File "threading.py", line 1044, in join
  File "threading.py", line 1060, in _wait_for_tstate_lock
KeyboardInterrupt
[448] Failed to execute script txt
```
于是查看 paddle\dataset\image.py 代码，发现200行如下
```
if six.PY3:
    import subprocess
    import sys
    import_cv2_proc = subprocess.Popen(
        [sys.executable, "-c", "import cv2"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = import_cv2_proc.communicate()
    retcode = import_cv2_proc.poll()
    if retcode != 0:
        cv2 = None
    else:
        import cv2
else:
    try:
        import cv2
    except ImportError:
        cv2 = None
```

然后根据pyinstaller issue帖子
<a href="https://github.com/pyinstaller/pyinstaller/issues/4067">4067</a>和<a href="https://github.com/pyinstaller/pyinstaller/issues/4110">4110</a>分析，怀疑subprocess.Popen导致问题
于是写测试程序，打包测试
```

import io
import os
import sys

import subprocess
import sys
import_cv2_proc = subprocess.Popen(
[sys.executable, "-c", "import cv2"],
stdout=subprocess.PIPE,
stderr=subprocess.PIPE)
out, err = import_cv2_proc.communicate()
retcode = import_cv2_proc.poll()
if retcode != 0:
    cv2 = None
else:
    import cv2
    
#from paddleocr import PaddleOCR

if __name__ == "__main__":


    print ("is ok!!!!!!!!!!!!!!!!!")
    args = input('input where you think:')
    print (args)
```
果然，重现问题，无线启动新进程。

* 2.3 解决方案
  
解决方案简单粗暴，修改image.py 39行开始代码，屏蔽subprocess调用
```
# if six.PY3:
#     import subprocess
#     import sys
#     import_cv2_proc = subprocess.Popen(
#         [sys.executable, "-c", "import cv2"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE)
#     out, err = import_cv2_proc.communicate()
#     retcode = import_cv2_proc.poll()
#     if retcode != 0:
#         cv2 = None
#     else:
#         import cv2
# else:
#     try:
#         import cv2
#     except ImportError:
#         cv2 = None
try:
    import cv2
except ImportError:
    cv2 = None
```

问题解决。

#### 如果本软件对你有用，请多多支持，这将使我有更有动力不断完善，谢谢！
<img src="imgs/donate.png" alt="alipay & wechat"/>
