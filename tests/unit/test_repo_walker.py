import os
import shutil
import pytest
from pathlib import Path
from app.utils.repo_walker import gather_repository_content

@pytest.fixture
def temp_repo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    
    # Create a normal file
    (repo_dir / "file1.txt").write_text("Hello World")
    
    # Create a file to be ignored
    (repo_dir / "ignored.log").write_text("This should be ignored")
    (repo_dir / ".gitignore").write_text("*.log\nnode_modules/")
    
    # Create a directory to be ignored
    (repo_dir / "node_modules").mkdir()
    (repo_dir / "node_modules" / "secret.txt").write_text("Hidden")
    
    # Create a binary file
    with open(repo_dir / "binary.bin", "wb") as f:
        f.write(b"\x00\x01\x02\x03")
        
    return repo_dir

def test_gather_repository_content(temp_repo):
    content = gather_repository_content(str(temp_repo))
    
    # file1.txt should be present
    assert "file1.txt" in content
    assert content["file1.txt"] == "Hello World"
    
    # .gitignore should be present (if not ignored by itself)
    assert ".gitignore" in content
    
    # ignored.log and node_modules/secret.txt should NOT be present
    assert "ignored.log" not in content
    assert "node_modules/secret.txt" not in content
    
    # binary.bin should NOT be present
    assert "binary.bin" not in content
    
    # Total count: file1.txt and .gitignore
    assert len(content) == 2
