from pandas import DataFrame, Series

from sample_code import dataframe


def max_customer_account_balance(dataframe: DataFrame) -> DataFrame:
    """Adds a column with the maximum account balance to the DataFrame."""
    dataframe["balance_max"] = dataframe["balance"].max()
    return dataframe


def customers_mean_age(dataframe: DataFrame) -> DataFrame:
    """Adds a column with the mean age of all customers to the DataFrame."""
    dataframe["age_mean"] = dataframe["age"].mean()
    return dataframe


def gb_max_customer_account_balance(dataframe: DataFrame) -> DataFrame:
    """Adds a column with the maximum account balance to the DataFrame."""
    dataframe["balance_max"] = dataframe["balance"].max()
    return dataframe["balance_max"].iloc[0]


def gb_customers_mean_age(dataframe: DataFrame) -> DataFrame:
    """Adds a column with the mean age of all customers to the DataFrame."""
    dataframe["age_mean"] = dataframe["age"].mean()
    return dataframe["age_mean"].iloc[0]


def marital_status_groups(dataframe: DataFrame) -> DataFrame:
    return dataframe.groupby("marital").apply(
        lambda x: Series(
            {
                "balance_max": gb_max_customer_account_balance(x),
                "age_mean": gb_customers_mean_age(x),
            }
        ),
        include_groups=False,
    )


def creating_features_banking_data(dataframe):
    return dataframe.pipe(max_customer_account_balance).pipe(customers_mean_age)


if __name__ == "__main__":
    banking_customers_df = creating_features_banking_data(dataframe)
    print(banking_customers_df.head())
    print(marital_status_groups(dataframe))
