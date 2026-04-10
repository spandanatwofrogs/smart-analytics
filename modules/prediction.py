import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load data
def load_data():
    return pd.read_excel('data/customers.xlsx')

# Train model
def train_and_save():
    df = load_data().copy()

    le_gender = LabelEncoder()
    le_location = LabelEncoder()
    le_occ = LabelEncoder()
    le_target = LabelEncoder()

    df['Gender'] = le_gender.fit_transform(df['Gender'])
    df['location'] = le_location.fit_transform(df['location'])
    df['occupation'] = le_occ.fit_transform(df['occupation'])
    df['Customer_value'] = le_target.fit_transform(df['Customer_value'])

    X = df[['Age', 'Gender', 'location', 'occupation',
            'total_spent', 'num_transactions', 'login_days']]
    y = df['Customer_value']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    acc = round(model.score(X_test, y_test) * 100, 2)

    os.makedirs('models', exist_ok=True)
    with open('models/model.pkl', 'wb') as f:
        pickle.dump((model, le_gender, le_location, le_occ, le_target), f)

    with open('models/accuracy.txt', 'w') as f:
        f.write(str(acc))

    return acc

# Accuracy
def get_accuracy():
    try:
        with open('models/accuracy.txt', 'r') as f:
            return float(f.read())
    except:
        return 0

# Prediction
def predict_single_customer(age, gender, location, occupation,
                            total_spent, num_transactions, login_days):

    with open('models/model.pkl', 'rb') as f:
        model, le_gender, le_location, le_occ, le_target = pickle.load(f)

    gender = le_gender.transform([gender])[0]
    location = le_location.transform([location])[0]
    occupation = le_occ.transform([occupation])[0]

    pred = model.predict([[
        age, gender, location, occupation,
        total_spent, num_transactions, login_days
    ]])

    return le_target.inverse_transform(pred)[0]

# Dashboard functions
def get_customer_distribution():
    df = load_data()

    dist = df['Customer_value'].value_counts().reset_index()
    dist.columns = ['Customer Value', 'Count']  # ✅ FIX

    return dist

def get_location_analysis():
    df = load_data()
    return df.groupby('location')['total_spent'].mean().reset_index().rename(
        columns={'total_spent': 'avg_transaction'}
    )

def get_top_customers():
    df = load_data()
    return df.sort_values(by='total_spent', ascending=False).head(5)

def get_occupation_analysis():
    df = load_data()
    gold = df[df['Customer_value'] == 'GOLD']

    total = df.groupby('occupation').size()
    gold_count = gold.groupby('occupation').size()

    result = (gold_count / total * 100).fillna(0).reset_index()
    result.columns = ['occupation', 'gold_percentage']
    return result

def get_subscription_analysis():
    df = load_data()
    if 'subscription_type' in df.columns:
        return df['subscription_type'].value_counts()
    return None