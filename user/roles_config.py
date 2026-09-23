ROLES_CONFIG = {
    "Admin": [
        # User & auth
        "add_user", "change_user", "delete_user", "view_user",
        "add_group", "change_group", "delete_group", "view_group",
        "add_permission", "change_permission", "delete_permission", "view_permission",

        # System / audit
        "add_logentry", "change_logentry", "delete_logentry", "view_logentry",
        "add_contenttype", "change_contenttype", "delete_contenttype", "view_contenttype",
        "add_session", "change_session", "delete_session", "view_session",
        "add_auditlog", "change_auditlog", "delete_auditlog", "view_auditlog",

        # Client registration
        "add_clientregistration", "change_clientregistration",
        "delete_clientregistration", "view_clientregistration",

        # Company / fiscal year
        "add_fiscalyear", "change_fiscalyear", "delete_fiscalyear", "view_fiscalyear",
        "add_company", "change_company", "delete_company", "view_company",

        # Dashboard config
        "add_dashboardconfigurations", "change_dashboardconfigurations",
        "delete_dashboardconfigurations", "view_dashboardconfigurations",

        # Roles
        "add_roles", "change_roles", "delete_roles", "view_roles",
    ],
}