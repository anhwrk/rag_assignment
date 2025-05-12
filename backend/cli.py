import os
import argparse
from pathlib import Path

def normalize_name(name: str) -> str:
    """Convert hyphenated or space-separated names to snake_case"""
    return name.replace('-', '_').replace(' ', '_').lower()

def snake_to_pascal(name: str) -> str:
    """Convert snake_case to PascalCase with special handling for CVS"""
    # First normalize the name to ensure we're working with snake_case
    name = normalize_name(name)
    
    # Special case for CVS
    words = name.split('_')
    capitalized_words = []
    for word in words:
        if word.lower() == 'cvs':
            capitalized_words.append('CVS')
        else:
            capitalized_words.append(word.capitalize())
    
    return ''.join(capitalized_words)

def service_template(name):
    pascal_name = snake_to_pascal(name)
    normalized_name = normalize_name(name)
    
    return f"""from loguru import logger
from core.decorators.service import Service

@Service()
class {pascal_name}Service:
    def __init__(self):
        logger.info("Initialize {pascal_name} service")
"""

def controller_template(name):
    pascal_name = snake_to_pascal(name)
    normalized_name = normalize_name(name)
    url_prefix = normalized_name.replace('_', '-')
    
    return f"""from core.fastapi.models import GetQueries
from fastapi import Request, Body
from loguru import logger

from core.decorators import Controller
from core.decorators.auth import Auth
from .{normalized_name}_service import {pascal_name}Service

@Controller(tags=["{normalized_name}"], prefix="/{url_prefix}")
@Auth()
class {pascal_name}Controller:
    def __init__(self):
        self.service = {pascal_name}Service()
        logger.info("Initialize {pascal_name} controller")
        
    def _register_routes(self):
        @self.router.post("/sample-route")
        async def sample_route():
            return None
"""

def init_template(name):
    pascal_name = snake_to_pascal(name)
    normalized_name = normalize_name(name)
    return f"""from .{normalized_name}_controller import {pascal_name}Controller
from .{normalized_name}_service import {pascal_name}Service

__all__ = ["{pascal_name}Controller", "{pascal_name}Service"]
"""

# Function to generate the controller file
def generate_files(directory: str, path: Path):
    normalized_name = normalize_name(directory)
    controller_file = path / f"{normalized_name}_controller.py"
    service_file = path / f"{normalized_name}_service.py"
    
    with open(controller_file, "w") as f:
        f.write(controller_template(directory))
    print(f"Generated {controller_file}")
    
    with open(service_file, "w") as f:
        f.write(service_template(directory))
    print(f"Generated {service_file}")
    
    init_file = path / "__init__.py"
    with open(init_file, "w") as f:
        f.write(init_template(directory))
    print(f"Generated {init_file}")
    
# Function to create the folder structure
def create_directory_structure(base_dir: Path, sub_dir: str):
    full_path = base_dir / sub_dir
    full_path.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {full_path}")
    return full_path

def update_v1_router(name: str):
    """Update the v1/__init__.py to include the new controller"""
    init_file = Path("app/v1/__init__.py")
    if not init_file.exists():
        return
    
    pascal_name = snake_to_pascal(name)
    
    with open(init_file, "r") as f:
        content = f.read()
    
    # Add import if not exists
    import_line = f"from .{name} import {pascal_name}Controller"
    if import_line not in content:
        # Find the last import line
        lines = content.split("\n")
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("from ."):
                last_import_idx = i
        
        # Insert new import after last import
        lines.insert(last_import_idx + 1, import_line)
        
        # Add router line if not exists
        router_line = f"v1_router.include_router({pascal_name}Controller().router)"
        if router_line not in content:
            # Find the last router.include line
            last_router_idx = 0
            for i, line in enumerate(lines):
                if "include_router" in line:
                    last_router_idx = i
            
            # Insert new router line after last router line
            lines.insert(last_router_idx + 1, router_line)
        
        # Write back the file
        with open(init_file, "w") as f:
            f.write("\n".join(lines))
        print(f"Updated {init_file} with new controller")

# Main function to parse command-line arguments and run the generation
def main():
    parser = argparse.ArgumentParser(description="FastAPI boilerplate generator")
    parser.add_argument("command", help="Command to run (e.g., 'new')")
    parser.add_argument("name", help="Name of the module to create")
    
    args = parser.parse_args()
    
    # Base directory for the app
    base_dir = Path("app/v1")
    
    if args.command == "new":
        directory = create_directory_structure(base_dir, args.name)
        generate_files(args.name, directory)
        update_v1_router(args.name)

if __name__ == "__main__":
    main()
