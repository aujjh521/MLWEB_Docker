#初始化flask伺服器
from flask import *

#為了inference
import urllib.request
from kernels.DogCatClassification.inference import *

#建Flask 的application物件, 可以設定靜態檔案的路徑處理
app = Flask(__name__,
            static_folder = 'public', #放置靜態檔案的資料夾名稱
            static_url_path = '/' #靜態檔案對應的網址路徑 (只給/就是網址裡面路徑/後面直接接上public資料夾內的檔案名稱就會吃到靜態檔案)
) 

#處裡貓狗分類執行預測的路由
@app.route("/DogCatClassification_predict",  methods=["POST", "GET"])
def DogCatClassification_predict():

    #save image to local folder
    try:
        img_url = request.form["imgurl"]
        # img_url = request.args.get("imgurl", "") #搭配get method處理

        app.logger.debug('get img from url success')
        local_path = "./public/download/" + "local-filename.jpg"
        urllib.request.urlretrieve(img_url, local_path)
        app.logger.debug(f'save image to local folder')


    except Exception as e:
        app.logger.debug(e)
        # return redirect("/GetImgFail?msg=該圖片無法被下載,請更換其他圖片網址")
        return e

    #load ML model
    model = CNN()
    model.load_state_dict(torch.load(pretrained_weight_path,map_location=torch.device("cpu")))

    #%%
    #inference
    test_transform = transforms.Compose([transforms.Resize((128, 128)),
                        transforms.ToTensor()
                        ])

    img = Image.open(local_path)
    img = test_transform(img).unsqueeze(0) #增加一個維度for batch
    res = model(img)

    #把predict結果mapping回初始類別
    _, pred = torch.max(res, dim=1)
    label_encode_mapping = {1:'dog',
                0:'cat'
                }
    
    return render_template('DogCatClassification_result.html',
                            #member_nickname = session["nickname"],
                            predicted_label = label_encode_mapping[pred.numpy()[0]],
                            target_image = "/download/"+"local-filename.jpg")




if __name__ == "__main__":
    #啟動伺服器, 可透過參數port修改port的設定,預設是5000
    app.run(host="0.0.0.0", port=5678) 