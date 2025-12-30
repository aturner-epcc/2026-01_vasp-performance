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
    )


@app.cell
def _(pd):
    df_cirrus = pd.read_csv('csv_data/CdTe_combined_Cirrus.csv')
    df_cirrus.head()
    return (df_cirrus,)


@app.cell
def _(df_cirrus):
    df_cirrus['LOOP+ per Band'] = df_cirrus['LOOP+ Time'] / df_cirrus['Bands']
    df_cirrus['Performance'] = 1 / df_cirrus['LOOP+ per Band']
    df_cirrus['Cores per Node'] = df_cirrus['Cores'] / df_cirrus['Nodes']
    df_cirrus['kWh'] = df_cirrus['Energy'] / 3600000.0
    df_cirrus['kWh Performance'] = df_cirrus['kWh'] / df_cirrus['LOOP+ per Band']
    df_cirrus['Coreh'] = df_cirrus['Cores'] * df_cirrus['Runtime']
    df_cirrus['Nodeh'] = df_cirrus['Nodes'] * df_cirrus['Runtime']
    df_cirrus['GPUh'] = 0.0
    return


@app.cell
def _(CIRRUS_EMB_EMISSIONS_RATE, SOUTH_SCOTLAND_CI, df_cirrus):
    df_cirrus['Op Emissions'] = df_cirrus['kWh'] * SOUTH_SCOTLAND_CI
    df_cirrus['Emb Emissions'] = df_cirrus['Coreh'] * CIRRUS_EMB_EMISSIONS_RATE
    df_cirrus['Emissions'] = df_cirrus['Op Emissions'] + df_cirrus['Emb Emissions']
    df_cirrus['Emissions Performance'] = df_cirrus['Emissions'] / df_cirrus['LOOP+ per Band']
    return


@app.cell
def _(pd):
    df_archer2 = pd.read_csv('csv_data/CdTe_combined_ARCHER2.csv')
    df_archer2.head()
    return (df_archer2,)


@app.cell
def _(df_archer2):
    df_archer2['LOOP+ per Band'] = df_archer2['LOOP+ Time'] / df_archer2['Bands']
    df_archer2['Performance'] = 1 / df_archer2['LOOP+ per Band']
    df_archer2['Cores per Node'] = df_archer2['Cores'] / df_archer2['Nodes']
    df_archer2['kWh'] = df_archer2['Energy'] / 3600000.0
    df_archer2['kWh Performance'] = df_archer2['kWh'] / df_archer2['LOOP+ per Band']
    df_archer2['Coreh'] = df_archer2['Cores'] * df_archer2['Runtime']
    df_archer2['Nodeh'] = df_archer2['Nodes'] * df_archer2['Runtime']
    df_archer2['GPUh'] = 0.0
    return


@app.cell
def _(ARCHER2_EMB_EMISSIONS_RATE, SOUTH_SCOTLAND_CI, df_archer2):
    df_archer2['Op Emissions'] = df_archer2['kWh'] * SOUTH_SCOTLAND_CI
    df_archer2['Emb Emissions'] = df_archer2['Nodeh'] * ARCHER2_EMB_EMISSIONS_RATE
    df_archer2['Emissions'] = df_archer2['Op Emissions'] + df_archer2['Emb Emissions']
    df_archer2['Emissions Performance'] = df_archer2['Emissions'] / df_archer2['LOOP+ per Band']
    return


@app.cell
def _(df_archer2, df_cirrus, pd):
    df = pd.concat([df_cirrus, df_archer2], ignore_index=True)
    return (df,)


@app.cell
def _(df):
    df_mpi = df.loc[df['Threads'] == 1]
    df_full = df_mpi.loc[(df_mpi['Cores per Node'] == 288) | (df_mpi['Cores per Node'] == 128) ]
    df_single = df_mpi.loc[df_mpi['Nodes'] == 1]
    return df_full, df_single


@app.cell
def _(df_full, sns):
    sns.lineplot(data=df_full, x='Cores', y='Performance', hue='System', markers=True)
    return


@app.cell
def _(df_full, sns):
    sns.lineplot(data=df_full, x='Nodes', y='Performance', hue='System', markers=True)
    return


@app.cell
def _(df_full, sns):
    sns.barplot(data=df_full, x='Cores', y='Performance', hue='System')
    return


@app.cell
def _(df_full, sns):
    sns.lineplot(data=df_full, x='Nodes', y='kWh Performance', hue='System', markers=True)
    return


@app.cell
def _(df_full, sns):
    sns.lineplot(data=df_full, x='Nodes', y='Emissions Performance', hue='System')
    return


@app.cell
def _(df_full, sns):
    sns.lineplot(data=df_full, x='Nodes', y='Emb Emissions', hue='System')
    return


@app.cell
def _(df_single, sns):
    sns.barplot(data=df_single, x='Cores per Node', y='Performance', hue='System')
    return


@app.cell
def _(df_single, sns):
    sns.lineplot(data=df_single, x='Cores', y='Emb Emissions', hue='System')
    return


@app.cell
def _(df_single, sns):
    sns.lineplot(data=df_single, x='Cores', y='Performance', hue='System')
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
