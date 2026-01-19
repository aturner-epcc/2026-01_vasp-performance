import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import seaborn as sns
    from matplotlib import pyplot
    return pd, pyplot, sns


@app.cell
def _(sns):
    # Constants
    SOUTH_SCOTLAND_CI = 0.0195 #  kgCO2e/kWh,  Median of mean monthly values over 2025
    SW_ENGLAND_CI = 0.218 #  kgCO2e/kWh,  Median of mean monthly values over 2025
    E_ENGLAND_CI = 0.1285 #  kgCO2e/kWh,  Median of mean monthly values over 2025
    NW_ENGLAND_CI = 0.054 #  kgCO2e/kWh,  Median of mean monthly values over 2025

    PUE = 1.1

    CIRRUS_EMB_EMISSIONS_RATE = 0.000166 # kgCO2e/coreh
    CIRRUS_CORES_PER_NODE = 288
    CIRRUS_FP64_NODE = 34.10 # TFLOP per node
    CIRRUS_POWER_OVERHEAD = 1.11

    ARCHER2_EMB_EMISSIONS_RATE = 0.0021 # kgCO2e/nodeh
    ARCHER2_CORES_PER_NODE = 128
    ARCHER2_FP64_NODE = 6.96 # TFLOP per node
    ARCHER2_POWER_OVERHEAD = 1.11

    TURSA_EMB_EMISSIONS_RATE = 0.0118 # kgCO2e/GPUh
    TURSA_CORES_PER_NODE = 32
    TURSA_FP64_GPU = 9.7 # TFLOP per GPU
    TURSA_POWER_OVERHEAD = 1.08

    RC_CUSTOM_PARAMS = {'axes.spines.right': False, 'axes.spines.top': False, 'figure.figsize':(6,6)}
    sns.set_theme(rc=RC_CUSTOM_PARAMS, style="ticks")
    return (
        ARCHER2_CORES_PER_NODE,
        ARCHER2_EMB_EMISSIONS_RATE,
        ARCHER2_FP64_NODE,
        ARCHER2_POWER_OVERHEAD,
        CIRRUS_CORES_PER_NODE,
        CIRRUS_EMB_EMISSIONS_RATE,
        CIRRUS_FP64_NODE,
        CIRRUS_POWER_OVERHEAD,
        E_ENGLAND_CI,
        NW_ENGLAND_CI,
        PUE,
        SOUTH_SCOTLAND_CI,
        SW_ENGLAND_CI,
        TURSA_CORES_PER_NODE,
        TURSA_EMB_EMISSIONS_RATE,
        TURSA_FP64_GPU,
        TURSA_POWER_OVERHEAD,
    )


@app.cell
def _(pd):
    df_cirrus = pd.read_csv('csv_data/TiO2_combined_Cirrus.csv')
    df_cirrus
    return (df_cirrus,)


@app.cell
def _(CIRRUS_CORES_PER_NODE, CIRRUS_FP64_NODE, df, df_cirrus):
    # Horrible fix for case where VASP output does not print high MPI process counts correctly
    df_cirrus.loc[(df_cirrus['Processes'] == 1) & (df['Nodes'] == 64), 'Cores'] = 64 * 288
    df_cirrus.loc[(df_cirrus['Processes'] == 1) & (df['Nodes'] == 64), 'Processes'] = 64 * 288

    df_cirrus['Bands/s'] = df_cirrus['Bands'] / df_cirrus['Runtime']
    df_cirrus['Reserved Cores'] = df_cirrus['Nodes'] * CIRRUS_CORES_PER_NODE
    df_cirrus['Bands/core'] = df_cirrus['Bands'] / df_cirrus['Cores']
    df_cirrus['Bands/GPU'] = 0.0
    df_cirrus['Cores per Node'] = df_cirrus['Cores'] / df_cirrus['Nodes']
    df_cirrus['kWh'] = df_cirrus['Energy'] / 3600000.0
    df_cirrus['Bands/kWh'] = df_cirrus['Bands'] / df_cirrus['kWh']
    df_cirrus['Coreh'] = (df_cirrus['Cores'] * df_cirrus['Runtime']) / 3600.0
    df_cirrus['Nodeh'] = (df_cirrus['Nodes'] * df_cirrus['Runtime']) / 3600.0
    df_cirrus['Resource'] = df_cirrus['Nodes']
    df_cirrus['Peak FP64 Flops'] = df_cirrus['Nodes'] * CIRRUS_FP64_NODE
    df_cirrus['GPUs'] = 0
    df_cirrus['GPUh'] = 0.0
    return


@app.cell
def _(
    CIRRUS_EMB_EMISSIONS_RATE,
    CIRRUS_POWER_OVERHEAD,
    E_ENGLAND_CI,
    NW_ENGLAND_CI,
    PUE,
    SOUTH_SCOTLAND_CI,
    SW_ENGLAND_CI,
    df_cirrus,
):
    df_cirrus['Emb Emissions'] = df_cirrus['Coreh'] * CIRRUS_EMB_EMISSIONS_RATE
    df_cirrus['Emissions (S Scotland)'] = df_cirrus['Emb Emissions'] + (df_cirrus['kWh'] * CIRRUS_POWER_OVERHEAD * PUE * SOUTH_SCOTLAND_CI)
    df_cirrus['Emissions (NW England)'] = df_cirrus['Emb Emissions'] + (df_cirrus['kWh'] * CIRRUS_POWER_OVERHEAD * PUE * NW_ENGLAND_CI)
    df_cirrus['Emissions (E England)'] = df_cirrus['Emb Emissions'] + (df_cirrus['kWh'] * CIRRUS_POWER_OVERHEAD * PUE * E_ENGLAND_CI)
    df_cirrus['Emissions (SW England)'] = df_cirrus['Emb Emissions'] + (df_cirrus['kWh'] * CIRRUS_POWER_OVERHEAD * PUE * SW_ENGLAND_CI)
    df_cirrus['Bands/kgCO2e (S Scotland)'] = df_cirrus['Bands'] / df_cirrus['Emissions (S Scotland)']
    df_cirrus['Bands/kgCO2e (NW England)'] = df_cirrus['Bands'] / df_cirrus['Emissions (NW England)']
    df_cirrus['Bands/kgCO2e (E England)'] = df_cirrus['Bands'] / df_cirrus['Emissions (E England)']
    df_cirrus['Bands/kgCO2e (SW England)'] = df_cirrus['Bands'] / df_cirrus['Emissions (SW England)']
    return


@app.cell
def _(df_cirrus):
    df_cirrus
    return


@app.cell
def _(df_cirrus):
    df_cirrus_single = df_cirrus.loc[df_cirrus['Nodes'] == 1]
    return (df_cirrus_single,)


@app.cell
def _(pd):
    df_archer2 = pd.read_csv('csv_data/TiO2_combined_ARCHER2.csv')
    df_archer2.head()
    return (df_archer2,)


@app.cell
def _(df_archer2):
    df_archer2
    return


@app.cell
def _(ARCHER2_CORES_PER_NODE, ARCHER2_FP64_NODE, df_archer2):
    df_archer2['Bands/s'] = df_archer2['Bands'] / df_archer2['Runtime']
    df_archer2['Reserved Cores'] = df_archer2['Nodes'] * ARCHER2_CORES_PER_NODE
    df_archer2['Bands/core'] = df_archer2['Bands'] / df_archer2['Cores']
    df_archer2['Bands/GPU'] = 0.0
    df_archer2['Cores per Node'] = df_archer2['Cores'] / df_archer2['Nodes']
    df_archer2['kWh'] = df_archer2['Energy'] / 3600000.0
    df_archer2['Bands/kWh'] = df_archer2['Bands'] / df_archer2['kWh']
    df_archer2['Coreh'] = (df_archer2['Cores'] * df_archer2['Runtime']) / 3600.0
    df_archer2['Nodeh'] = (df_archer2['Nodes'] * df_archer2['Runtime']) / 3600.0
    df_archer2['Resource'] = df_archer2['Nodes']
    df_archer2['Peak FP64 Flops'] = df_archer2['Nodes'] * ARCHER2_FP64_NODE
    df_archer2['GPUs'] = 0
    df_archer2['GPUh'] = 0.0
    return


@app.cell
def _(
    ARCHER2_EMB_EMISSIONS_RATE,
    ARCHER2_POWER_OVERHEAD,
    E_ENGLAND_CI,
    NW_ENGLAND_CI,
    PUE,
    SOUTH_SCOTLAND_CI,
    SW_ENGLAND_CI,
    df_archer2,
):
    df_archer2['Emb Emissions'] = df_archer2['Nodeh'] * ARCHER2_EMB_EMISSIONS_RATE
    df_archer2['Emissions (S Scotland)'] = df_archer2['Emb Emissions'] + (df_archer2['kWh'] * ARCHER2_POWER_OVERHEAD * PUE * SOUTH_SCOTLAND_CI)
    df_archer2['Emissions (NW England)'] = df_archer2['Emb Emissions'] + (df_archer2['kWh'] * ARCHER2_POWER_OVERHEAD * PUE * NW_ENGLAND_CI)
    df_archer2['Emissions (E England)'] = df_archer2['Emb Emissions'] + (df_archer2['kWh'] * ARCHER2_POWER_OVERHEAD * PUE * E_ENGLAND_CI)
    df_archer2['Emissions (SW England)'] = df_archer2['Emb Emissions'] + (df_archer2['kWh'] * ARCHER2_POWER_OVERHEAD * PUE * SW_ENGLAND_CI)
    df_archer2['Bands/kgCO2e (S Scotland)'] = df_archer2['Bands'] / df_archer2['Emissions (S Scotland)']
    df_archer2['Bands/kgCO2e (NW England)'] = df_archer2['Bands'] / df_archer2['Emissions (NW England)']
    df_archer2['Bands/kgCO2e (E England)'] = df_archer2['Bands'] / df_archer2['Emissions (E England)']
    df_archer2['Bands/kgCO2e (SW England)'] = df_archer2['Bands'] / df_archer2['Emissions (SW England)']
    return


@app.cell
def _(df_archer2):
    df_archer2_single = df_archer2.loc[df_archer2['Nodes'] == 1]
    return (df_archer2_single,)


@app.cell
def _(pd):
    df_tursa = pd.read_csv('csv_data/TiO2_combined_Tursa.csv')
    df_tursa.head()
    return (df_tursa,)


@app.cell
def _(TURSA_CORES_PER_NODE, TURSA_FP64_GPU, df_tursa):
    df_tursa['Bands/s'] = df_tursa['Bands'] / df_tursa['Runtime']
    df_tursa['Reserved Cores'] = df_tursa['Nodes'] * TURSA_CORES_PER_NODE
    df_tursa['Bands/core'] = 0.0
    df_tursa['Bands/GPU'] = df_tursa['Bands'] / df_tursa['GPUs']
    df_tursa['Cores per Node'] = df_tursa['Cores'] / df_tursa['Nodes']
    df_tursa['kWh'] = df_tursa['Energy'] / 3600000.0
    df_tursa['Bands/kWh'] = df_tursa['Bands'] / df_tursa['kWh']
    df_tursa['Coreh'] = (df_tursa['Cores'] * df_tursa['Runtime']) / 3600.0
    df_tursa['Nodeh'] = (df_tursa['Nodes'] * df_tursa['Runtime']) / 3600.0
    df_tursa['GPUh'] = (df_tursa['GPUs'] * df_tursa['Runtime']) / 3600.0
    df_tursa['Resource'] = df_tursa['GPUs']
    df_tursa['Peak FP64 Flops'] = df_tursa['GPUs'] * TURSA_FP64_GPU
    return


@app.cell
def _(
    E_ENGLAND_CI,
    NW_ENGLAND_CI,
    PUE,
    SOUTH_SCOTLAND_CI,
    SW_ENGLAND_CI,
    TURSA_EMB_EMISSIONS_RATE,
    TURSA_POWER_OVERHEAD,
    df_tursa,
):
    df_tursa['Emb Emissions'] = df_tursa['GPUh'] * TURSA_EMB_EMISSIONS_RATE
    df_tursa['Emissions (S Scotland)'] = df_tursa['Emb Emissions'] + (df_tursa['kWh'] * TURSA_POWER_OVERHEAD * PUE * SOUTH_SCOTLAND_CI)
    df_tursa['Emissions (NW England)'] = df_tursa['Emb Emissions'] + (df_tursa['kWh'] * TURSA_POWER_OVERHEAD * PUE * NW_ENGLAND_CI)
    df_tursa['Emissions (E England)'] = df_tursa['Emb Emissions'] + (df_tursa['kWh'] * TURSA_POWER_OVERHEAD * PUE * E_ENGLAND_CI)
    df_tursa['Emissions (SW England)'] = df_tursa['Emb Emissions'] + (df_tursa['kWh'] * TURSA_POWER_OVERHEAD * PUE * SW_ENGLAND_CI)
    df_tursa['Bands/kgCO2e (S Scotland)'] = df_tursa['Bands'] / df_tursa['Emissions (S Scotland)']
    df_tursa['Bands/kgCO2e (NW England)'] = df_tursa['Bands'] / df_tursa['Emissions (NW England)']
    df_tursa['Bands/kgCO2e (E England)'] = df_tursa['Bands'] / df_tursa['Emissions (E England)']
    df_tursa['Bands/kgCO2e (SW England)'] = df_tursa['Bands'] / df_tursa['Emissions (SW England)']
    return


@app.cell
def _(df_tursa):
    df_tursa_single = df_tursa.loc[df_tursa['Nodes'] == 1]
    return (df_tursa_single,)


@app.cell
def _(df_archer2, df_cirrus, df_tursa, pd):
    df = pd.concat([df_cirrus, df_archer2, df_tursa], ignore_index=True)
    df_cpu = pd.concat([df_cirrus, df_archer2], ignore_index=True)
    df_cpu_mpi = df_cpu.loc[df_cpu['Threads'] == 1]
    df_single = df.loc[df['Nodes'] == 1]
    return df, df_cpu, df_cpu_mpi, df_single


@app.cell
def _(df_single, sns):
    sns.barplot(data=df_single, y='Label', x='Bands/s', hue='System')
    return


@app.cell
def _(df_cirrus_single):
    df_cirrus_single.sort_values('Bands/s', ascending=False)
    return


@app.cell
def _(df_cirrus_single):
    df_cirrus_single.loc[df_cirrus_single['Bands/s'].idxmax()]
    return


@app.cell
def _(df_archer2_single):
    df_archer2_single.sort_values('Bands/s', ascending=False)
    return


@app.cell
def _(df_archer2_single):
    df_archer2_single.loc[df_archer2_single['Bands/s'].idxmax()]
    return


@app.cell
def _(df_tursa_single):
    df_tursa_single.sort_values('Bands/s', ascending=False)
    return


@app.cell
def _(df_tursa_single):
    df_tursa_single.loc[df_tursa_single['Bands/s'].idxmax()]
    return


@app.cell
def _(df_single, sns):
    sns.barplot(data=df_single, y='Label', x='Bands/kWh', hue='System')
    return


@app.cell
def _(df_single, sns):
    sns.barplot(data=df_single, y='Label', x='Bands/kgCO2e (S Scotland)', hue='System')
    return


@app.cell
def _(df, pyplot, sns):
    ax1 = sns.lineplot(data=df, x='Peak FP64 Flops', y='Bands/s', style='System', markers=True, estimator=max, errorbar=None)
    pyplot.savefig('tio2_bands_scaling.png', dpi=300, bbox_inches='tight')
    ax1
    return


@app.cell
def _(df, pyplot, sns):
    ax2 = sns.lineplot(data=df, x='Peak FP64 Flops', y='Bands/kWh', style='System', markers=True, estimator=max, errorbar=None)
    pyplot.savefig('tio2_bandkwh_scaling.png', dpi=300, bbox_inches='tight')
    ax2
    return


@app.cell
def _(df, pyplot, sns):
    ax3 = sns.lineplot(data=df, x='Peak FP64 Flops', y='Bands/kgCO2e (S Scotland)', style='System', markers=True, estimator=max, errorbar=None)
    pyplot.savefig('tio2_bandkgco2e_scaling.png', dpi=300, bbox_inches='tight')
    ax3
    return


@app.cell
def _(df_cpu, pyplot, sns):
    ax4 = sns.lineplot(data=df_cpu, x='Peak FP64 Flops', y='Bands/s', hue='Label', style='System', markers=True, estimator=max, errorbar=None)
    ax4.set(xlim=(0,600))
    pyplot.savefig('tio2_bands_linalg.png', dpi=300, bbox_inches='tight')
    ax4
    return


@app.cell
def _(df_cpu, pyplot, sns):
    ax5 = sns.lineplot(data=df_cpu, x='Peak FP64 Flops', y='Bands/kWh', hue='Label', style='System', markers=True, estimator=max, errorbar=None)
    ax5.set(xlim=(0,600))
    sns.despine()
    pyplot.savefig('tio2_bandkwh_linalg.png', dpi=300, bbox_inches='tight')
    ax5
    return


@app.cell
def _(df_cpu, pyplot, sns):
    ax6 = sns.lineplot(data=df_cpu, x='Peak FP64 Flops', y='Bands/kgCO2e (S Scotland)', hue='Label', style='System', markers=True, estimator=max, errorbar=None)
    ax6.set(xlim=(0,600))
    pyplot.savefig('tio2_bandkgco2e_linalg.png', dpi=300, bbox_inches='tight')
    ax6
    return


@app.cell
def _(df_cpu, pyplot, sns):
    ax7 = sns.lineplot(data=df_cpu, x='Peak FP64 Flops', y='Bands/s', hue='Threads', style='System', markers=True, estimator=max, errorbar=None)
    ax7.set(xlim=(0, 600))
    pyplot.savefig('tio2_bands_threads.png', dpi=300, bbox_inches='tight')
    ax7
    return


@app.cell
def _(df_cpu, pyplot, sns):
    ax8 = sns.lineplot(data=df_cpu, x='Peak FP64 Flops', y='Bands/kgCO2e (S Scotland)', hue='Threads', style='System', markers=True, estimator=max, errorbar=None)
    ax8.set(xlim=(0, 600))
    pyplot.savefig('tio2_bandkgco2e_threads.png', dpi=300, bbox_inches='tight')
    ax8
    return


@app.cell
def _(df_cpu, pyplot, sns):
    ax9 = sns.lineplot(data=df_cpu, x='Peak FP64 Flops', y='Bands/kWh', hue='Threads', style='System', markers=True, estimator=max, errorbar=None)
    ax9.set(xlim=(0, 600))
    pyplot.savefig('tio2_bandkwh_threads.png', dpi=300, bbox_inches='tight')
    ax9
    return


@app.cell
def _(df_cpu_mpi, pyplot, sns):
    ax10 = sns.lineplot(data=df_cpu_mpi, x='Peak FP64 Flops', y='Bands/s', hue='NCORE', style='System', markers=True, estimator=max, errorbar=None)
    ax10.set(xlim=(0, 600))
    pyplot.savefig('tio2_bands_ncore.png', dpi=300, bbox_inches='tight')
    ax10
    return


@app.cell
def _(df_cpu_mpi, pyplot, sns):
    ax11 = sns.lineplot(data=df_cpu_mpi, x='Peak FP64 Flops', y='Bands/kgCO2e (S Scotland)', hue='NCORE', style='System', markers=True, estimator=max, errorbar=None)
    ax11.set(xlim=(0, 600))
    pyplot.savefig('tio2_bandkgco2e_ncore.png', dpi=300, bbox_inches='tight')
    ax11
    return


@app.cell
def _(df_cpu_mpi, pyplot, sns):
    ax12 = sns.lineplot(data=df_cpu_mpi, x='Peak FP64 Flops', y='Bands/kWh', hue='NCORE', style='System', markers=True, estimator=max, errorbar=None)
    ax12.set(xlim=(0, 600))
    pyplot.savefig('tio2_bandkwh_ncore.png', dpi=300, bbox_inches='tight')
    ax12
    return


@app.cell
def _(df):
    df_emissions = df[['Peak FP64 Flops','System','Bands/kgCO2e (S Scotland)', 'Bands/kgCO2e (NW England)', 'Bands/kgCO2e (E England)', 'Bands/kgCO2e (SW England)']].copy()
    df_emissions
    return (df_emissions,)


@app.cell
def _(df_emissions, pd):
    df_melt_emissions = pd.melt(df_emissions, id_vars=['Peak FP64 Flops', 'System'], value_vars=['Bands/kgCO2e (S Scotland)', 'Bands/kgCO2e (NW England)', 'Bands/kgCO2e (E England)','Bands/kgCO2e (SW England)'], var_name='Location', value_name='Bands/kgCO2e')
    df_melt_emissions
    return (df_melt_emissions,)


@app.cell
def _(df_melt_emissions, pyplot, sns):
    g = sns.FacetGrid(df_melt_emissions, col="Location")
    g.map_dataframe(sns.lineplot, "Peak FP64 Flops", "Bands/kgCO2e", style="System", markers=True, estimator=max, errorbar=None)
    g.set_titles(col_template="{col_name}")
    g.set(xlim=(-10, 600))
    g.add_legend()
    pyplot.savefig('tio2_bandkgco2e_location.png', dpi=300, bbox_inches='tight')
    g
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
