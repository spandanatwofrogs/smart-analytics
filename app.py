import streamlit as st
import pandas as pd
import plotly.express as px
import sys
<<<<<<< HEAD
import os
sys.path.append('.')

from modules.chatbot import chatbot_response
from modules.sentiment import (
    get_sentiment_summary,
    load_sentiment_model,
    analyze_single
)
from modules.prediction import (
    get_customer_distribution,
    get_location_analysis,
    get_top_customers,
    get_occupation_analysis,
    get_subscription_analysis,
    get_accuracy,
    train_and_save,
    predict_single_customer
)
=======
sys.path.append('.')
from modules.chatbot import chatbot_response
from modules.sentiment import get_sentiment_summary, load_sentiment_model, analyze_single
from modules.prediction import get_predictions, train_and_save
>>>>>>> 0f9b7448ba6f27c159251f119ab909abd5b29458

st.set_page_config(
    page_title="Smart Customer Analytics",
    page_icon="",
    layout="wide"
)

st.sidebar.title("Smart Analytics")
st.sidebar.markdown("---")
<<<<<<< HEAD
page = st.sidebar.radio(
    "Go to",
    ["Chatbot",
     "Sentiment Analysis",
     "Sales Analytics",
     "Customer Prediction"]
)
st.sidebar.markdown("---")
st.sidebar.caption("BERT + Random Forest")

# ─────────────────────────────────────────────
# PAGE 1 — CHATBOT
# ─────────────────────────────────────────────
if page == "Chatbot":
    st.title("Customer Assistant Chatbot")
    st.caption(
        "Answers product queries and "
        "store policies instantly"
    )
=======
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
>>>>>>> 0f9b7448ba6f27c159251f119ab909abd5b29458

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "bot",
<<<<<<< HEAD
             "text": (
                 "Hello! Welcome to Smart Analytics Store.\n\n"
                 "I can help you with products, "
                 "prices, deals and policies.\n\n"
                 "What are you looking for?"
             )}
=======
             "text": "Hi! Ask me about products or policies."}
>>>>>>> 0f9b7448ba6f27c159251f119ab909abd5b29458
        ]

    for msg in st.session_state.messages:
        if msg["role"] == "bot":
<<<<<<< HEAD
            st.chat_message("assistant").write(
                msg["text"])
        else:
            st.chat_message("user").write(msg["text"])

    user_input = st.chat_input(
        "Type your question here...")
=======
            st.chat_message("assistant").write(msg["text"])
        else:
            st.chat_message("user").write(msg["text"])

    user_input = st.chat_input("Type your question here...")
>>>>>>> 0f9b7448ba6f27c159251f119ab909abd5b29458
    if user_input:
        st.session_state.messages.append(
            {"role": "user", "text": user_input})
        response = chatbot_response(user_input)
        st.session_state.messages.append(
            {"role": "bot", "text": response})
        st.rerun()

<<<<<<< HEAD
# ─────────────────────────────────────────────
# PAGE 2 — SENTIMENT ANALYSIS
# ─────────────────────────────────────────────
elif page == "Sentiment Analysis":
    st.title("Customer Sentiment Dashboard")
    st.caption(
        "BERT model — DistilBERT fine-tuned "
        "on customer reviews"
    )
=======
# ─────────────────────────────
# PAGE 2: SENTIMENT ANALYSIS
# ─────────────────────────────
elif page == "Sentiment Analysis":
    st.title("Customer Sentiment Dashboard")
    st.caption("Powered by BERT — DistilBERT model")

    col1, col2, col3 = st.columns(3)
>>>>>>> 0f9b7448ba6f27c159251f119ab909abd5b29458

    with st.spinner("Loading sentiment data..."):
        counts = get_sentiment_summary()

<<<<<<< HEAD
    pos   = counts.get('POSITIVE', 0)
    neg   = counts.get('NEGATIVE', 0)
    total = pos + neg

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Positive Reviews",
        f"{round(pos/total*100)}%" if total else "0%",
        f"{pos} reviews"
    )
    col2.metric(
        "Negative Reviews",
        f"{round(neg/total*100)}%" if total else "0%",
        f"{neg} reviews"
    )
=======
    pos = counts.get('POSITIVE', 0)
    neg = counts.get('NEGATIVE', 0)
    total = pos + neg

    col1.metric("Positive Reviews",
                f"{round(pos/total*100)}%" if total else "0%")
    col2.metric("Negative Reviews",
                f"{round(neg/total*100)}%" if total else "0%")
>>>>>>> 0f9b7448ba6f27c159251f119ab909abd5b29458
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
<<<<<<< HEAD
        "Type any review text:")
    if test_text:
        with st.spinner("Analyzing..."):
            model = load_sentiment_model()
            label, score = analyze_single(
                test_text, model)
        if label == "POSITIVE":
            st.success(
                f"POSITIVE — {score}% confidence")
        else:
            st.error(
                f"NEGATIVE — {score}% confidence")

# ─────────────────────────────────────────────
# PAGE 3 — SALES ANALYTICS (products.csv)
# ─────────────────────────────────────────────
elif page == "Sales Analytics":
    st.title("Sales Analytics Dashboard")
    st.caption(
        "Product sales insights from "
        "3,660 transaction records"
    )

    df = pd.read_csv('data/products.csv')

    CAT_COL   = 'Category'
    PRICE_COL = 'Price (Rs.)'
    DISC_COL  = 'Discount (%)'
    PAY_COL   = 'Payment_Method'

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", len(df))
    col2.metric(
        "Categories",
        df[CAT_COL].nunique()
    )
    col3.metric(
        "Avg Price",
        f"₹{round(df[PRICE_COL].mean(), 2)}"
    )
    col4.metric(
        "Avg Discount",
        f"{round(df[DISC_COL].mean(), 1)}%"
    )

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        cat_counts = df[CAT_COL].value_counts()
        fig1 = px.bar(
            x=cat_counts.index,
            y=cat_counts.values,
            title="Transactions by Category",
            color=cat_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        avg_disc = df.groupby(
            CAT_COL)[DISC_COL].mean().reset_index()
        fig2 = px.bar(
            avg_disc,
            x=CAT_COL,
            y=DISC_COL,
            title="Average Discount by Category",
            color=DISC_COL,
            color_continuous_scale='Teal'
        )
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        pay_counts = df[PAY_COL].value_counts()
        fig3 = px.pie(
            values=pay_counts.values,
            names=pay_counts.index,
            title="Payment Method Distribution"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        avg_price = df.groupby(
            CAT_COL)[PRICE_COL].mean().reset_index()
        fig4 = px.bar(
            avg_price,
            x=CAT_COL,
            y=PRICE_COL,
            title="Average Price by Category",
            color=PRICE_COL,
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("Category deep dive")
    selected_cat = st.selectbox(
        "Select a category:",
        df[CAT_COL].unique().tolist()
    )
    sub = df[df[CAT_COL] == selected_cat]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Items", len(sub))
    c2.metric(
        "Min Price",
        f"₹{sub[PRICE_COL].min()}"
    )
    c3.metric(
        "Max Price",
        f"₹{sub[PRICE_COL].max()}"
    )
    c4.metric(
        "Avg Discount",
        f"{round(sub[DISC_COL].mean(), 1)}%"
    )

# ─────────────────────────────────────────────
# PAGE 4 — CUSTOMER PREDICTION (customers.xlsx)
# ─────────────────────────────────────────────
elif page == "Customer Prediction":
    st.title("Customer Value Prediction")
    st.caption(
        "Random Forest — predicts "
        "GOLD / SILVER / BRONZE customer tier"
    )

    if st.button("Train / Retrain Model"):
        with st.spinner("Training..."):
            acc = train_and_save()
        st.success(f"Model trained! Accuracy: {acc}%")

    acc       = get_accuracy()
    df_cust   = pd.read_excel('data/customers.xlsx')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Model Accuracy", f"{acc}%")
    col2.metric("Total Customers", len(df_cust))
    col3.metric(
        "Gold Customers",
        len(df_cust[
            df_cust['Customer_value'] == 'GOLD'])
    )
    col4.metric(
        "Cities",
        df_cust['location'].nunique()
    )

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        dist = get_customer_distribution()
        fig1 = px.pie(
            dist,
            names='Customer Value',
            values='Count',
            title='Customer Value Distribution',
            color='Customer Value',
            color_discrete_map={
                'GOLD':   '#EF9F27',
                'SILVER': '#888780',
                'BRONZE': '#D85A30'
            }
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        loc = get_location_analysis()
        fig2 = px.bar(
            loc,
            x='location',
            y='avg_transaction',
            title='Avg Transaction by City',
            color='avg_transaction',
            color_continuous_scale='Teal'
        )
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        occ = get_occupation_analysis()
        fig3 = px.bar(
            occ,
            x='occupation',
            y='gold_percentage',
            title='Gold Customer % by Occupation',
            color='gold_percentage',
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.subheader("Top 5 customers")
        top = get_top_customers()
        st.dataframe(top, use_container_width=True)

    st.markdown("---")
    st.subheader("Predict customer value")
    st.caption(
        "Enter customer details to predict "
        "GOLD / SILVER / BRONZE"
    )

    p1, p2, p3 = st.columns(3)
    age_in = p1.number_input("Age", 18, 70, 30)
    gen_in = p2.selectbox("Gender",
        ["Female", "Male"])
    loc_in = p3.selectbox("City",
        df_cust['location'].unique().tolist())

    p4, p5, p6 = st.columns(3)
    occ_in = p4.selectbox("Occupation",
        df_cust['occupation'].unique().tolist())
    amt_in = p5.number_input(
        "Total Spent (₹)", 0, 200000, 10000)
    cnt_in = p6.number_input(
        "No. of Transactions", 1, 100, 10)

    p7, p8, p9 = st.columns(3)
    login_in = p7.slider("Login Days", 1, 60, 15)
    supp_in  = p8.number_input(
        "Support Tickets", 0, 20, 2)
    disc_in  = p9.number_input(
        "Discounts Used", 0, 20, 3)

    if st.button("Predict Customer Value"):
        with st.spinner("Predicting..."):
            result = predict_single_customer(
                age_in, gen_in, loc_in,
                occ_in, amt_in, cnt_in, login_in
            )
        if 'GOLD' in result:
            st.success(f"Prediction: {result}")
        elif 'SILVER' in result:
            st.warning(f"Prediction: {result}")
        else:
            st.info(f"Prediction: {result}")
=======
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
>>>>>>> 0f9b7448ba6f27c159251f119ab909abd5b29458
