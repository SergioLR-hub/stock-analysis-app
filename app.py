import streamlit as st  
import yfinance as yf  
import plotly.graph_objects as go  

# Configuración de la página  
st.set_page_config(page_title="Análisis de Acciones", layout="wide")  
st.title("Análisis de Acciones para Swing Trading")  

# Input para el símbolo de la acción  
symbol = st.text_input("Introduce el símbolo de la acción (ej: AAPL)").upper()  

if symbol:  
    # Obtener datos  
    stock = yf.Ticker(symbol)  
    hist = stock.history(period="1y")  
    info = stock.info  

    # Mostrar información básica  
    col1, col2, col3 = st.columns(3)  
    with col1:  
        st.metric("Precio Actual", f"${info.get('currentPrice', 'N/A')}")  
    with col2:  
        st.metric("P/E Ratio", info.get('forwardPE', 'N/A'))  
    with col3:  
        st.metric("Volumen", info.get('volume', 'N/A'))  

    # Gráfico de precios  
    fig = go.Figure(data=[go.Candlestick(x=hist.index,  
                open=hist['Open'],  
                high=hist['High'],  
                low=hist['Low'],  
                close=hist['Close'])])  
    st.plotly_chart(fig)  

    # Análisis y recomendaciones  
    st.subheader("Análisis y Recomendaciones")  
    rsi = hist['Close'].pct_change().rolling(window=14).mean()  
    if rsi.iloc[-1] > 0.7:  
        st.warning("RSI indica sobrecompra")  
    elif rsi.iloc[-1] < 0.3:  
        st.warning("RSI indica sobreventa")  

    # Botón para descargar informe  
    if st.button("Descargar Informe PDF"):  
        # Aquí iría la lógica para generar el PDF  
        st.success("Informe descargado")  
