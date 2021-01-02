@echo package start...

pyinstaller -F -w --clean --exclude matplotlib -p C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddleocr;C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddle\libs scr2txt.py -i scr2txt.ico --add-binary C:\Anaconda2\envs\paddleocr\Lib\site-packages\paddle\libs;. --add-data C:\opencode\ocr\scr2txt\model;.\model --add-data C:\opencode\ocr\scr2txt\model\scr2txt.ico;.\ --additional-hooks-dir=.

@echo package ok!!