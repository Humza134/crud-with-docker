from sqlmodel import SQLModel,Field, Relationship
from datetime import datetime


# Todo model

class TodoBase(SQLModel):
    title: str = Field(index=True)
    description: str = Field(default=None, nullable=True)
    completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TodoUpdate(SQLModel):
    title: str | None = Field(default=None, nullable=True)
    description: str | None = Field(default=None, nullable=True)
    completed: bool | None = Field(default=None, nullable=True)
    updated_at: datetime | None = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
     


