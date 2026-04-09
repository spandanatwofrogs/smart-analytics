import streamlit as st
import pandas as pd
import plotly.express as px
import sys
sys.path.append('.')
from modules.chatbot import chatbot_response
from modules.sentiment import get_sentiment_summary, load_sentiment_model, analyze_single
from modules.prediction import get_predictions, train_and_save

st.set_page_config(
    page_title="Smart Customer Analytics",
    page_icon="",
    layout="wide"
)

st.sidebar.title("Smart Analytics")
st.sidebar.markdown("---")
page = st.sidebar.radio("Go to", 
    ["Chatbot", "Sentiment Analysis", "Sales Prediction"])
st.sidebar.markdown("---")
st.sidebar.caption("Built with BERT + Random Forest")

# ─────────────────────────────
# PAGE 1: CHATBOT
# ─────────────────────────────
if page == "Chatbot":
    st.title("Customer Assistant Chatbot")
    st.caption(
        "Ask about products, prices, policies or recommendations")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "bot",
             "text": "Hi! Ask me about products or policies."}
        ]

    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            st.chat_message("assistant").write(msg["text"])
        else:
            st.chat_message("user").write(msg["text"])

    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.session_state.messages.append(
            {"role": "user", "text": user_input})
        response = chatbot_response(user_input)
        st.session_state.messages.append(
            {"role": "bot", "text": response})
        st.rerun()

# ─────────────────────────────
# PAGE 2: SENTIMENT ANALYSIS
# ─────────────────────────────
elif page == "Sentiment Analysis":
    st.title("Customer Sentiment Dashboard")
    st.caption("Powered by BERT — DistilBERT model")

    col1, col2, col3 = st.columns(3)

    with st.spinner("Loading sentiment data..."):
        counts = get_sentiment_summary()

    pos = counts.get('POSITIVE', 0)
    neg = counts.get('NEGATIVE', 0)
    total = pos + neg

    col1.metric("Positive Reviews",
                f"{round(pos/total*100)}%" if total else "0%")
    col2.metric("Negative Reviews",
                f"{round(neg/total*100)}%" if total else "0%")
    col3.metric("Total Analyzed", f"{total}")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        fig1 = px.pie(
            values=counts.values,
            names=counts.index,
            title="Overall Sentiment Distribution",
            color_discrete_map={
                'POSITIVE': '#1D9E75',
                'NEGATIVE': '#E24B4A'
            }
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = px.bar(
            x=counts.index,
            y=counts.values,
            title="Review Count by Sentiment",
            color=counts.index,
            color_discrete_map={
                'POSITIVE': '#1D9E75',
                'NEGATIVE': '#E24B4A'
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Test live sentiment")
    test_text = st.text_input(
        "Type any review text and see the result:")
    if test_text:
        with st.spinner("Analyzing..."):
            model = load_sentiment_model()
            label, score = analyze_single(test_text, model)
        if label == "POSITIVE":
            st.success(f"POSITIVE — {score}% confidence")
        else:
            st.error(f"NEGATIVE — {score}% confidence")

# ─────────────────────────────
# PAGE 3: SALES PREDICTION
# ─────────────────────────────
elif page == "Sales Prediction":
    st.title("Sales Prediction Dashboard")
    st.caption(
        "Random Forest model trained on historical sales data")

    if st.button("Train / Retrain Model"):
        with st.spinner("Training model..."):
            acc = train_and_save()
        st.success(f"Model trained! Accuracy: {acc}%")

    with st.spinner("Loading predictions..."):
        df_pred = get_predictions()

    col1, col2, col3 = st.columns(3)
    col1.metric("Categories Analyzed", len(df_pred))
    col2.metric("High Demand Categories",
                len(df_pred[df_pred['Demand Score'] >= 50]))
    col3.metric("Model", "Random Forest")

    st.markdown("---")
    fig = px.bar(
        df_pred,
        x='Category',
        y='Demand Score',
        title='Predicted Demand Score by Category (%)',
        color='Demand Score',
        color_continuous_scale='Teal'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Top predicted high-demand categories")
    st.dataframe(
        df_pred.sort_values(
            'Demand Score', ascending=False),
        use_container_width=True
    )