from fluigi_cloud.db.file import File
from fluigi_cloud.db.workspace import Workspace


@staticmethod
def add_new_file_to_workspace(file_model_ref: File, workspace_id: str):
    """Adds a file to a workspace

    Args:
        file_id (str): The id of the file to add
        workspace_id (str): The id of the workspace to add the file to

    Returns:
        str: The id of the file that was added
    """
    workspace = Workspace.objects.get(id=workspace_id)
    workspace.design_files.append(file_model_ref)
    workspace.save()
    

