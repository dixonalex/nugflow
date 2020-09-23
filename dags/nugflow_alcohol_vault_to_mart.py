# import typing
# from nugflow.config import bootstrap
# from nugflow.interfaces.db import Db
# import nugflow.interfaces.vault as vault
# import nugflow.interfaces.airflow as af
# import nugflow.interfaces.geocoder as geocoder
# import nugflow.domain.vault.mart.alcohol.repository as repo
# import nugflow.domain.geo.transform as gt
#
#
# def mart_liquor_license(**context) -> None:
#     bootstrap()
#     repo.mart_liquor_license()
#
#
# def extract_address_geocodes(**context) -> typing.List[str]:
#     bootstrap()
#     df = repo.get_geocode_input()
#     paths = list(geocoder.process(df, af.get_work_dir(context)))
#     return paths
#
#
# def transform_address_geocodes(**context) -> typing.List[str]:
#     bootstrap()
#     output_paths = list()
#     work_dir = af.get_work_dir(context)
#     paths = af.get_last_task_xcom(context)
#     for i, path in enumerate(paths):
#         vault_data = gt.get_vault_geocode(path, context["ts"])
#         output_path = vault_data.to_csv(work_dir, i)
#         output_paths.append(output_path)
#     return output_paths
#
#
# def load_address_geocodes(**context) -> None:
#     src_paths = af.get_last_task_xcom(context)
#     bootstrap()
#     for src_path in src_paths:
#         print("Got src_path", src_path)
#         data = vault.VaultData.from_csv(src_path)
#         vault.stage(data)
#         vault.load(data)
#         vault.clean_stage()
#
#
# dag_id = __file__.rsplit("/", 1)[1].split(".")[0]
# dag = af.NugflowManualDAG(dag_id)
#
# with dag:
#     mll = af.NugflowOperator(mart_liquor_license)
#     e = af.NugflowOperator(extract_address_geocodes)
#     t = af.NugflowOperator(transform_address_geocodes)
#     l = af.NugflowOperator(load_address_geocodes)
#     mll >> e
#     e >> t
#     t >> l
