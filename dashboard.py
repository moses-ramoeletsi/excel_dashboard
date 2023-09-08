import pandas as pd
import streamlit as st
import plotly.express as px

dataset = pd.read_excel('Sales.xlsx')

st.set_page_config(page_title="Ralenki Sales", layout="wide")

category = st.sidebar.multiselect("Filter By Category", 
                                  options=dataset["CATEGORY"].unique(),
                                  default=dataset["CATEGORY"].unique())
selection_query=dataset.query("CATEGORY == @category")

# st.dataframe(selection_query)
st.title("Ralenki Dashboard")

total_profit=(selection_query["PROFIT"].sum())
avg_rating=round((selection_query["AVG_RATING"].mean()),2)

first_column,second_column = st.columns(2)

with first_column:
    st.markdown("### Total Profit: ")
    st.subheader(f'{total_profit} $')
with second_column:
    st.markdown("### AVG Products Rating")
    st.subheader(f'{avg_rating}')

st.markdown("---")

profit_by_catagory = (selection_query.groupby(by=["CATEGORY"]).sum()[["PROFIT"]])

profit_by_catagory_barchart = px.bar(profit_by_catagory,
                                     x="PROFIT",
                                     y=profit_by_catagory.index,
                                     title="Profit By Category",
                                     color_discrete_sequence=["#17f50c"],
                                     )

profit_by_catagory_barchart.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))

profit_by_catagory_piechart = px.pie(profit_by_catagory, names=profit_by_catagory.index,values="PROFIT", title="Profit % By Category", hole=.3, color=profit_by_catagory.index,color_discrete_sequence=px.colors.sequential.RdBu_r)

left_column,right_column = st.columns(2)
left_column.plotly_chart(profit_by_catagory_barchart,use_container_width=True)
right_column.plotly_chart(profit_by_catagory_piechart,use_container_width=True)



hide= """ 
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
</style

"""

st.markdown(hide,unsafe_allow_html=True)
