from pathlib import Path

class ProjectEnvironment():

    def __init__(self, repo_root, project_folder_name):
        self._repo_root = Path(repo_root)
        self._project_folder_name = project_folder_name

        self.content_directory = self._get_content_directory()
        
    def _get_content_directory(self):
        return self._repo_root.joinpath("Content")

