import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import seaborn as sns
    from matplotlib import pyplot
    return pd, sns


@app.cell
def _():
    # Constants
    SOUTH_SCOTLAND_CI = 0.0195 #  kgCO2e/kWh,  Median of mean monthly values over 2025
    CIRRUS_EMB_EMISSIONS_RATE = 0.000166 # kgCO2e/coreh
    ARCHER2_EMB_EMISSIONS_RATE = 0.0021 # kgCO2e/nodeh
    TURSA_EMB_EMISSIONS_RATE = 0.0118 # kgCO2e/GPUh
    return (
        ARCHER2_EMB_EMISSIONS_RATE,
        CIRRUS_EMB_EMISSIONS_RATE,
        SOUTH_SCOTLAND_CI,
        TURSA_EMB_EMISSIONS_RATE,
    )


@app.cell
def _(pd):
    df_cirrus = pd.read_csv('csv_data/CdTe_combined_Cirrus.csv')
    df_cirrus.head()
    return (df_cirrus,)


@app.cell
def _(df_cirrus):
    df_cirrus['Bands/s'] = df_cirrus['Bands'] / df_cirrus['LOOP+ Time']
    df_cirrus['Cores per Node'] = df_cirrus['Cores'] / df_cirrus['Nodes']
    df_cirrus['kWh'] = df_cirrus['Energy'] / 3600000.0
    df_cirrus['Bands/kWh'] = df_cirrus['Bands'] / df_cirrus['kWh']
    df_cirrus['Coreh'] = df_cirrus['Cores'] * df_cirrus['Runtime']
    df_cirrus['Nodeh'] = df_cirrus['Nodes'] * df_cirrus['Runtime']
    df_cirrus['Resource'] = df_cirrus['Nodes']
    df_cirrus['GPUs'] = 0
    df_cirrus['GPUh'] = 0.0
    return


@app.cell
def _(CIRRUS_EMB_EMISSIONS_RATE, SOUTH_SCOTLAND_CI, df_archer2, df_cirrus):
    df_cirrus['Op Emissions'] = df_cirrus['kWh'] * SOUTH_SCOTLAND_CI
    df_cirrus['Emb Emissions'] = df_cirrus['Coreh'] * CIRRUS_EMB_EMISSIONS_RATE
    df_cirrus['Emissions'] = df_cirrus['Op Emissions'] + df_cirrus['Emb Emissions']
    df_cirrus['Bands/kgCO2e'] = df_archer2['Bands'] / df_cirrus['Emissions']
    return


@app.cell
def _(pd):
    df_archer2 = pd.read_csv('csv_data/CdTe_combined_ARCHER2.csv')
    df_archer2.head()
    return (df_archer2,)


@app.cell
def _(df_archer2):
    df_archer2['Bands/s'] = df_archer2['Bands'] / df_archer2['LOOP+ Time']
    df_archer2['Cores per Node'] = df_archer2['Cores'] / df_archer2['Nodes']
    df_archer2['kWh'] = df_archer2['Energy'] / 3600000.0
    df_archer2['Bands/kWh'] = df_archer2['Bands'] / df_archer2['kWh']
    df_archer2['Coreh'] = df_archer2['Cores'] * df_archer2['Runtime']
    df_archer2['Nodeh'] = df_archer2['Nodes'] * df_archer2['Runtime']
    df_archer2['Resource'] = df_archer2['Nodes']
    df_archer2['GPUs'] = 0
    df_archer2['GPUh'] = 0.0
    return


@app.cell
def _(ARCHER2_EMB_EMISSIONS_RATE, SOUTH_SCOTLAND_CI, df_archer2):
    df_archer2['Op Emissions'] = df_archer2['kWh'] * SOUTH_SCOTLAND_CI
    df_archer2['Emb Emissions'] = df_archer2['Nodeh'] * ARCHER2_EMB_EMISSIONS_RATE
    df_archer2['Emissions'] = df_archer2['Op Emissions'] + df_archer2['Emb Emissions']
    df_archer2['Bands/kgCO2e'] = df_archer2['Bands'] / df_archer2['Emissions']
    return


@app.cell
def _(pd):
    df_tursa = pd.read_csv('csv_data/CdTe_combined_Tursa.csv')
    df_tursa.head()
    return (df_tursa,)


@app.cell
def _(df_tursa):
    df_tursa['Bands/s'] = df_tursa['Bands'] / df_tursa['LOOP+ Time']
    df_tursa['Cores per Node'] = df_tursa['Cores'] / df_tursa['Nodes']
    df_tursa['kWh'] = df_tursa['Energy'] / 3600000.0
    df_tursa['Bands/kWh'] = df_tursa['Bands'] / df_tursa['kWh']
    df_tursa['Coreh'] = df_tursa['Cores'] * df_tursa['Runtime']
    df_tursa['Nodeh'] = df_tursa['Nodes'] * df_tursa['Runtime']
    df_tursa['GPUh'] = df_tursa['GPUs'] * df_tursa['Runtime']
    df_tursa['Resource'] = df_tursa['GPUs']
    return


@app.cell
def _(SOUTH_SCOTLAND_CI, TURSA_EMB_EMISSIONS_RATE, df_tursa):
    df_tursa['Op Emissions'] = df_tursa['kWh'] * SOUTH_SCOTLAND_CI
    df_tursa['Emb Emissions'] = df_tursa['GPUh'] * TURSA_EMB_EMISSIONS_RATE
    df_tursa['Emissions'] = df_tursa['Op Emissions'] + df_tursa['Emb Emissions']
    df_tursa['Bands/kgCO2e'] = df_tursa['Bands'] / df_tursa['Emissions']
    return


@app.cell
def _(df_archer2, df_cirrus, df_tursa, pd):
    df = pd.concat([df_cirrus, df_archer2, df_tursa], ignore_index=True)
    df_single = df.loc[df['Nodes'] == 1]
    return df, df_single


@app.cell
def _(df_single, sns):
    sns.barplot(data=df_single, y='Label', x='Bands/s', hue='System')
    return


@app.cell
def _(df_single, sns):
    sns.barplot(data=df_single, y='Label', x='LOOP+ Time', hue='System')
    return


@app.cell
def _(df_single, sns):
    sns.barplot(data=df_single, y='Label', x='Bands/kWh', hue='System')
    return


@app.cell
def _(df_single, sns):
    sns.barplot(data=df_single, y='Label', x='Bands/kgCO2e', hue='System')
    return


@app.cell
def _(df, sns):
    sns.lineplot(data=df, x='Resource', y='Bands/s', hue='System', markers=True)
    return


@app.cell
def _(df, sns):
    sns.lineplot(data=df, x='Resource', y='Bands/kWh', hue='System', markers=True)
    return


@app.cell
def _(df, sns):
    sns.lineplot(data=df, x='Resource', y='Bands/kgCO2e', hue='System', markers=True)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
