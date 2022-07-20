import pandas as pd
df = pd.read_csv("../../../treering/OpenData/detrend v0.1.1 a.csv")
df.rename(columns= {'res.Lbai.normalized': 'growth_index'}, inplace=True)
df.drop(["uid_tree", "uid_radius", "SummerSMI", "SummerSMI.t_1","Ecoregions"], axis=1, inplace=True)
df = df.groupby(['species', 'year'], as_index=False)['growth_index'].mean()
df = df.pivot(index='species', columns='year', values='growth_index')
#df = df.set_index("species")
df.columns = df.columns.astype(str)

species = ['PICEGLA','ABIEBAL']
data = df.loc[species]
data = data.T.reset_index()
data = pd.melt(data, id_vars=["year"]).rename(columns={"index": "year", "value": "growth_index"})

print(data)

AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
df = df.set_index("Region")

countries = ["China", "United States of America"]
data = df.loc[countries]
data /= 1000000.0
data = data.T.reset_index()
data = pd.melt(data, id_vars=["index"]).rename(columns={"index": "year", "value": "Gross Agricultural Product ($B)"})

print(data)
