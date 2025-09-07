#!/usr/bin/env python3
"""
Agent Serialization for Evolutionary Training

Handles saving, loading, and managing agent code and metadata
with support for different formats and compatibility checking.
"""
import os
import json
import pickle
import hashlib
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import importlib.util

@dataclass
class SerializedAgent:
    """Container for serialized agent data"""
    agent_id: str
    code: str
    metadata: Dict[str, Any]
    code_hash: str
    serialization_version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'agent_id': self.agent_id,
            'code': self.code,
            'metadata': self.metadata,
            'code_hash': self.code_hash,
            'serialization_version': self.serialization_version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SerializedAgent':
        """Create from dictionary"""
        return cls(**data)

class AgentSerializer:
    """
    Handles serialization and deserialization of evolutionary agents
    
    Supports multiple formats:
    - Python files (.py) - Human readable
    - JSON files (.json) - Structured metadata
    - Pickle files (.pkl) - Binary format for complex objects
    """
    
    def __init__(self, base_directory: str):
        """
        Initialize agent serializer
        
        Args:
            base_directory: Base directory for agent storage
        """
        self.base_directory = base_directory
        os.makedirs(base_directory, exist_ok=True)
    
    def save_agent_python(self, agent_id: str, code: str, metadata: Dict[str, Any], 
                         filepath: Optional[str] = None) -> str:
        """
        Save agent as Python file with metadata header
        
        Args:
            agent_id: Unique agent identifier
            code: Python code string
            metadata: Agent metadata dictionary
            filepath: Custom file path (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            filename = f"{agent_id}.py"
            filepath = os.path.join(self.base_directory, filename)
        
        # Generate code hash for integrity checking
        code_hash = self._generate_code_hash(code)
        
        # Create file content with metadata header
        file_content = self._format_python_file(agent_id, code, metadata, code_hash)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        return filepath
    
    def save_agent_json(self, agent_id: str, code: str, metadata: Dict[str, Any],
                       filepath: Optional[str] = None) -> str:
        """
        Save agent as JSON file
        
        Args:
            agent_id: Unique agent identifier
            code: Python code string
            metadata: Agent metadata dictionary
            filepath: Custom file path (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            filename = f"{agent_id}.json"
            filepath = os.path.join(self.base_directory, filename)
        
        code_hash = self._generate_code_hash(code)
        
        serialized_agent = SerializedAgent(
            agent_id=agent_id,
            code=code,
            metadata=metadata,
            code_hash=code_hash
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serialized_agent.to_dict(), f, indent=2)
        
        return filepath
    
    def load_agent_python(self, filepath: str) -> Optional[SerializedAgent]:
        """
        Load agent from Python file
        
        Args:
            filepath: Path to Python file
            
        Returns:
            SerializedAgent object or None if loading failed
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata and code
            metadata, code = self._parse_python_file(content)
            
            if not metadata or not code:
                return None
            
            # Verify code hash if present
            stored_hash = metadata.get('code_hash')
            if stored_hash:
                actual_hash = self._generate_code_hash(code)
                if stored_hash != actual_hash:
                    print(f"⚠️  Code hash mismatch in {filepath}")
            
            return SerializedAgent(
                agent_id=metadata.get('agent_id', os.path.basename(filepath)),
                code=code,
                metadata=metadata,
                code_hash=stored_hash or self._generate_code_hash(code)
            )
            
        except Exception as e:
            print(f"❌ Failed to load agent from {filepath}: {e}")
            return None
    
    def load_agent_json(self, filepath: str) -> Optional[SerializedAgent]:
        """
        Load agent from JSON file
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            SerializedAgent object or None if loading failed
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            agent = SerializedAgent.from_dict(data)
            
            # Verify code hash
            actual_hash = self._generate_code_hash(agent.code)
            if agent.code_hash != actual_hash:
                print(f"⚠️  Code hash mismatch in {filepath}")
            
            return agent
            
        except Exception as e:
            print(f"❌ Failed to load agent from {filepath}: {e}")
            return None
    
    def validate_agent_code(self, code: str) -> bool:
        """
        Validate that agent code can be executed
        
        Args:
            code: Python code string
            
        Returns:
            True if code is valid, False otherwise
        """
        try:
            # Try to compile the code
            compile(code, '<string>', 'exec')
            
            # Check for required get_action function
            exec_globals = {}
            exec(code, exec_globals)
            
            if 'get_action' not in exec_globals:
                return False
            
            # Check if get_action is callable
            get_action_func = exec_globals['get_action']
            if not callable(get_action_func):
                return False
            
            return True
            
        except Exception:
            return False
    
    def create_agent_backup(self, agent_id: str, code: str, metadata: Dict[str, Any],
                           backup_dir: Optional[str] = None) -> str:
        """
        Create a backup copy of an agent
        
        Args:
            agent_id: Agent identifier
            code: Agent code
            metadata: Agent metadata
            backup_dir: Backup directory (default: base_directory/backups)
            
        Returns:
            Path to backup file
        """
        if backup_dir is None:
            backup_dir = os.path.join(self.base_directory, "backups")
        
        os.makedirs(backup_dir, exist_ok=True)
        
        # Add backup timestamp to metadata
        import time
        backup_metadata = metadata.copy()
        backup_metadata['backup_timestamp'] = time.time()
        backup_metadata['original_agent_id'] = agent_id
        
        # Create backup filename with timestamp
        timestamp = int(time.time())
        backup_filename = f"{agent_id}_backup_{timestamp}.py"
        backup_filepath = os.path.join(backup_dir, backup_filename)
        
        return self.save_agent_python(f"{agent_id}_backup", code, backup_metadata, backup_filepath)
    
    def list_agents(self, file_extension: str = ".py") -> List[str]:
        """
        List all agent files in the base directory
        
        Args:
            file_extension: File extension to filter by
            
        Returns:
            List of agent file paths
        """
        agent_files = []
        
        for filename in os.listdir(self.base_directory):
            if filename.endswith(file_extension):
                filepath = os.path.join(self.base_directory, filename)
                agent_files.append(filepath)
        
        return sorted(agent_files)
    
    def get_agent_summary(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Get summary information about an agent without loading full code
        
        Args:
            filepath: Path to agent file
            
        Returns:
            Summary dictionary or None if failed
        """
        try:
            if filepath.endswith('.py'):
                agent = self.load_agent_python(filepath)
            elif filepath.endswith('.json'):
                agent = self.load_agent_json(filepath)
            else:
                return None
            
            if not agent:
                return None
            
            return {
                'agent_id': agent.agent_id,
                'file_path': filepath,
                'code_length': len(agent.code),
                'code_lines': len(agent.code.split('\n')),
                'metadata_keys': list(agent.metadata.keys()),
                'fitness': agent.metadata.get('fitness'),
                'generation': agent.metadata.get('generation'),
                'fighting_style': agent.metadata.get('fighting_style'),
                'code_hash': agent.code_hash
            }
            
        except Exception as e:
            print(f"❌ Failed to get summary for {filepath}: {e}")
            return None
    
    def _generate_code_hash(self, code: str) -> str:
        """Generate SHA-256 hash of code for integrity checking"""
        return hashlib.sha256(code.encode('utf-8')).hexdigest()[:16]  # First 16 chars
    
    def _format_python_file(self, agent_id: str, code: str, metadata: Dict[str, Any], 
                           code_hash: str) -> str:
        """Format Python file with metadata header"""
        header = f'''"""
Evolutionary Agent: {agent_id}
{'=' * (20 + len(agent_id))}

Metadata:
{json.dumps(metadata, indent=2)}

Code Hash: {code_hash}
Serialization Version: 1.0
"""

# Agent Code:
'''
        
        return header + code
    
    def _parse_python_file(self, content: str) -> tuple[Dict[str, Any], str]:
        """Parse Python file to extract metadata and code"""
        try:
            # Find the metadata section
            if '"""' not in content:
                return {}, content
            
            # Extract docstring
            parts = content.split('"""')
            if len(parts) < 3:
                return {}, content
            
            docstring = parts[1]
            code_part = '"""'.join(parts[2:])
            
            # Extract metadata from docstring
            metadata = {}
            
            # Look for JSON metadata
            if 'Metadata:' in docstring:
                metadata_start = docstring.find('Metadata:') + len('Metadata:')
                metadata_end = docstring.find('Code Hash:', metadata_start)
                if metadata_end == -1:
                    metadata_end = len(docstring)
                
                metadata_text = docstring[metadata_start:metadata_end].strip()
                try:
                    metadata = json.loads(metadata_text)
                except json.JSONDecodeError:
                    pass
            
            # Extract code hash
            if 'Code Hash:' in docstring:
                hash_line = [line for line in docstring.split('\n') if 'Code Hash:' in line]
                if hash_line:
                    metadata['code_hash'] = hash_line[0].split('Code Hash:')[1].strip()
            
            # Extract agent ID
            if 'Evolutionary Agent:' in docstring:
                id_line = [line for line in docstring.split('\n') if 'Evolutionary Agent:' in line]
                if id_line:
                    metadata['agent_id'] = id_line[0].split('Evolutionary Agent:')[1].strip()
            
            # Clean up code (remove comment markers)
            if code_part.startswith('\n# Agent Code:\n'):
                code_part = code_part[len('\n# Agent Code:\n'):]
            
            return metadata, code_part.strip()
            
        except Exception as e:
            print(f"⚠️  Failed to parse Python file: {e}")
            return {}, content

def test_agent_serialization():
    """Test the agent serialization system"""
    print("🧪 Testing Agent Serialization")
    print("=" * 50)
    
    # Create test directory
    test_dir = f"test_serialization_{int(time.time())}"
    
    try:
        serializer = AgentSerializer(test_dir)
        
        # Test data
        test_code = '''
def get_action(state):
    distance = state[22]
    if distance < 0.3:
        return 4  # punch
    else:
        return 2  # move right
'''
        
        test_metadata = {
            'fitness': 85.5,
            'generation': 3,
            'fighting_style': 'aggressive',
            'win_rate': 0.75
        }
        
        # Test 1: Save as Python file
        py_path = serializer.save_agent_python("test_agent_1", test_code, test_metadata)
        py_saved = os.path.exists(py_path)
        print(f"✅ Python save: {'PASS' if py_saved else 'FAIL'}")
        
        # Test 2: Load Python file
        loaded_agent = serializer.load_agent_python(py_path)
        py_loaded = (loaded_agent is not None and 
                    loaded_agent.agent_id == "test_agent_1" and
                    "def get_action" in loaded_agent.code)
        print(f"✅ Python load: {'PASS' if py_loaded else 'FAIL'}")
        
        # Test 3: Save as JSON file
        json_path = serializer.save_agent_json("test_agent_2", test_code, test_metadata)
        json_saved = os.path.exists(json_path)
        print(f"✅ JSON save: {'PASS' if json_saved else 'FAIL'}")
        
        # Test 4: Load JSON file
        loaded_json = serializer.load_agent_json(json_path)
        json_loaded = (loaded_json is not None and 
                      loaded_json.agent_id == "test_agent_2")
        print(f"✅ JSON load: {'PASS' if json_loaded else 'FAIL'}")
        
        # Test 5: Code validation
        valid_code = serializer.validate_agent_code(test_code)
        invalid_code = serializer.validate_agent_code("def invalid(): pass")
        validation_works = valid_code and not invalid_code
        print(f"✅ Code validation: {'PASS' if validation_works else 'FAIL'}")
        
        # Test 6: Agent listing
        agent_files = serializer.list_agents(".py")
        listing_works = len(agent_files) >= 1
        print(f"✅ Agent listing: {'PASS' if listing_works else 'FAIL'}")
        
        # Test 7: Agent summary
        summary = serializer.get_agent_summary(py_path)
        summary_works = (summary is not None and 
                        summary['agent_id'] == "test_agent_1" and
                        summary['fitness'] == 85.5)
        print(f"✅ Agent summary: {'PASS' if summary_works else 'FAIL'}")
        
        print(f"\n📊 Agent Serialization test complete")
        return True
        
    except Exception as e:
        print(f"❌ Agent Serialization test failed: {e}")
        return False
    
    finally:
        # Cleanup
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

if __name__ == "__main__":
    import time
    test_agent_serialization()
