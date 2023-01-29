目前這版是把整個app整包包成一個image (前後端/ML kernel都一起), image name是docker-flask-torch
requirements.txt裡面的內容是基於vscode的FlaskDocker環境直接做pip freeze, 所以最後的image超級無敵肥 (6.X GB)

注意
-1. app.py裡面最後啟動flask的時候host="0.0.0.0"是為了確保可以用localhost做訪問
-2. Dockerfile是直接把建立image當下資料夾內的所有檔案都複製到WORKDIR (可以使用指令 "docker container exec 容器名稱 ls" 確認)

===========================================
2023/01/27
把code分成frontend跟backend兩塊,並且各自包成image,同時再加上yaml啟動

要注意container啟動的時候指定的port要跟python code裡面flask的啟動port做搭配

詳細操作可以搭配notion裡面的說明筆記

