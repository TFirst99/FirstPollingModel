import numpy as np

def weighted_average(df, weights):
    total_weight = weights.sum()
    harris_avg = np.average(df['Harris'], weights=weights)
    trump_avg = np.average(df['Trump'], weights=weights)
    return {
        'Harris': harris_avg,
        'Trump': trump_avg,
        'Harris_Trump_Difference': harris_avg - trump_avg,
        'Total_Weight': total_weight
    }
