import os
from pathlib import Path

project_name = "youtube-realtime-pipeline"

list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/webhook_service/__init__.py",
    f"{project_name}/webhook_service/main.py",
    f"{project_name}/webhook_service/youtube_subscriber.py",
    f"{project_name}/webhook_service/config.py",
    f"{project_name}/data_ingestion/__init__.py",
    f"{project_name}/data_ingestion/youtube_api.py",
    f"{project_name}/data_ingestion/initial_load.py",
    f"{project_name}/data_ingestion/metadata_processor.py",
    f"{project_name}/database/__init__.py",
    f"{project_name}/database/mongodb_client.py",
    f"{project_name}/database/models.py",
    f"{project_name}/database/query_operations.py",
    f"{project_name}/api/__init__.py",
    f"{project_name}/api/main.py",
    f"{project_name}/api/routes.py",
    f"{project_name}/api/auth.py",
    f"{project_name}/chatbot/__init__.py",
    f"{project_name}/chatbot/app.py",
    f"{project_name}/chatbot/agents.py",
    f"{project_name}/chatbot/tools.py",
    f"{project_name}/chatbot/prompts.py",
    f"{project_name}/scripts/__init__.py",
    f"{project_name}/scripts/query_db.py",
    f"{project_name}/scripts/deploy.sh",
    f"{project_name}/tests/__init__.py",
    f"{project_name}/tests/test_webhook.py",
    f"{project_name}/tests/test_api.py",
    f"{project_name}/tests/test_database.py",
    "README.md",
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "setup.py",
    "Dockerfile",
    ".dockerignore",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
    else:
        print(f"{filename} is already present in {filedir} and has some content. Skipping creation.")

print(f"\n✓ Project structure for '{project_name}' created successfully!")
