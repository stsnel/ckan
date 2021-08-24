# -*- coding: utf-8 -*-

from typing import (
    Any, Dict, List, Optional, Tuple, Union
)
from typing_extensions import TypeAlias

from ..model import Query, Model

###############################################################################
#                                     get                                     #
###############################################################################
PackageList = List[str]
CurrentPackageListWithResources = List[Dict[str, Any]]
MemberList = List[Tuple[Any, ...]]
PackageCollaboratorList = List[Dict[str, Any]]
PackageCollaboratorListForUser = PackageCollaboratorList
GroupList = List[Dict[str, Any]]
OrganizationList = List[Dict[str, Any]]
GroupListAuthz = List[Dict[str, Any]]
OrganizationListForUser = List[Dict[str, Any]]
LicenseList = List[Dict[str, Any]]
TagList = Union[List[Dict[str, Any]], List[str]]
UserList = Union[List[Dict[str, Any]], List[str], "Query[Model.User]"]
PackageRelationshipsList = List[Dict[str, Any]]
PackageShow = Dict[str, Any]
ResourceShow = Dict[str, Any]
ResourceViewShow = Dict[str, Any]
ResourceViewList = List[Dict[str, Any]]
GroupShow = Dict[str, Any]
OrganizationShow = Dict[str, Any]
GroupPackageShow = List[Dict[str, Any]]
TagShow = Dict[str, Any]
UserShow = Dict[str, Any]
PackageAutocomplete = List[Dict[str, Any]]
FormatAutocomplete = List[str]
UserAutocomplete = List[Dict[str, Any]]
GroupAutocomplete = List[Dict[str, Any]]
OrganizationAutocomplete = List[Dict[str, Any]]
PackageSearch = Dict[str, Any]
ResourceSearch = Dict[str, Any]
TagSearch = Dict[str, Any]
TagAutocomplete = List[str]
TaskStatusShow = Dict[str, Any]
TermTranslationShow = List[Dict[str, Any]]
GetSiteUser = Dict[str, Any]
StatusShow = Dict[str, Any]
VocabularyList = List[Dict[str, Any]]
VocabularyShow = Dict[str, Any]
UserActivityList = List[Dict[str, Any]]
PackageActivityList = List[Dict[str, Any]]
GroupActivityList = List[Dict[str, Any]]
OrganizationActivityList = List[Dict[str, Any]]
RecentlyChangedPackagesActivityList = List[Dict[str, Any]]
UserFollowerCount = int
DatasetFollowerCount = int
GroupFollowerCount = int
OrganizationFollowerCount = int
UserFollowerList = List[Dict[str, Any]]
DatasetFollowerList = List[Dict[str, Any]]
GroupFollowerList = List[Dict[str, Any]]
OrganizationFollowerList = List[Dict[str, Any]]
AmFollowingUser = bool
AmFollowingDataset = bool
AmFollowingGroup = bool
FolloweeCount = int
UserFolloweeCount = int
DatasetFolloweeCount = int
GroupFolloweeCount = int
FolloweeList = List[Dict[str, Any]]
UserFolloweeList = List[Dict[str, Any]]
DatasetFolloweeList = List[Dict[str, Any]]
GroupFolloweeList = List[Dict[str, Any]]
OrganizationFolloweeList = List[Dict[str, Any]]
DashboardActivityList = List[Dict[str, Any]]
DashboardNewActivitiesCount = int
ActivityShow = Dict[str, Any]
ActivityDataShow = Dict[str, Any]
ActivityDiff = Dict[str, Any]
MemberRolesList = List[Dict[str, Any]]
HelpShow = Optional[str]
ConfigOptionShow = Any
ConfigOptionList = List[str]
JobList = List[Dict[str, Any]]
JobShow = Dict[str, Any]
ApiTokenList = List[Dict[str, Any]]

###############################################################################
#                                    create                                   #
###############################################################################
PackageCreate = Union[Dict[str, Any], str]
ResourceCreate = Dict[str, Any]
ResourceViewCreate = Dict[str, Any]
ResourceCreateDefaultResourceViews = List[Dict[str, Any]]
PackageCreateDefaultResourceViews = List[Dict[str, Any]]
PackageRelationshipCreate = Dict[str, Any]
MemberCreate = Dict[str, Any]
PackageCollaboratorCreate = Dict[str, Any]
GroupCreate = Union[str, Dict[str, Any]]
OrganizationCreate = Union[str, Dict[str, Any]]
UserCreate = Dict[str, Any]
UserInvite = Dict[str, Any]
VocabularyCreate = Dict[str, Any]
ActivityCreate = Optional[Dict[str, Any]]
TagCreate = Dict[str, Any]
FollowUser = Dict[str, Any]
FollowDataset = Dict[str, Any]
GroupOrOrgMemberCreate = Dict[str, Any]
GroupMemberCreate = Dict[str, Any]
OrganizationMemberCreate = Dict[str, Any]
FollowGroup = Dict[str, Any]
ApiTokenCreate = Dict[str, Any]

###############################################################################
#                                    delete                                   #
###############################################################################
UserDelete: TypeAlias = None
PackageDelete: TypeAlias = None
DatasetPurge: TypeAlias = None
ResourceDelete: TypeAlias = None
ResourceViewDelete: TypeAlias = None
ResourceViewClear: TypeAlias = None
PackageRelationshipDelete: TypeAlias = None
MemberDelete: TypeAlias = None
PackageCollaboratorDelete: TypeAlias = None
GroupDelete: TypeAlias = None
OrganizationDelete: TypeAlias = None
ApiTokenRevoke: TypeAlias = None

###############################################################################
#                                    patch                                    #
###############################################################################
PackagePatch = Union[str, Dict[str, Any]]
ResourcePatch = Dict[str, Any]
GroupPatch = Dict[str, Any]
OrganizationPatch = Dict[str, Any]
UserPatch = Dict[str, Any]

###############################################################################
#                                    update                                   #
###############################################################################
ResourceUpdate = Dict[str, Any]
ResourceViewUpdate = Dict[str, Any]
ResourceViewReorder = Dict[str, Any]
PackageUpdate = Union[str, Dict[str, Any]]
ConfigOptionUpdate = Dict[str, Any]
PackageRevise = Dict[str, Any]
PackageResourceReorder = Dict[str, Any]
PackageRelationshipUpdate = Dict[str, Any]
GroupUpdate = Dict[str, Any]
OrganizationUpdate = Dict[str, Any]
UserUpdate = Dict[str, Any]
UserGenerateApikey = Dict[str, Any]
TaskStatusUpdate = Dict[str, Any]
TaskStatusUpdateMany = Dict[str, Any]
TermTranslationUpdate = Dict[str, Any]
TermTranslationUpdateMany = Dict[str, Any]
VocabularyUpdate = Dict[str, Any]
DashboardMarkActivitiesOld: TypeAlias = None
SendEmailNotifications: TypeAlias = None
PackageOwnerOrgUpdate: TypeAlias = None
BulkUpdatePrivate: TypeAlias = None
BulkUpdatePublic: TypeAlias = None
BulkUpdateDelete: TypeAlias = None
