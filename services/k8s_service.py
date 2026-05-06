import yaml

def explain_k8s_manifest(manifest_str: str) -> dict:
    try:
        docs = list(yaml.safe_load_all(manifest_str))
        explanations = []
        for doc in docs:
            if not doc:
                continue
            kind = doc.get("kind", "Unknown")
            name = doc.get("metadata", {}).get("name", "Unknown")
            namespace = doc.get("metadata", {}).get("namespace", "default")
            
            explanation = f"This manifest defines a **{kind}** named **{name}** in the **{namespace}** namespace."
            
            if kind == "Deployment":
                replicas = doc.get("spec", {}).get("replicas", 1)
                explanation += f" It will run **{replicas}** replica(s) of the application."
            elif kind == "Service":
                svc_type = doc.get("spec", {}).get("type", "ClusterIP")
                explanation += f" It is of type **{svc_type}**."
                
            explanations.append({"kind": kind, "name": name, "explanation": explanation})
            
        return {"success": True, "explanations": explanations}
    except Exception as e:
        return {"success": False, "error": str(e)}
