import numpy as np
import pandas as pd


def get_series_from_data(data, data_key_list,interpolate=True,lightweighting=10):
    try:
        # select the first injection as the injection timestamp
        inject_timestamp = data["Injection"]["data"][-1][0]
    except KeyError:
        inject_timestamp = 0

    data_series_list = []
    for data_key in data_key_list:
        data_array = np.array(data[data_key]["data"])#.astype(float)
        data_series = pd.Series(data=data_array[:, 1], index=data_array[:, 0].astype(float))
        # remove duplicates
        data_series = data_series[~data_series.index.duplicated()]
        # offset by the infection_timestamp

        data_series.index -= inject_timestamp

        data_series_list.append(data_series)

    df = pd.concat(data_series_list, axis=1)
    df.columns = data_key_list

    df = df.sort_index()
    df = df.reset_index(names=["mL"])

    if interpolate:
      df = df.interpolate(method='linear')

    if lightweighting:
      light_index = np.array(df.index[df.index%10==0])

      # オブジェクトタイプの列を選択
      object_columns = df.select_dtypes(include=['object']).columns

      # 全てのオブジェクト列でNaNでないインデックスを取得し、1つのリストにまとめる
      non_nan_indices = sorted(set(df[object_columns].dropna(how="all").index))

      light_index = np.append(light_index,non_nan_indices)
      light_index = sorted(set(light_index))
      
      df = df.loc[light_index]
      df = df.reset_index(drop=True)




    return df