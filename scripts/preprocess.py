import pandas as pd

def preprocess_m5_sales(filepath):
    df = pd.read_csv(filepath)
    df = df.drop(columns=['id','item_id','dept_id','cat_id','store_id','state_id'])
    df = df.sum().reset_index()
    df.columns = ['d', 'sales']
    df['sales'] = df['sales'].rolling(window=7, min_periods=1).mean()  # Smooth with rolling avg
    start_date = pd.to_datetime('2011-01-29')
    df['Date'] = pd.date_range(start=start_date, periods=len(df), freq='D')
    df = df[['Date', 'sales']]
    return df


def preprocess_m5_by_item(filepath, item_id, agg_method='sum'):
    df = pd.read_csv(filepath)

    # Filter for the item
    df = df[df['item_id'] == item_id]

    # Only keep daily sales columns (d_1 to d_1913)
    day_cols = [col for col in df.columns if col.startswith('d_')]
    
    if agg_method == 'mean':
        df = df[day_cols].mean().reset_index()
    elif agg_method == 'store_1':
        df = df.iloc[0][day_cols].reset_index()
    else:  # Default: sum over all stores
        df = df[day_cols].sum().reset_index()

    df.columns = ['d', 'sales']
    df['Date'] = pd.date_range(start='2011-01-29', periods=len(df), freq='D')
    df = df[['Date', 'sales']]
    
    return df
