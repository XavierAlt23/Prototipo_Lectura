"""
Utilidades para dividir datasets en train, validation y test.
"""

from sklearn.model_selection import train_test_split


def split_dataset(dataframe, label_column="label", test_size=0.15, validation_size=0.15, random_seed=42):
    train_val, test = train_test_split(
        dataframe,
        test_size=test_size,
        stratify=dataframe[label_column],
        random_state=random_seed,
    )
    relative_validation_size = validation_size / (1 - test_size)
    train, validation = train_test_split(
        train_val,
        test_size=relative_validation_size,
        stratify=train_val[label_column],
        random_state=random_seed,
    )
    return train, validation, test
