def apply_filter(df, slider_values, slider_ids):
    for value, id in zip(slider_values, slider_ids):
        if value:
            low, high = value
            col_name = id['index']
            mask = (df[col_name] >= low) & (df[col_name] <= high)
            df = df[mask]
    
    return df