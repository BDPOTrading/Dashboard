import json
import requests
import pandas as pd
import streamlit as st
import numpy as np
from twelvedata import TDClient
import plotly.express as px
import requests
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
st.set_page_config(layout="wide")

apikey="6004f900eaab46259d06a95edc95c314"
td = TDClient(apikey=apikey)
fmpAPI = 'aa005c9f1003c4b4d396cc1e7037272f'







def chart_data(asset):

    symbol = asset

    URL = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=500&apikey={fmpAPI}"


    data = requests.get(URL)
    data = data.json()


    lSymbol = []
    lDate = []
    lEps =[]
    lEbitda =[]

    for value in data:

        date = value['date']
        eps = value['eps']
        ebitda = value['ebitda']

        lDate.append(date)
        lEps.append(eps)
        lEbitda.append(ebitda)


    df = pd.DataFrame()


    df['date'] = lDate 
    df['eps'] = lEps
    df['ebitda'] = lEbitda 
    df = df.set_index('date')
    print(df)

    return df

def dcf(asset):
    URL = f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{asset}?limit=500&apikey={fmpAPI}"


    data = requests.get(URL)
    data = data.json()

    lDate = []
    lDcf =[]
    lPrice =[]

    for value in data:

        date = value['date']
        currentPrice = value['Stock Price']
        dcfPrice = value['dcf']

        lDate.append(date)
        lPrice.append(currentPrice)
        lDcf.append(dcfPrice)


    df = pd.DataFrame()


    df['date'] = lDate 
    df['DCF'] = lDcf
    df['Price'] = lPrice 
    df = df.set_index('date')

    print(df)
    return df

def sectorPerformance():
    URL = f"https://financialmodelingprep.com/api/v3/sector-performance?apikey={fmpAPI}"
    data = requests.get(URL)
    data = data.json()
    print(data)

    sectorl =[]
    changesPercentagel =[]


    for value in data:
        sector = value['sector']
        perChange = value['changesPercentage']  

        perChange = perChange.replace("%", "")
        perChange = pd.to_numeric(perChange)

        

        sectorl.append(sector)
        changesPercentagel.append(perChange)


    df = pd.DataFrame()


    df['Sector'] = sectorl 
    df['Movement (%)'] = changesPercentagel

    df = df.set_index('Sector')

    print(df)
    return df

def tickerGraph(asset):
    ts = td.time_series(
    symbol=asset,
    outputsize=500,
    interval="1day",
)

    tickerDf = ts.as_pandas()
    print(tickerDf)

    ts.as_plotly_figure()
    chart = ts.with_ema(time_period=200).with_ema(time_period=50).with_mom().with_macd().as_plotly_figure()
    return chart, tickerDf

def sectorgraph():
    df = sectorPerformance()
    fig = px.bar(df, x=df.index, y='Movement (%)')
    # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=True)
    fig.update_layout(yaxis={'visible': True, 'showticklabels': True})
    sectorGraphObject = fig
    return sectorGraphObject

def gainerslosers():

    loserSymbolsl = []
    gainersSymbolsl = []
    losernamel = []
    gainernamel = []
    loserchangel=[]
    gainerchangel = []
    typeLoser = []
    typeGainer = []

    fmpAPI = 'aa005c9f1003c4b4d396cc1e7037272f'



    URL = f"https://financialmodelingprep.com/api/v3/stock_market/losers?apikey={fmpAPI}"
    URLGainer = f"https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey={fmpAPI}"
    data = requests.get(URL)
    data = data.json()

    dataGainer = requests.get(URLGainer)
    dataGainer = dataGainer.json()


    for value in data:
        symbol = value['symbol']
        name = value['name']
        changeLoser = np.absolute(value['changesPercentage'])

        loserSymbolsl.append(symbol)
        losernamel.append(name)
        loserchangel.append(changeLoser)
        typeLoser.append('Loser')

    for value in dataGainer:
        symbol = value['symbol']
        name = value['name']
        changeGainer = value['changesPercentage']

        gainersSymbolsl.append(symbol)
        gainernamel.append(name)
        gainerchangel.append(changeGainer)
        typeGainer.append('Gainer')

    dfLoser = pd.DataFrame()
    dfGainer = pd.DataFrame()

    dfLoser['Symbol'] = loserSymbolsl 
    dfLoser['Name'] = losernamel
    dfLoser['Type'] = typeLoser
    dfLoser['Change'] = loserchangel

    dfGainer['Symbol'] = gainersSymbolsl 
    dfGainer['Name'] = gainernamel
    dfGainer['Type'] = typeGainer
    dfGainer['Change'] = gainerchangel

    dfLoser = dfLoser.set_index('Symbol')
    dfGainer = dfGainer.set_index('Symbol')


    frames = [dfGainer, dfLoser]

    result = pd.concat(frames)
    result = result.sort_values('Name')

    fig = px.scatter(result, x='Name', y="Change", color="Type",
                hover_name="Name",size="Change")

    return dfLoser, dfGainer, result, fig

def incomeStatement(asset):
    URL = f'https://financialmodelingprep.com/api/v3/income-statement/{asset}?limit=240&apikey={fmpAPI}'
    data = requests.get(URL)
    data = data.json()
    print(data)

    datel= []
    revenuel = []
    grossProfitl = []
    netIncomel = []


    for value in data:
        date = value['date']
        revenue = value['revenue']
        grossProfit = value['grossProfit']
        netIncome = value['netIncome']

        datel.append(date)
        revenuel.append(revenue)
        grossProfitl.append(grossProfit)
        netIncomel.append(netIncome)

        df = pd.DataFrame()

        df['Date'] = datel
        df['Revenue'] = revenuel
        df['Gross profit'] = grossProfitl
        df['Net income'] = netIncomel

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Date'], y=df['Revenue'],
                        mode='lines+markers',
                        name='Revenue'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Gross profit'],
                        mode='lines+markers',
                        name='Gross profit'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Net income'],
                        mode='lines+markers',
                        name='Net income'))


    print(df)
    return df, fig



def marketNews():
    URL  = f"https://financialmodelingprep.com/api/v3/fmp/articles?page=0&size=30&apikey={fmpAPI}"
    data = requests.get(URL)
    data = data.json()

    titleL = []
    datel = []

    for value in data['content']:
        date = (value['date']) 
        title = (value['title']) 
        content = (value['content']) 

        titleL.append(title)
        datel.append(date)

    return titleL, datel















add_selectbox = st.sidebar.selectbox(
    "Dashboard type?",
    ("Main", "Comparision")
)

if add_selectbox == "Comparision":
    st.title('Hello world')

if add_selectbox == "Main":
    
    st.title('Nasdaq Dashboard')
    st.header('Enter a ticker or run market summary')

    ticker = st.text_input('Enter a ticker', value='MSFT')
    option = st.selectbox(
            'Summary graph',
            ('QQQ', 'SPY', 'DIA'))
    ticker = ticker.upper()

    button1, button2, button3 = st.columns(3, gap='large')
    with button1:
        buttonPressed = st.button('Run ticker')
    with button2:
        marketSummaryPressed = st.button('Run market summary')
    
    with button3:
        newsButton = st.button('Market headlines')





    if buttonPressed:
        if ticker != "":
            st.success(f'Ticker found: {ticker}')
            incState, incomeStatementChart = incomeStatement(ticker)
            chart_data = chart_data(ticker)
            dcfData = dcf(ticker)
            tickerChart, tickerDataFrame = tickerGraph(ticker)
            
            upside = round((((round((dcfData['DCF'][-1]),2) - round((dcfData['Price'][-1]),2))/round((dcfData['Price'][-1]),2))*100),2)

            curretStockPrice = round((dcfData['Price'][-1]),2)

            
            epsData = chart_data['eps']


            currenEPS = round(chart_data['eps'][0], 2)
            priorYearEPS = round(chart_data['eps'][1], 2)
            priorTwoEPS = round(chart_data['eps'][2], 2)

            yearOneMovement = round((((chart_data['eps'][0] - chart_data['eps'][1])/chart_data['eps'][1])*100),2)
            yearTwoMovement = round((((chart_data['eps'][1] - chart_data['eps'][2])/chart_data['eps'][2])*100),2)
            yearThreeMovement = round((((chart_data['eps'][2] - chart_data['eps'][3])/chart_data['eps'][3])*100),2)


            st.plotly_chart(tickerChart, use_container_width=True)

            st.header('DCF Valuation')
        

            co1, co2, co3 = st.columns(3)   
            co1.metric('Date', dcfData.index[-1], delta=None)
            co2.metric("Share Price", curretStockPrice, delta=None)
            co3.metric("DCF / Upside", round((dcfData['DCF'][-1]),2), f'{upside}%')

            st.header('EPS Movement')
            col1, col2, col3 = st.columns(3)
    
            col1.metric("Current Year EPS Movement", currenEPS, f'{yearOneMovement}%')
            col2.metric("Prior Year EPS Movement", priorYearEPS, f'{yearTwoMovement}%')
            col3.metric("2 Years Prior EPS Movement", priorTwoEPS, f'{yearThreeMovement}%')


            st.plotly_chart(incomeStatementChart, use_container_width= True)

    
            col1, col2 = st.columns(2)

            with col1:
                df = epsData
                fig = px.bar(df, x=df.index, y='eps', text_auto='.2s', title="EPS Growth")
                fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=True)
                fig.update_layout(yaxis={'visible': True, 'showticklabels': False})
                epsBarChart = fig
                st.plotly_chart(epsBarChart, use_container_width=True)


            with col2:
                ebitdaGrowth = chart_data['ebitda']
                fig = px.bar(ebitdaGrowth, x=df.index, y='ebitda', text_auto='.2s', title="Ebitda Movement")
                fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=True)
                fig.update_layout(yaxis={'visible': True, 'showticklabels': False})
                edbitdaChart = fig
                st.plotly_chart(edbitdaChart, use_container_width= True)









            st.header('Raw data')
            st.table(chart_data)
            st.table(incState)
            st.table(tickerDataFrame)
        else:
            st.text('ticker cant be blank')

    if marketSummaryPressed:
        st.success('Running market summary')

        sectorData = sectorPerformance()
        tickerChart, tickerDataFrame = tickerGraph(option)
        losers, gainers, full, gainerloserChart = gainerslosers()
        st.plotly_chart(tickerChart, use_container_width=True)
        st.subheader('Gainer / Losers')
        st.plotly_chart(gainerloserChart, use_container_width=True)
        st.subheader('Sector performance')
        st.plotly_chart(sectorgraph(), use_container_width=True)
        st.subheader('Raw Data')
        st.table(sectorData)
        st.table(losers)
        st.table(gainers)
        st.table(tickerDataFrame)

    if newsButton:
        data, date = marketNews()
        st.markdown(f'◼ {date[0]}: {data[0]}')
        st.markdown(f'◼ {date[1]}: {data[1]}')
        st.markdown(f'◼ {date[2]}: {data[2]}')
        st.markdown(f'◼ {date[3]}: {data[3]}')
        st.markdown(f'◼ {date[4]}: {data[4]}')
        st.markdown(f'◼ {date[5]}: {data[5]}')
        st.markdown(f'◼ {date[6]}: {data[6]}')
        st.markdown(f'◼ {date[7]}: {data[7]}')
        st.markdown(f'◼ {date[8]}: {data[8]}')
        st.markdown(f'◼ {date[9]}: {data[9]}')
        st.markdown(f'◼ {date[10]}: {data[10]}')
        st.markdown(f'◼ {date[11]}: {data[11]}')
        st.markdown(f'◼ {date[12]}: {data[12]}')
        st.markdown(f'◼ {date[13]}: {data[13]}')
        st.markdown(f'◼ {date[14]}: {data[14]}')
        st.markdown(f'◼ {date[15]}: {data[15]}')
        st.markdown(f'◼ {date[16]}: {data[16]}')
        st.markdown(f'◼ {date[17]}: {data[17]}')
        st.markdown(f'◼ {date[18]}: {data[18]}')
        st.markdown(f'◼ {date[19]}: {data[19]}')
        st.markdown(f'◼ {date[20]}: {data[20]}')
        st.markdown(f'◼ {date[21]}: {data[21]}')
        st.markdown(f'◼ {date[22]}: {data[22]}')
        st.markdown(f'◼ {date[23]}: {data[23]}')
        st.markdown(f'◼ {date[24]}: {data[24]}')
        st.markdown(f'◼ {date[25]}: {data[25]}')
        st.markdown(f'◼ {date[26]}: {data[26]}')
        st.markdown(f'◼ {date[27]}: {data[27]}')
        st.markdown(f'◼ {date[28]}: {data[28]}')
        st.markdown(f'◼ {date[29]}: {data[29]}')

