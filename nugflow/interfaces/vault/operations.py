import hashlib
from typing import Iterable, List
import pandas as pd

from .entities import VaultData, data_marker_missing_value


def get_vault_hash(df: pd.DataFrame, cols: Iterable[str]) -> pd.Series:
    """Implementation of the recommended vault hashing algorithm
        >>> df = pd.DataFrame({'license_number': [1, 2, 3]})
        >>> vault_hash(df, ['license_number']) 
    """
    cols = sorted(cols)
    head, *tail = cols
    joined = df[head].astype(str).str.cat(df[tail].astype(str), sep="|")
    hashed = joined.apply(lambda r: hashlib.md5(r.lower().encode()).hexdigest())
    return hashed


def get_hash_key(vd: VaultData) -> pd.Series:
    """Apply the hash key algorithm to a set of business values."""
    return get_vault_hash(vd.data, vd.hkey_columns)


def get_hash_diff(vd: VaultData) -> pd.Series:
    """Hash diff should follow the same hkey algorithm but for all business valued columns"""
    return get_vault_hash(vd.data, vd.attribute_columns)


def hash(vd: VaultData) -> VaultData:
    """Apply vault data hashing and transforms"""
    cols = list(vd.data)
    print(f"cols: {cols}")
    for col in vd.hkey_columns:
        vd.data[col] = vd.data[col].fillna(data_marker_missing_value)
    vd.data["hkey"] = get_hash_key(vd)
    vd.data = vd.data.drop_duplicates(subset=["hkey"])
    if vd.attribute_columns:
        vd.data["hash_diff"] = get_hash_diff(vd)
    return vd


def snake(col: str) -> str:
    """Next implementation abstract this to utils"""
    return "_".join([word.lower() for word in col.split(" ")])


def df_to_vault(
    df: pd.DataFrame,
    date: str,
    source_service: str,
    tbl_metadata: Iterable[tuple],
    column_rename: dict = None,
) -> List[VaultData]:
    """Transform dataframe to vault shaped object"""
    vault_data = list()

    columns = {col: snake(col) for col in list(df)}
    df = df.rename(columns=columns)

    if column_rename:
        df = df.rename(columns=column_rename)

    for cols, hkey_cols, tbl in tbl_metadata:
        _df = df.reindex(columns=cols)
        _df["load_date"] = date
        _df["source_service"] = source_service
        vault_datum = VaultData(tbl, hkey_cols, _df)
        hash(vault_datum)
        vault_data.append(vault_datum)

    return vault_data
