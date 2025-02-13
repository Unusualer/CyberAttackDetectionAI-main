# Create backend structure
"backend/app", "backend/tests", "backend/alembic",
"backend/app/api", "backend/app/core", "backend/app/models", 
"backend/app/schemas", "backend/app/services", 
"backend/app/middleware", "backend/app/api/v1" |
    ForEach-Object { mkdir $_ }

# Create frontend structure
"frontend/src", "frontend/public",
"frontend/src/components", "frontend/src/services", 
"frontend/src/hooks", "frontend/src/utils", 
"frontend/src/store", "frontend/src/types" |
    ForEach-Object { mkdir $_ }

# Create ML engine structure
"ml_engine/models", "ml_engine/services", 
"ml_engine/utils", "ml_engine/tests" |
    ForEach-Object { mkdir $_ }

# Create agent structure
"agent/src", "agent/include", "agent/tests" |
    ForEach-Object { mkdir $_ }
