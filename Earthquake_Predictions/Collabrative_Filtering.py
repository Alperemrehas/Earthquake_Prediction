import data
import pandas as pd
import numpy as np

def collab_filter(data):
    pd.options.display.max_columns = None
    pd.options.display.max_rows = 1000
    print("Now I am filtering")
    # print(data.head(5))
    # print(data["x"].iloc[16264], data["y"].iloc[16264])
    # print(data["x"]["y"].iloc[16264], data["y"].iloc[16264])

    # Calculate the average of all earthquakes in Turkey
    C = data["mag"].mean()
    print("Average of Magninitudes : {}".format(C))

    # Calculate the minimum number of earthquakes required to be in the chart, m
    m = data["mag"].quantile(0.90)
    print("Minumum Required Earthquakes : {}".format(m))

    # Filter out all earthquakes  into a new DataFrame
    q_earthquake = data.copy().loc[data['mag'] >= m]
    # print(data.shape)
    # print(q_earthquake.shape)
    print(max(data["x"]), min(data["x"]))
    print(max(data["y"]), min(data["y"]))
    print(max(data["year"]), min(data["year"]))

    number_of_eq = {"x":[], "y": [], "year":[]}
    for i in range(0,len(data)):
        # for j in range(1973,2022):
        if data["x"].iloc[i] == 2 and data["y"].iloc[i] == 5 :
            number_of_eq["x"].append(data["x"].iloc[i])
            number_of_eq["y"].append(data["y"].iloc[i])
            number_of_eq["year"].append(data["year"].iloc[i])

    # print(number_of_eq)
    print(type(q_earthquake))
    alt_df = data.drop(['time','latitude','longitude','place'],axis = 1)
    # print(alt_df)

    # Cell earthquake average,min,max,count regarding to every year
    user_item_eq = (alt_df.groupby(['x', 'y','year'], as_index=False).mean())
    user_item_min = (alt_df.groupby(['x', 'y', 'year'], as_index=False).min())
    user_item_max = (alt_df.groupby(['x', 'y', 'year'], as_index=False).max())
    user_item_count = (alt_df.groupby(['x', 'y', 'year'], as_index=False).count())
    user_rating = user_item_eq.drop(['year'],axis = 1)
    mean_min = pd.merge(user_item_eq, user_item_min, on=["x", "y","year"],suffixes=('_mean', '_min'))
    merged_df = pd.merge(mean_min, user_item_max, on=["x", "y", "year"])
    merged_df = merged_df.rename(columns={'mag': 'mag_max'})
    merged_df = pd.merge(merged_df, user_item_count, on=["x", "y", "year"])
    merged_df = merged_df.rename(columns={'mag': 'Num_of_Eqs'})

    # Calculating the M

    # print("MEAN")
    # print(user_item_eq)
    # print("MIN")
    # print(user_item_min)
    # print("MAX")
    # print(user_item_max)
    # print("USER")
    # print(user_rating)
    # print("Count")
    # print(user_item_count)
    print("COMBINED")
    print(merged_df.iloc[0:2])

    # Model Based Filtering(Item-Item)
    new_df1 = merged_df
    ratings_matrix = new_df1.pivot_table(values='mag_mean', index=['x','y'], columns='year', fill_value=0)
    print(ratings_matrix[0:2])
    # print(ratings_matrix.shape)

    X = ratings_matrix.T
    # print(X.head())
    # print(X.shape)

    X1 = X

    # Decomposing the Matrix
    from sklearn.decomposition import TruncatedSVD
    SVD = TruncatedSVD(n_components=10)
    decomposed_matrix = SVD.fit_transform(X)
    # print(decomposed_matrix.shape)

    # Correlation Matrix
    correlation_matrix = np.corrcoef(decomposed_matrix)
    # print(correlation_matrix.shape)

    print("Subject Earthquake Year to Find Similar Years: {} ".format(X.index[47]))

    i = X.index[47]

    earthquake_names = list(X.index)
    earthquake_ID = earthquake_names.index(i)
    # print(product_ID)

    correlation_earthquake_ID = correlation_matrix[earthquake_ID]
    # print(correlation_earthquake_ID.shape)
    print(correlation_earthquake_ID[0:2])

    Recommend = list(X.index[correlation_earthquake_ID > 0.75])

    # Removes the years already have earthquake by the cell
    Recommend.remove(i)

    print(Recommend[0:50])

    done = "Similart"
    return done

