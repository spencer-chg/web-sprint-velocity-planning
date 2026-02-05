"""
Migration script to import historical sprint data into Supabase
Run once: python migrate_historical_data.py
"""

from supabase import create_client

# Supabase connection
SUPABASE_URL = "https://iwarvepodaijjofyyvvm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3YXJ2ZXBvZGFpampvZnl5dnZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzMDQyOTksImV4cCI6MjA4NTg4MDI5OX0.z9c_aYcY53G7Id3FSyNgrheNtKVWlSt5EGaoM-wAMWc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Historical sprint data from original JSX file
HISTORICAL_SPRINTS = [
    {"sprintId":"2025-S01","sprintName":"Suttungr","startDate":"2025-09-10","endDate":"2025-09-23","sprintDays":10,"assignments":[{"engineerId":"fredrik-svensson","teamId":"storyblok","storyPoints":1,"totalPtoDays":0.25},{"engineerId":"fredrik-svensson","teamId":"team1","storyPoints":1,"totalPtoDays":0.25},{"engineerId":"stephen-corry","teamId":"storyblok","storyPoints":6,"totalPtoDays":0},{"engineerId":"stephen-corry","teamId":"team2","storyPoints":0.5,"totalPtoDays":0},{"engineerId":"cody-worthen","teamId":"team1","storyPoints":19,"totalPtoDays":0},{"engineerId":"fernando-fernandez","teamId":"team1","storyPoints":7,"totalPtoDays":0},{"engineerId":"fernando-fernandez","teamId":"team2","storyPoints":0.5,"totalPtoDays":0},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":7,"totalPtoDays":0},{"engineerId":"jaime-virrueta","teamId":"team1","storyPoints":1,"totalPtoDays":0},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":2.5,"totalPtoDays":0},{"engineerId":"brady-hession","teamId":"team2","storyPoints":2,"totalPtoDays":0},{"engineerId":"tom-sharrock","teamId":"team2","storyPoints":9,"totalPtoDays":2}]},
    {"sprintId":"2025-S02","sprintName":"Thyone","startDate":"2025-09-24","endDate":"2025-10-07","sprintDays":10,"assignments":[{"engineerId":"fredrik-svensson","teamId":"storyblok","storyPoints":2,"totalPtoDays":0},{"engineerId":"stephen-corry","teamId":"storyblok","storyPoints":8.5,"totalPtoDays":0.5},{"engineerId":"stephen-corry","teamId":"team2","storyPoints":1,"totalPtoDays":0.5},{"engineerId":"cody-worthen","teamId":"team1","storyPoints":13,"totalPtoDays":0},{"engineerId":"fernando-fernandez","teamId":"team1","storyPoints":9,"totalPtoDays":0},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":3,"totalPtoDays":3},{"engineerId":"brady-hession","teamId":"team2","storyPoints":0.5,"totalPtoDays":0},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":1.5,"totalPtoDays":0},{"engineerId":"tom-sharrock","teamId":"team2","storyPoints":1,"totalPtoDays":0}]},
    {"sprintId":"2025-S03","sprintName":"Ursa Minor","startDate":"2025-10-08","endDate":"2025-10-21","sprintDays":10,"assignments":[{"engineerId":"fredrik-svensson","teamId":"storyblok","storyPoints":2.5,"totalPtoDays":0},{"engineerId":"fredrik-svensson","teamId":"team1","storyPoints":0.5,"totalPtoDays":0},{"engineerId":"stephen-corry","teamId":"storyblok","storyPoints":5,"totalPtoDays":0},{"engineerId":"cody-worthen","teamId":"team1","storyPoints":9,"totalPtoDays":3.5},{"engineerId":"fernando-fernandez","teamId":"team1","storyPoints":5,"totalPtoDays":1},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":4,"totalPtoDays":0},{"engineerId":"brady-hession","teamId":"team2","storyPoints":8,"totalPtoDays":1},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":1,"totalPtoDays":0},{"engineerId":"tom-sharrock","teamId":"team2","storyPoints":7,"totalPtoDays":0}]},
    {"sprintId":"2025-S04","sprintName":"Vega","startDate":"2025-10-22","endDate":"2025-11-04","sprintDays":10,"assignments":[{"engineerId":"stephen-corry","teamId":"storyblok","storyPoints":2,"totalPtoDays":1},{"engineerId":"cody-worthen","teamId":"team1","storyPoints":12.5,"totalPtoDays":0},{"engineerId":"fernando-fernandez","teamId":"team1","storyPoints":5.5,"totalPtoDays":1},{"engineerId":"fredrik-svensson","teamId":"team1","storyPoints":2.5,"totalPtoDays":1.5},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":2,"totalPtoDays":0},{"engineerId":"brady-hession","teamId":"team2","storyPoints":6,"totalPtoDays":1},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":2.5,"totalPtoDays":0},{"engineerId":"tom-sharrock","teamId":"team2","storyPoints":10.5,"totalPtoDays":0}]},
    {"sprintId":"2025-S05","sprintName":"Wendelinefroger","startDate":"2025-11-05","endDate":"2025-11-18","sprintDays":10,"assignments":[{"engineerId":"cody-worthen","teamId":"team1","storyPoints":11,"totalPtoDays":0},{"engineerId":"fernando-fernandez","teamId":"team1","storyPoints":8,"totalPtoDays":0},{"engineerId":"fredrik-svensson","teamId":"team1","storyPoints":3,"totalPtoDays":0},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":7,"totalPtoDays":0},{"engineerId":"brady-hession","teamId":"team2","storyPoints":4.5,"totalPtoDays":1},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":5.5,"totalPtoDays":0},{"engineerId":"stephen-corry","teamId":"team2","storyPoints":3,"totalPtoDays":3.25},{"engineerId":"tom-sharrock","teamId":"team2","storyPoints":12.5,"totalPtoDays":0}]},
    {"sprintId":"2025-S06","sprintName":"Xosa","startDate":"2025-11-19","endDate":"2025-12-02","sprintDays":10,"assignments":[{"engineerId":"cody-worthen","teamId":"storyblok","storyPoints":14,"totalPtoDays":1},{"engineerId":"cody-worthen","teamId":"team1","storyPoints":6.5,"totalPtoDays":1},{"engineerId":"tom-sharrock","teamId":"storyblok","storyPoints":3,"totalPtoDays":3.5},{"engineerId":"tom-sharrock","teamId":"team2","storyPoints":1,"totalPtoDays":3.5},{"engineerId":"fredrik-svensson","teamId":"team1","storyPoints":3,"totalPtoDays":3},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":1.5,"totalPtoDays":5},{"engineerId":"brady-hession","teamId":"team2","storyPoints":5.5,"totalPtoDays":2},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":3,"totalPtoDays":2},{"engineerId":"stephen-corry","teamId":"team2","storyPoints":8.5,"totalPtoDays":4}]},
    {"sprintId":"2025-S07","sprintName":"Yeungchuchiu","startDate":"2025-12-03","endDate":"2025-12-16","sprintDays":10,"assignments":[{"engineerId":"cody-worthen","teamId":"storyblok","storyPoints":0.5,"totalPtoDays":0.75},{"engineerId":"cody-worthen","teamId":"team1","storyPoints":0.5,"totalPtoDays":0.75},{"engineerId":"tom-sharrock","teamId":"storyblok","storyPoints":2,"totalPtoDays":7},{"engineerId":"fernando-fernandez","teamId":"team1","storyPoints":5.5,"totalPtoDays":1},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":3.5,"totalPtoDays":1},{"engineerId":"brady-hession","teamId":"team2","storyPoints":4,"totalPtoDays":0},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":5,"totalPtoDays":0},{"engineerId":"stephen-corry","teamId":"team2","storyPoints":1,"totalPtoDays":3}]},
    {"sprintId":"2025-S08","sprintName":"Zaurak","startDate":"2025-12-17","endDate":"2025-12-31","sprintDays":10,"assignments":[{"engineerId":"fredrik-svensson","teamId":"team1","storyPoints":5,"totalPtoDays":0},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":0.5,"totalPtoDays":5},{"engineerId":"brady-hession","teamId":"team2","storyPoints":1,"totalPtoDays":8},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":1,"totalPtoDays":6},{"engineerId":"tom-sharrock","teamId":"team2","storyPoints":3,"totalPtoDays":8}]},
    {"sprintId":"2025-S09","sprintName":"Amazing Spiderman","startDate":"2025-12-31","endDate":"2026-01-13","sprintDays":10,"assignments":[{"engineerId":"cody-worthen","teamId":"storyblok","storyPoints":20,"totalPtoDays":0.5},{"engineerId":"stephen-corry","teamId":"storyblok","storyPoints":4.5,"totalPtoDays":1},{"engineerId":"tom-sharrock","teamId":"storyblok","storyPoints":5.5,"totalPtoDays":1.5},{"engineerId":"cody-worthen","teamId":"team1","storyPoints":1,"totalPtoDays":0.5},{"engineerId":"tom-sharrock","teamId":"team2","storyPoints":1,"totalPtoDays":1.5},{"engineerId":"fernando-fernandez","teamId":"team1","storyPoints":3,"totalPtoDays":2},{"engineerId":"fredrik-svensson","teamId":"team1","storyPoints":7,"totalPtoDays":0},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":7.5,"totalPtoDays":1},{"engineerId":"brady-hession","teamId":"team2","storyPoints":12.5,"totalPtoDays":2},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":1.5,"totalPtoDays":0}]},
    {"sprintId":"2025-S10","sprintName":"Bizarro","startDate":"2026-01-14","endDate":"2026-01-27","sprintDays":10,"assignments":[{"engineerId":"fernando-fernandez","teamId":"team1","storyPoints":10,"totalPtoDays":2},{"engineerId":"matthew-callison","teamId":"team1","storyPoints":4,"totalPtoDays":1},{"engineerId":"matthew-callison","teamId":"team2","storyPoints":1,"totalPtoDays":0},{"engineerId":"brady-hession","teamId":"team2","storyPoints":1,"totalPtoDays":1},{"engineerId":"jaime-virrueta","teamId":"team2","storyPoints":1,"totalPtoDays":2}]}
]

# Default team assignments
DEFAULT_TEAM_ASSIGNMENTS = {
    "fredrik-svensson": "team1",
    "fernando-fernandez": "team1",
    "matthew-callison": "team1",
    "cody-worthen": "team1",
    "stephen-corry": "team2",
    "tom-sharrock": "team2",
    "brady-hession": "team2",
    "jaime-virrueta": "team2"
}

def migrate_sprints():
    """Insert historical sprint data into Supabase"""
    print("Starting migration of historical sprint data...")

    success_count = 0
    skip_count = 0
    error_count = 0

    for sprint in HISTORICAL_SPRINTS:
        try:
            # Check if sprint already exists
            existing = supabase.table("sprints").select("sprint_id").eq("sprint_id", sprint["sprintId"]).execute()

            if existing.data:
                print(f"  ⏭️  Skipping '{sprint['sprintName']}' - already exists")
                skip_count += 1
                continue

            # Insert sprint
            supabase.table("sprints").insert({
                "sprint_id": sprint["sprintId"],
                "sprint_name": sprint["sprintName"],
                "start_date": sprint["startDate"],
                "end_date": sprint["endDate"],
                "sprint_days": sprint["sprintDays"]
            }).execute()

            # Insert assignments
            for assignment in sprint["assignments"]:
                supabase.table("sprint_assignments").insert({
                    "sprint_id": sprint["sprintId"],
                    "engineer_id": assignment["engineerId"],
                    "team_id": assignment["teamId"],
                    "story_points": assignment["storyPoints"],
                    "pto_days": assignment["totalPtoDays"]
                }).execute()

            print(f"  ✅ Migrated '{sprint['sprintName']}' ({len(sprint['assignments'])} assignments)")
            success_count += 1

        except Exception as e:
            print(f"  ❌ Error migrating '{sprint['sprintName']}': {e}")
            error_count += 1

    print(f"\n{'='*50}")
    print(f"Migration complete!")
    print(f"  ✅ Migrated: {success_count}")
    print(f"  ⏭️  Skipped: {skip_count}")
    print(f"  ❌ Errors: {error_count}")

def migrate_team_assignments():
    """Insert default team assignments into Supabase"""
    print("\nMigrating team assignments...")

    for engineer_id, team_id in DEFAULT_TEAM_ASSIGNMENTS.items():
        try:
            supabase.table("team_assignments").upsert({
                "engineer_id": engineer_id,
                "team_id": team_id
            }).execute()
            print(f"  ✅ {engineer_id} → {team_id}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

    print("Team assignments migrated!")

if __name__ == "__main__":
    migrate_sprints()
    migrate_team_assignments()
    print("\n🎉 All done! Your historical data is now in Supabase.")
