import plotly.express as px

def ranking_carreras_chart(df_ranking):
    fig = px.bar(
        df_ranking,
        x="carrera",
        y="cantidad",
        title="Ranking de Carreras",
    )
    return fig
