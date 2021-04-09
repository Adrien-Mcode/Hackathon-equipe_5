

def preprocess(df, config):
    if config.only_quantitative:
        df = df[['total_supply', 'declared_supply', 'manual_added_supply',
                      'manual_removed_supply', 'meals_saved', 'consumer_cancellation',
                      'store_cancellation', 'item_price', 'meals_refunded',
                      'rating_count', 'sum_rating_overall', 'target']]
    inputers = []
    return df, inputers