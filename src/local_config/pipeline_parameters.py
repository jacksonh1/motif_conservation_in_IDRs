import copy
from pathlib import Path
from typing import Any, Literal, Union

from attrs import asdict, define, field, validators

# from enum import Enum, auto
# class SearchMethod(Enum):
#     SEARCH = auto()
#     GIVEN_POSITIONS = auto()


@define
class HitSequenceConf:
    hit_sequence_search_method: Literal["search", "given_positions"] = field(
        default="search",
        validator=validators.in_(["search", "given_positions"]),
    )
    longest_common_subsequence: bool = field(default=False, converter=bool)
    lcs_min_length: int = field(default=20, converter=int)
    target_hit_length: int = field(default=0, converter=int)


@define
class IdrConf:
    find_idrs: bool = field(default=True, converter=bool)
    idr_map_file: str | Path | None = field(default=None)
    iupred_cutoff: float = field(
        default=0.4,
        converter=float,
        validator=validators.and_(validators.le(1), validators.ge(0))
    )
    gap_merge_threshold: int = field(default=10, converter=int)
    idr_min_length: int = field(default=8, converter=int)
    
    def __attrs_post_init__(self):
        if self.find_idrs:
            assert self.idr_map_file is None, "idr_map_file must not be provided if find_idrs is True. choose one"
        else:
            assert self.idr_map_file is not None, "idr_map_file must be provided if find_idrs is False"


@define
class MultiLevelPlotConf:
    score_key: str = field(default="property_entropy")
    output_folder: str | Path = field(default="plots")
    num_bg_scores_cutoff: int = field(default=20, converter=int) 


@define
class FilterConf:
    min_num_orthos: int = field(default=20, converter=int)


@define
class ScoreMethod:
    """
    TODO: Enum
    """
    score_key: str = field(default="property_entropy")
    score_kwargs: dict[str, Any] = field(factory=dict)

@define
class TableAnnotationConf:
    """
    """
    score_key_for_table: str = field(default="property_entropy")
    motif_regex: str|None = field(default=None)
    levels: list[str] = field(factory=list)

@define
class AlnSliceConf:
    """
    parameters for creating the slice of the MSA surrounding the hit sequence

    Parameters
    ----------
    col_flank : int
        number of columns in the alignment to flank the hit sequence with
    """
    n_flanking_cols: int = field(default=20, converter=int)    


@define
class PipelineParameters:
    """
    Parameters for the pipeline
    """

    database_filekey: str | Path
    table_file: str | Path
    precalculated_aln_conservation_score_keys: list[str] = field(factory=list)
    clear_files: bool = field(default=False, converter=bool)
    clean_analysis_files: bool = field(default=True, converter=bool)
    score_methods: list[ScoreMethod] = field(factory=list)
    output_folder: str | Path = field(default="conservation_analysis")
    hit_sequence_params: HitSequenceConf = field(default=HitSequenceConf())
    idr_params: IdrConf = field(default=IdrConf())
    filter_params: FilterConf = field(default=FilterConf())
    multilevel_plot_params: MultiLevelPlotConf = field(default=MultiLevelPlotConf())
    aln_slice_params: AlnSliceConf = field(default=AlnSliceConf())
    table_annotation_params: TableAnnotationConf = field(default=TableAnnotationConf())
    
    @classmethod
    def from_dict(cls, d: dict[str, Any]):
        d = copy.deepcopy(d)
        return cls(
            hit_sequence_params=HitSequenceConf(**d.pop("hit_sequence_params", {})),
            idr_params=IdrConf(**d.pop("idr_params", {})),
            filter_params=FilterConf(**d.pop("filter_params", {})),
            score_methods=[ScoreMethod(k, v) for k,v in d.pop("new_score_methods", {}).items()],
            multilevel_plot_params=MultiLevelPlotConf(**d.pop("multilevel_plot_params", {})),
            table_annotation_params=TableAnnotationConf(**d.pop("table_annotation_params", {})),
            **d
        )
    
    def __attrs_post_init__(self):
        if not Path(self.table_file).exists():
            raise FileNotFoundError(f"table_file {self.table_file} does not exist")
        if not Path(self.database_filekey).exists():
            raise FileNotFoundError(f"database_filekey {self.database_filekey} does not exist")






# print(test["new_score_methods"])


test = {
    "output_folder": "./ortholog_analysis",
    "database_filekey": "../../data/example_orthogroup_database_merged_version/human_odb_groups/database_key.json",
    "table_file": "../../examples/table_annotation/table.csv",
    # "hit_sequence_params": {
        # "hit_sequence_search_method": "search"
    # },
    "idr_params": {
        "find_idrs": True,
        # idr_map_file: "./idr_map.json"
        "iupred_cutoff": 0.4,
        "gap_merge_threshold": 10,
        "idr_min_length": 8,
    },
    "filter_params": {
        "min_num_orthos": 20
    },

    "precalculated_aln_conservation_score_keys": [
        "property_entropy",
    ],
    "new_score_methods": {
        "property_entropy":{
            "matrix_name": "EDSSMat50_max_off_diagonal_norm",
            "gap_frac_cutoff": 0.2
        },
    },
    "clear_files": False
}
# test2 = {
#     "output_folder": "./ortholog_analysis",
#     "database_filekey": "../../data/example_orthogroup_database/human_odb_groups/database_key.json",
#     "table_file": "./table.csv",
#     "hit_sequence_params": {
#         "hit_sequence_search_method": "search"
#     },
#     "idr_params": {
#         "find_idrs": True,
#         # idr_map_file: "./idr_map.json"
#         "iupred_cutoff": 0.4,
#         "gap_merge_threshold": 10,
#         "idr_min_length": 8,
#     },
#     "filter_params": {
#         "min_num_orthos": 20
#     },
#     "new_score_methods": {
#         "property_entropy":{
#             "matrix_name": "EDSSMat50_max_off_diagonal_norm",
#             "gap_frac_cutoff": 0.2
#         },
#     },
#     "clear_files": False
# }

# config = PipelineParameters.from_dict(test)
# for k, v in asdict(config).items():
#     print(k, v)

# config.precalculated_aln_conservation_score_keys.append("test")


# config2 = PipelineParameters.from_dict(test)
# for k, v in asdict(config2).items():
#     print(k, v)


# config = PipelineParameters.from_dict(test2)
# for k, v in asdict(config).items():
    # print(k, v)