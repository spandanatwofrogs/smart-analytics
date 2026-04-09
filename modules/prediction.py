import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def train_and_save():
    df = pd.read_csv('data/sales.csv')
    print("Sales columns:", df.columns.tolist())

    # Find quantity and category columns automatically
    qty_col = [c for c in df.columns
               if 'qty' in c.lower() or 'quantity' in c.lower()
               or 'units' in c.lower()][0]
    cat_col = [c for c in df.columns
               if 'category' in c.lower() or 'cat' in c.lower()][0]
    price_col = [c for c in df.columns
                 if 'price' in c.lower()][0]

    # Create target: 1 = high demand
    df['high_demand'] = (
        df[qty_col] >= df[qty_col].median()).astype(int)

    le = LabelEncoder()
    df['cat_encoded'] = le.fit_transform(df[cat_col].astype(str))

    X = df[['cat_encoded', price_col]]
    y = df['high_demand']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    accuracy = round(model.score(X_test, y_test) * 100, 1)
    print(f"Model accuracy: {accuracy}%")

    os.makedirs('models', exist_ok=True)
    pickle.dump({'model': model, 'encoder': le,
                 'cat_col': cat_col, 'price_col': price_col,
                 'qty_col': qty_col},
                open('models/sales_model.pkl', 'wb'))
    print("Model saved.")
    return accuracy

def get_predictions():
    if not os.path.exists('models/sales_model.pkl'):
        train_and_save()
    data = pickle.load(open('models/sales_model.pkl', 'rb'))
    model = data['model']
    le = data['encoder']
    cat_col = data['cat_col']
    price_col = data['price_col']
    qty_col = data['qty_col']

    df = pd.read_csv('data/sales.csv')
    df['cat_encoded'] = le.transform(df[cat_col].astype(str))
    df['predicted_demand'] = model.predict(
        df[['cat_encoded', price_col]])
    df['demand_label'] = df['predicted_demand'].map(
        {1: 'High', 0: 'Low'})

    summary = df.groupby(cat_col)['predicted_demand'].mean()
    summary = summary.sort_values(ascending=False).reset_index()
    summary.columns = ['Category', 'Demand Score']
    summary['Demand Score'] = (
        summary['Demand Score'] * 100).round(1)
    return summary