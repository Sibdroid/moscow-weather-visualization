import pandas as pd
df = pd.read_excel(r"C:\Users\Gleb\Мои Папки\py\school_project\weather_data.xlsx", index_col = 0)
df = df.iloc[92:]
df = df.iloc[:, :-1]
df = df.iloc[:-1, :]
df.index = [str(1871 + i) for i, j in enumerate(df.index)]
df.columns = ['янв.', 'фев.', 'мар.', 'апр.', 'май.', 'июн.',
              'июл.', 'авг.', 'сен.', 'окт.', 'ноя.', 'дек.']
df.to_excel("weather_data_final.xlsx")

