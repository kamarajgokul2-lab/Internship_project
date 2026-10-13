$projectPath = $PSScriptRoot
Set-Location -LiteralPath $projectPath
& "$projectPath\.venv\Scripts\python.exe" -m streamlit run "$projectPath\app.py" --server.address 127.0.0.1 --server.port 8501
