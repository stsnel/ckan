# -*- coding: utf-8 -*-

from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
    TYPE_CHECKING,
)

from typing_extensions import Protocol, TypedDict, TypeAlias
from blinker import Signal
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.orm import Query

if TYPE_CHECKING:
    import ckan.model as model_


AlchemySession = ScopedSession
Query = Query
Model: TypeAlias = "model_"

Config = Dict[str, Union[str, Mapping[str, str]]]
CKANApp = Any

# dictionary passed to actions
DataDict = Dict[str, Any]
# dictionary passed to the ValidationError
ErrorDict = Dict[str, Union[int, str, List[Union[str, Dict[str, Any]]]]]

FlattenKey = Tuple[Any, ...]
FlattenDataDict = Dict[FlattenKey, Any]
FlattenErrorDict = Dict[FlattenKey, List[str]]

SignalMapping = Dict[Signal, Iterable[Union[Any, Dict[str, Any]]]]


class Context(TypedDict, total=False):
    """Mutable private dictionary passed along through many layers of code.

    Used for all sorts of questionable parameter passing and global state
    sharing.  We're trying to *not* add to this dictionary and use normal
    parameters instead.  Bonus points for anything that can be removed from
    here.
    """
    user: str
    model: Model
    session: AlchemySession

    __auth_user_obj_checked: bool
    __auth_audit: List[Tuple[str, int]]
    auth_user_obj: Optional["model_.User"]
    user_obj: "model_.User"

    schema_keys: List[Any]
    revision_id: Optional[Any]
    revision_date: Optional[Any]

    connection: Any
    check_access: Callable[..., Any]

    id: str
    user_id: str
    user_is_admin: bool
    search_query: bool
    return_query: bool
    return_minimal: bool
    return_id_only: bool
    defer_commit: bool
    reset_password: bool
    save: bool
    active: bool
    allow_partial_update: bool
    for_update: bool
    for_edit: bool
    for_view: bool
    ignore_auth: bool
    preview: bool
    allow_state_change: bool
    is_member: bool
    use_cache: bool
    include_plugin_extras: bool
    message: str

    keep_email: bool
    keep_apikey: bool
    skip_validation: bool
    validate: bool
    count_private_and_draft_datasets: bool

    schema: "Schema"
    group: "model_.Group"
    package: "model_.Package"
    vocabulary: "model_.Vocabulary"
    tag: "model_.Tag"
    activity: "model_.Activity"
    task_status: "model_.TaskStatus"
    resource: "model_.Resource"
    resource_view: "model_.ResourceView"
    relationship: "model_.PackageRelationship"
    api_version: int
    dataset_counts: Dict[str, Any]
    limits: Dict[str, Any]
    metadata_modified: str
    with_capacity: bool

    table_names: List[str]


class AuthResult(TypedDict, total=False):
    """Result of any access check
    """
    success: bool
    msg: Optional[str]


# Simplest validator that accepts only validated value.
ValueValidator = Callable[[Any], Any]
# Validator that accepts validation context alongside with the value.
ContextValidator = Callable[[Any, Context], Any]
# Complex validator that has access the whole validated dictionary.
DataValidator = Callable[
    [FlattenKey, FlattenDataDict, FlattenErrorDict, Context], None]

Validator = Union[ValueValidator, ContextValidator, DataValidator]
ValidatorFactory = Callable[..., Validator]

Schema = Dict[str, Union[List[Validator], "Schema"]]

# Function that accepts arbitary number of validators(decorated by
# ckan.logic.schema.validator_args) and returns Schema dictionary
ComplexSchemaFunc = Callable[..., Schema]
# ComplexSchemaFunc+validator_args decorator = function that accepts no args
# and returns Schema dictionary
PlainSchemaFunc = Callable[[], Schema]

AuthFunctionWithOptionalDataDict = Callable[
    [Context, Optional[DataDict]], AuthResult
]
AuthFunctionWithMandatoryDataDict = Callable[[Context, DataDict], AuthResult]
AuthFunction = Union[
    AuthFunctionWithOptionalDataDict,
    AuthFunctionWithMandatoryDataDict,
    'partial[AuthResult]',
]
ChainedAuthFunction = Callable[
    [AuthFunction, Context, Optional[DataDict]], AuthResult
]

Action = Callable[[Context, DataDict], Any]
ChainedAction = Callable[[Action, Context, DataDict], Any]


class PFeed(Protocol):
    """Contract for IFeed.get_feed_class
    """

    def __init__(
        self,
        feed_title: str,
        feed_link: str,
        feed_description: str,
        language: Optional[str],
        author_name: Optional[str],
        feed_guid: Optional[str],
        feed_url: Optional[str],
        previous_page: Optional[str],
        next_page: Optional[str],
        first_page: Optional[str],
        last_page: Optional[str],
    ) -> None:
        ...

    def add_item(self, **kwargs: Any) -> None:
        ...

    def writeString(self, encoding: str) -> str:
        ...


class PUploader(Protocol):
    """Contract for IUploader.get_uploader
    """

    def __init__(
        self, object_type: str, old_filename: Optional[str] = None
    ) -> None:
        ...

    def upload(self, max_size: int = ...) -> None:
        ...

    def update_data_dict(
        self,
        data_dict: Dict[str, Any],
        url_field: str,
        file_field: str,
        clear_field: str,
    ) -> None:
        ...


class PResourceUploader(Protocol):
    """Contract for IUploader.get_uploader
    """

    mimetype: Optional[str]
    filesize: int

    def __init__(self, resource: Dict[str, Any]) -> None:
        ...

    def get_path(self, id: str) -> str:
        ...

    def upload(self, id: str, max_size: int = ...) -> None:
        ...
