import pandas as pd

# day in seconds
_index = range(24 * 60 * 60)


def read_excel(file) -> pd.DataFrame:
    """Read, transform and expand source excel file"""
    df = pd.read_excel(file, names='tvd', dtype=str)
    # transform time to seconds
    df['t'] = [d.seconds for d in pd.to_timedelta(df['t'])]
    # replace 'x' to 0
    df['v'] = df['v'].replace({'x': 0}).astype(float)
    # transform delta to seconds
    df['d'] = [d.seconds for d in pd.to_timedelta(df['d'])]
    # resulting dataframe
    target = pd.DataFrame(index=_index, columns=['v'])
    # expand data intervals
    for t, v, d in df.itertuples(index=False):
        target[t: t + d] = v
    target.fillna(0, inplace=True)
    return target
