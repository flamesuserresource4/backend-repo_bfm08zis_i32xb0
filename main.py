import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import db, create_document, get_documents
from schemas import Project, Testimonial, ContactMessage

app = FastAPI(title="Mobile Dev Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Portfolio API ready"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# -----------------------------
# Portfolio Endpoints
# -----------------------------

@app.get("/api/projects", response_model=List[Project])
def list_projects():
    docs = get_documents("project", {}, limit=None) if db else []
    # Pydantic will validate/serialize
    return [Project(**{k: v for k, v in doc.items() if k != "_id"}) for doc in docs]

@app.get("/api/projects/featured", response_model=List[Project])
def list_featured_projects():
    docs = get_documents("project", {"featured": True}, limit=8) if db else []
    return [Project(**{k: v for k, v in doc.items() if k != "_id"}) for doc in docs]

@app.get("/api/projects/{slug}", response_model=Project)
def get_project(slug: str):
    docs = get_documents("project", {"slug": slug}, limit=1) if db else []
    if not docs:
        raise HTTPException(status_code=404, detail="Project not found")
    doc = docs[0]
    return Project(**{k: v for k, v in doc.items() if k != "_id"})

@app.post("/api/contact")
def submit_contact(message: ContactMessage):
    if db is None:
        return {"status": "ok", "stored": False}
    _id = create_document("contactmessage", message)
    return {"status": "ok", "stored": True, "id": _id}

@app.get("/api/testimonials", response_model=List[Testimonial])
def get_testimonials():
    docs = get_documents("testimonial", {}, limit=12) if db else []
    return [Testimonial(**{k: v for k, v in doc.items() if k != "_id"}) for doc in docs]

# Seed helper for demo if DB empty
class SeedResponse(BaseModel):
    inserted: int

@app.post("/api/seed", response_model=SeedResponse)
def seed_demo_data():
    if db is None:
        return SeedResponse(inserted=0)
    existing = get_documents("project", {}, limit=1)
    if existing:
        return SeedResponse(inserted=0)

    samples: List[Project] = [
        Project(
            title="Habit Hero",
            slug="habit-hero",
            short_description="Gamified habit tracker with streaks and rewards",
            description="A mobile app that helps users build habits using streaks, badges, and a playful mascot.",
            platform=["iOS", "Android", "Flutter"],
            tech_stack=["Flutter", "Dart", "Firebase", "Riverpod"],
            role="Lead Mobile Developer",
            highlights=["Realtime sync", "Widget support", "App Clip"],
            repo_url=None,
            live_url="https://example.com/habit-hero",
            screenshots=[],
            cover_image="https://images.unsplash.com/photo-1557690265-0d5fd7f9c2a5?q=80&w=1600&auto=format&fit=crop",
            year=2024,
            featured=True,
        ),
        Project(
            title="FitFriends",
            slug="fitfriends",
            short_description="Group workouts, challenges, and leaderboards",
            description="Social fitness app with squads, weekly challenges, and GPS run tracking.",
            platform=["iOS", "Android", "React Native"],
            tech_stack=["React Native", "TypeScript", "Expo", "Supabase"],
            role="Mobile Engineer",
            highlights=["Background GPS", "Offline-first", "Push notifications"],
            live_url="https://example.com/fitfriends",
            cover_image="https://images.unsplash.com/photo-1541532713592-79a0317b6b77?q=80&w=1600&auto=format&fit=crop",
            year=2023,
            featured=True,
        )
    ]

    inserted = 0
    for p in samples:
        create_document("project", p)
        inserted += 1

    create_document("testimonial", Testimonial(author="CEO, HealthCo", role="Client", message="Outstanding delivery and attention to detail.").model_dump())
    return SeedResponse(inserted=inserted)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
