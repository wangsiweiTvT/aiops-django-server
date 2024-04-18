from django.http import JsonResponse
import pandas as pd
from adtk.data import validate_series
from adtk.detector import SeasonalAD
from rest_framework.views import APIView
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
from pypots.imputation import SAITS
saits = SAITS(
    n_steps=48,
    n_features=37,
    n_layers=2,
    d_model=256,
    d_ffn=128,
    n_heads=4,
    d_k=64,
    d_v=64,
    dropout=0.1,
    epochs=10,
    # saving_path="examples/saits", # set the path for saving tensorboard logging file and model checkpoint
    # model_saving_strategy="best", # only save the model with the best validation performance
)
saits.load(str(BASE_DIR) + "/static/SAITS.pypots")
class Detector(APIView):
    def get(self,request):
        # 读取 CSV 文件
        file_path = request.GET.get('file_path')
        print(file_path)
        df = pd.read_csv(str(BASE_DIR) + "/static/" + file_path)

        # 获取特征列名
        feature_column = "17"

        # 跳过非数值列
        if df[feature_column].dtype not in ['int64', 'float64']:
            raise ValueError(f"Column '{feature_column}' is not numeric.")

        # 获取当前特征列的数据
        feature_series = df[feature_column]

        # 使用线性插值法处理缺失值
        feature_series_int = feature_series.interpolate()

        # 创建一个简单的时间索引
        time_index = pd.date_range(start="2024-01-01", periods=len(feature_series_int), freq="D")

        # 使用 adtk 进行数据验证
        feature_series_int = validate_series(pd.Series(data=feature_series_int.values, index=time_index))

        # 使用 SeasonalAD 进行季节性异常检测
        detector = SeasonalAD(freq=None, side='both', c=4.5, trend=False)  # 使用默认设置进行自动检测
        anomalies = detector.fit_detect(feature_series_int)

        x=list()
        y=list()
        mark_points=list()

        result_list = list()
        for index, row in feature_series_int.iteritems():
            x.append(str(index))

            if anomalies[index]:
                y.append({
                    "value":row,
                    "itemStyle":{ "color": "red" },
                    "symbolSize":"5"
                })
                mark_points.append({"name": '异常点'+str(len(mark_points)),"color":"green", "value": row, "xAxis": str(index), "yAxis": row})
            else:y.append(row)
            # result_itm = {
            #     "time": str(index),
            #     "is_error": bool(anomalies[index]),
            #     "value": row
            # }
            # result_list.append(result_itm)

        return JsonResponse({"x":x,"y":y,"mark_points":mark_points})


class Impute(APIView):
    def get(self,request):
        return JsonResponse({})
