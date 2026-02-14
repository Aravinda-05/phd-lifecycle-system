app_name = "phd_management"
app_title = "PhD Management"
app_publisher = "DevOps Group"
app_description = "PhD Lifecycle Management System"
app_email = "devops@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/phd_management/css/phd_management.css"
# app_include_js = "/assets/phd_management/js/phd_management.js"

fixtures = [
    "Workflow State",
    "Role",
    "Workflow"
]

scheduler_events = {
    "daily": [
        "phd_management.tasks.check_at_risk_students"
    ]
}
