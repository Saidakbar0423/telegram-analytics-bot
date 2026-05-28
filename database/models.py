from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    Float, Boolean, Index, ForeignKey, BigInteger, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Telegram user model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, nullable=True, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    is_bot = Column(Boolean, default=False)
    message_count = Column(Integer, default=0)
    last_seen = Column(DateTime, nullable=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    group_memberships = relationship("GroupMember", back_populates="user", cascade="all, delete-orphan")
    username_history = relationship("UsernameHistory", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_user_id_username", "user_id", "username"),
        Index("idx_last_seen", "last_seen"),
    )


class Group(Base):
    """Telegram group/channel model"""

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(BigInteger, unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    username = Column(String(255), nullable=True, unique=True, index=True)
    description = Column(Text, nullable=True)
    is_channel = Column(Boolean, default=False)
    is_forum = Column(Boolean, default=False)
    member_count = Column(Integer, nullable=True)
    message_count = Column(Integer, default=0)
    last_message_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = relationship("Message", back_populates="group", cascade="all, delete-orphan")
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_group_id_username", "group_id", "username"),
        Index("idx_last_message_date", "last_message_date"),
    )


class Message(Base):
    """Telegram message model"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(BigInteger, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False, index=True)
    group_id = Column(BigInteger, ForeignKey("groups.group_id"), nullable=False, index=True)
    text = Column(Text, nullable=True)
    media_type = Column(String(50), nullable=True)  # photo, video, document, etc.
    reply_to_message_id = Column(BigInteger, nullable=True)
    forward_from_user_id = Column(BigInteger, nullable=True)
    edit_date = Column(DateTime, nullable=True)
    message_date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="messages")
    group = relationship("Group", back_populates="messages")

    __table_args__ = (
        Index("idx_user_group_date", "user_id", "group_id", "message_date"),
        Index("idx_message_date", "message_date"),
    )


class GroupMember(Base):
    """Group member association"""

    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False, index=True)
    group_id = Column(BigInteger, ForeignKey("groups.group_id"), nullable=False, index=True)
    joined_date = Column(DateTime, default=datetime.utcnow)
    left_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="group_memberships")
    group = relationship("Group", back_populates="members")

    __table_args__ = (
        Index("idx_user_group", "user_id", "group_id"),
    )


class UsernameHistory(Base):
    """Track username changes"""

    __tablename__ = "username_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False, index=True)
    old_username = Column(String(255), nullable=True)
    new_username = Column(String(255), nullable=False, index=True)
    change_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="username_history")

    __table_args__ = (
        Index("idx_user_change_date", "user_id", "change_date"),
    )


class TrackedUsername(Base):
    """Track specific usernames for monitoring"""

    __tablename__ = "tracked_usernames"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(BigInteger, nullable=True, index=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    found = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ParserLog(Base):
    """Parser activity logs"""

    __tablename__ = "parser_logs"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(BigInteger, nullable=True, index=True)
    status = Column(String(50), nullable=False)  # success, error, rate_limit
    message = Column(Text, nullable=True)
    messages_collected = Column(Integer, default=0)
    errors = Column(JSON, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_status_date", "status", "created_at"),
    )


class Statistics(Base):
    """Pre-calculated statistics cache"""

    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    stat_type = Column(String(100), nullable=False)  # top_users, top_groups, keywords, etc.
    data = Column(JSON, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_stat_type_date", "stat_type", "calculated_at"),
    )