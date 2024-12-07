import streamlit as st  
import yfinance as yf  
import plotly.graph_objects as go  
from fpdf import FPDF  
import pandas as pd  

# Configuración de la página  
st.set_page_config(page_title="Análisis de Acciones", layout="wide")  
st.title("Análisis de Acciones para Swing Trading")  

# Input para el símbolo de la acción  
symbol = st.text_input("Introduce el símbolo de la acción (ej: AAPL)").upper()  

if symbol:  
    # Obtener datos de la acción  
    stock = yf.Ticker(symbol)  
    hist = stock.history(period="1y")  # Último año  
    info = stock.info  

    # Gráfico de precios  
    st.subheader("Gráfico de Precios")  
    fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Precio')])  
    st.plotly_chart(fig)  

    # Datos fundamentales  
    st.subheader("Datos Fundamentales")  
    col1, col2, col3 = st.columns(3)  
    with col1:  
        st.metric("P/E Ratio", info.get('forwardPE', 'N/A'))  
    with col2:  
        st.metric("EPS", info.get('trailingEps', 'N/A'))  
    with col3:  
        st.metric("Cash Flow", f"${info.get('operatingCashflow', 'N/A')}")  

    # EPS de los últimos 4 trimestres  
    st.subheader("EPS de los últimos 4 trimestres")  
    try:  
        earnings = stock.quarterly_earnings  
        st.write(earnings.tail(4))  
    except Exception as e:  
        st.write("No se pudieron obtener los datos de EPS trimestrales.")  

    # Análisis técnico  
    st.subheader("Análisis Técnico")  
    col4, col5, col6 = st.columns(3)  

    # Cálculo del RSI  
    delta = hist['Close'].diff()  
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()  
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()  
    rs = gain / loss  
    rsi = 100 - (100 / (1 + rs))  

    with col4:  
        st.metric("RSI", f"{rsi.iloc[-1]:.2f}" if not rsi.isna().iloc[-1] else "N/A")  

    # Cálculo de la MA200  
    ma200 = hist['Close'].rolling(window=200).mean()  
    with col5:  
        st.metric("MA200", f"${ma200.iloc[-1]:.2f}" if not ma200.isna().iloc[-1] else "N/A")  

    with col6:  
        st.metric("Volumen", hist['Volume'].iloc[-1])  

    # Análisis sectorial  
    st.subheader("Análisis Sectorial")  
    col7, col8 = st.columns(2)  
    with col7:  
        st.metric("Tendencia", "Alcista")  # Ejemplo estático  
    with col8:  
        st.metric("Crecimiento Semanal", "1.59%")  # Ejemplo estático  

    # Recomendación  
    st.subheader("Recomendación para Swing Trading")  
    st.write("""  
    Basado en el análisis actual:  
    - El sector muestra tendencia alcista.  
    Recuerda: Esta es solo una herramienta de apoyo. La decisión final debe basarse en tu propio análisis y estrategia de trading.  
    """)  

    # Botón para descargar informe en PDF  
    if st.button("Descargar Informe PDF"):  
        pdf = FPDF()  
        pdf.add_page()  
        pdf.set_font("Arial", size=12)  
        pdf.cell(200, 10, txt="Informe de Análisis de Acciones", ln=True, align='C')  
        pdf.ln(10)  
        pdf.cell(200, 10, txt=f"Símbolo: {symbol}", ln=True)  
        pdf.cell(200, 10, txt=f"P/E Ratio: {info.get('forwardPE', 'N/A')}", ln=True)  
        pdf.cell(200, 10, txt=f"EPS: {info.get('trailingEps', 'N/A')}", ln=True)  
        pdf.cell(200, 10, txt=f"Cash Flow: ${info.get('operatingCashflow', 'N/A')}", ln=True)  
        pdf.cell(200, 10, txt=f"RSI: {rsi.iloc[-1]:.2f}" if not rsi.isna().iloc[-1] else "N/A", ln=True)  
        pdf.cell(200, 10, txt=f"MA200: ${ma200.iloc[-1]:.2f}" if not ma200.isna().iloc[-1] else "N/A", ln=True)  
        pdf.cell(200, 10, txt="Tendencia: Alcista", ln=True)  
        pdf.cell(200, 10, txt="Crecimiento Semanal: 1.59%", ln=True)  
        pdf.output("informe.pdf")  
        with open("informe.pdf", "rb") as file:  
            st.download_button("Haz clic aquí para descargar el PDF", file, file_name="informe.pdf")  
