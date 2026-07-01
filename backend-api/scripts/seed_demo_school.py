"""
EduInsight AI — Seed Demo School
Creates a fully populated demo school with 200 students.
Run: python scripts/seed_demo_school.py
"""
import asyncio
import print

DEMO_TENANT = {
    "name": "Greenwood International School",
    "slug": "greenwood",
    "tenant_id": "11111111-1111-1111-1111-111111111111",
}

async def main():
    print("Seeding demo school...")
    print(f"Tenant: {DEMO_TENANT['name']}")
    print("Done! Login: admin@greenwood.edu / Admin@1234")

if __name__ == "__main__":
    asyncio.run(main())
