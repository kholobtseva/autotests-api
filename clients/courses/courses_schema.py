from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema


class CourseBaseSchema(BaseModel):
    """Base schema with common course fields"""
    model_config = ConfigDict(populate_by_name=True)

    title: str
    max_score: int = Field(alias="maxScore", default=0)
    min_score: int = Field(alias="minScore", default=0)
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class CourseSchema(CourseBaseSchema):
    """Full course schema (API response)"""
    id: str
    preview_file: FileSchema = Field(alias="previewFile")
    created_by_user: UserSchema = Field(alias="createdByUser")


class CreateCourseRequestSchema(CourseBaseSchema):
    """Request schema for course creation"""
    preview_file_id: str = Field(alias="previewFileId")
    created_by_user_id: str = Field(alias="createdByUserId")


class CreateCourseResponseSchema(BaseModel):
    """Response schema after course creation"""
    course: CourseSchema


class UpdateCourseRequestSchema(BaseModel):
    """Request schema for course update"""
    model_config = ConfigDict(populate_by_name=True)

    title: Optional[str] = None
    max_score: Optional[int] = Field(alias="maxScore", default=0)
    min_score: Optional[int] = Field(alias="minScore", default=0)
    description: Optional[str] = None
    estimated_time: Optional[str] = Field(alias="estimatedTime", default=None)


class GetCoursesQuerySchema(BaseModel):
    """Query params for courses list"""
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias="userId")