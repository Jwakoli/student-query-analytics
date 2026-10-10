
from datetime import datetime, timedelta
from database import init_db, get_connection

# Create the database and table if they do not exist.
init_db()

departments = [
    "ICT",
    "Finance",
    "Admissions",
    "Student Affairs",
    "Academic Affairs",
]

categories = [
    "Technical Issue",
    "Registration",
    "Finance",
    "Academic",
    "Facilities",
]

priorities = ["Low", "Medium", "High", "Urgent"]

# A balanced mix of statuses for meaningful analytics.
statuses = (
    ["Resolved"] * 15
    + ["Pending"] * 9
    + ["In Progress"] * 6
)

now = datetime.now()
connection = get_connection()

try:
    cursor = connection.cursor()

    # Remove only records created by this sample-data script.
    cursor.execute(
        "DELETE FROM queries WHERE student_name LIKE 'SAMPLE DATA - Student %'"
    )

    for i in range(30):
        created_at = now - timedelta(
            days=(i * 7) % 30,
            hours=(i * 3) % 24,
        )

        status = statuses[i]
        resolved_at = None

        if status == "Resolved":
            resolved_at = created_at + timedelta(
                hours=2 + (i % 48)
            )

        student_name = f"SAMPLE DATA - Student {i + 1:02d}"
        title = f"Demo query {i + 1:02d}"

        description = (
            f"Fictional demonstration query number {i + 1}. "
            "This record is sample data for dashboard testing."
        )

        category = categories[i % len(categories)]
        department = departments[(i * 2) % len(departments)]
        priority = priorities[i % len(priorities)]

        cursor.execute(
            """
            INSERT INTO queries (
                student_name,
                title,
                description,
                category,
                department,
                priority,
                status,
                created_at,
                resolved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_name,
                title,
                description,
                category,
                department,
                priority,
                status,
                created_at.strftime("%Y-%m-%d %H:%M:%S"),
                (
                    resolved_at.strftime("%Y-%m-%d %H:%M:%S")
                    if resolved_at
                    else None
                ),
            ),
        )

    connection.commit()
    print("Success! Added 30 sample queries.")
    print("Your existing non-sample queries were preserved.")

finally:
    connection.close()
