import os
import shutil


git_path = os.path.join('.git')
hooks_path = os.path.join(git_path, 'hooks')
commitmsg_hook_path = os.path.join(hooks_path, 'commit-msg')


def install():
    check_git_path()
    if not os.path.isdir(hooks_path):
        os.makedirs(hooks_path, mode=0o755, exist_ok=True)
    uninstall()
    commitmsg_script_path = shutil.which('commit-msg')
    assert commitmsg_script_path
    os.symlink(commitmsg_script_path, commitmsg_hook_path)
    assert os.path.exists(commitmsg_hook_path)
    return commitmsg_hook_path


def uninstall():
    check_git_path()
    if os.path.exists(commitmsg_hook_path):
        os.remove(commitmsg_hook_path)
        return commitmsg_hook_path


def check_git_path():
    assert os.path.isdir(git_path)
