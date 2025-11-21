"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# -------------------------------------------------------------------
# Portfolio-specific schemas
# -------------------------------------------------------------------

class Project(BaseModel):
    """
    Mobile developer project portfolio schema
    Collection name: "project"
    """
    title: str = Field(..., description="Project title")
    slug: str = Field(..., description="URL-friendly unique identifier")
    short_description: str = Field(..., description="One-liner summary")
    description: str = Field(..., description="Detailed description")
    platform: List[str] = Field(default_factory=list, description="e.g., iOS, Android, Flutter, React Native")
    tech_stack: List[str] = Field(default_factory=list, description="Technologies used")
    role: str = Field(..., description="Your role in the project")
    highlights: List[str] = Field(default_factory=list, description="Key achievements or features")
    repo_url: Optional[HttpUrl] = Field(None, description="Repository URL if public")
    live_url: Optional[HttpUrl] = Field(None, description="Live app or landing page URL")
    screenshots: List[HttpUrl] = Field(default_factory=list, description="Screenshot URLs")
    cover_image: Optional[HttpUrl] = Field(None, description="Cover image URL")
    year: Optional[int] = Field(None, description="Year of the project")
    featured: bool = Field(False, description="Whether to highlight on homepage")

class Testimonial(BaseModel):
    """
    Testimonials from clients or teammates
    Collection name: "testimonial"
    """
    author: str = Field(..., description="Person name")
    role: Optional[str] = Field(None, description="Author role or company")
    message: str = Field(..., description="Testimonial text")
    avatar_url: Optional[HttpUrl] = Field(None, description="Avatar image URL")

class ContactMessage(BaseModel):
    """
    Contact form submissions
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender name")
    email: str = Field(..., description="Sender email")
    subject: str = Field(..., description="Subject line")
    message: str = Field(..., description="Message body")

# Example schemas (kept for reference)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
