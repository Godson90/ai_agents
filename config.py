import yaml


def config():
    # Define file paths for YAML configurations
    files = {
        'agents': r'C:\Workspace\CrewAI\ai_agents\config\agents.yaml',
    }
    # Load configurations from YAML files
    configs = {}
    for config_type, file_path in files.items():
        with open(file_path, 'r') as file:
            configs[config_type] = yaml.safe_load(file)
    # Assign loaded configurations to specific variables
    agents_config = configs['agents']
    return agents_config
