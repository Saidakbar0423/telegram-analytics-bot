from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    bio: Optional[str] = None
    is_bot: bool = False


class UserUpdate(BaseModel):
    """User update schema"""
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    last_seen: Optional[datetime] = None


class UserStats(BaseModel):
    """User statistics schema"""
    user_id: int
    username: Optional[str]
    message_count: int
    first_seen: datetime
    last_seen: Optional[datetime]
    active_groups: int


class UserResponse(UserBase):
    """User response schema"""
    id: int
    message_count: int
    first_seen: datetime
    last_seen: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# Group Schemas
class GroupBase(BaseModel):
    """Base group schema"""
    group_id: int
    name: str
    username: Optional[str] = None


class GroupCreate(GroupBase):
    """Group creation schema"""
    description: Optional[str] = None
    is_channel: bool = False


class GroupStats(BaseModel):
    """Group statistics schema"""
    group_id: int
    name: str
    username: Optional[str]
    message_count: int
    member_count: Optional[int]
    last_message_date: Optional[datetime]


class GroupResponse(GroupBase):
    """Group response schema"""
    id: int
    description: Optional[str]
    is_channel: bool
    message_count: int
    member_count: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# Message Schemas
class MessageBase(BaseModel):
    """Base message schema"""
    message_id: int
    user_id: int
    group_id: int
    text: Optional[str] = None


class MessageCreate(MessageBase):
    """Message creation schema"""
    message_date: datetime
    media_type: Optional[str] = None


class MessageResponse(MessageBase):
    """Message response schema"""
    id: int
    media_type: Optional[str]
    message_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class MessageSearch(BaseModel):
    """Message search schema"""
    query: str
    group_id: Optional[int] = None
    user_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=20, le=100)
    offset: int = Field(default=0, ge=0)


# Pagination Schemas
class PaginationParams(BaseModel):
    """Pagination parameters"""
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class PaginatedResponse(BaseModel):
    """Paginated response schema"""
    total: int
    limit: int
    offset: int
    data: list


# Authentication Schemas
class TokenRequest(BaseModel):
    """Token request schema"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Statistics Schemas
class TopUserStats(BaseModel):
    """Top user statistics"""
    user_id: int
    username: Optional[str]
    message_count: int
    rank: int


class KeywordStats(BaseModel):
    """Keyword statistics"""
    keyword: str
    frequency: int
    percentage: float


class ActivityHeatmap(BaseModel):
    """Activity heatmap data"""
    day: str
    hour: int
    count: int