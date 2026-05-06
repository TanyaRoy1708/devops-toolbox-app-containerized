def lint_dockerfile(dockerfile_content: str) -> dict:
    lines = dockerfile_content.split("\n")
    warnings = []
    has_user = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("USER "):
            has_user = True
        if line.startswith("RUN apt-get install") and "-y" not in line:
            warnings.append(f"Line {i+1}: 'apt-get install' should use the '-y' flag to avoid interactive prompts.")
        if line.startswith("FROM "):
            if "latest" in line:
                warnings.append(f"Line {i+1}: Avoid using the 'latest' tag in FROM instructions.")
                
    if not has_user:
        warnings.append("No USER instruction found. Containers should not run as root.")
        
    return {
        "success": True,
        "warnings": warnings,
        "passed": len(warnings) == 0
    }
