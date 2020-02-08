import json
import os
import stat


def permissions_to_int(owner_read=False, owner_write=False, owner_execute=False,
                       group_read=False, group_write=False, group_execute=False,
                       world_read=False, world_write=False, world_execute=False):
    """
    Get the numeric mode represented by the given params
    See https://docs.python.org/3/library/os.html#os.chmod
    """

    permission_int = 0

    # User
    if owner_read:
        permission_int |= stat.S_IRUSR
    if owner_write:
        permission_int |= stat.S_IWUSR
    if owner_execute:
        permission_int |= stat.S_IXUSR

    # Group
    if group_read:
        permission_int |= stat.S_IRGRP
    if group_write:
        permission_int |= stat.S_IWGRP
    if group_execute:
        permission_int |= stat.S_IXGRP

    # Everyone else
    if world_read:
        permission_int |= stat.S_IROTH
    if world_write:
        permission_int |= stat.S_IWOTH
    if world_execute:
        permission_int |= stat.S_IXOTH

    return permission_int


def permissions_from_int(permission_int):
    return {
        "owner": {
            "read": permission_int & stat.S_IRUSR > 0,
            "write": permission_int & stat.S_IWUSR > 0,
            "execute": permission_int & stat.S_IXUSR > 0,
        },
        "group": {
            "read": permission_int & stat.S_IRGRP > 0,
            "write": permission_int & stat.S_IWGRP > 0,
            "execute": permission_int & stat.S_IXGRP > 0,
        },
        "world": {
            "read": permission_int & stat.S_IROTH > 0,
            "write": permission_int & stat.S_IWOTH > 0,
            "execute": permission_int & stat.S_IXOTH > 0
        }
    }


def test_get_permission_int():
    with open("test1.txt", "w") as f:
        f.write("1")

    os.chmod(
        "test1.txt",
        permissions_to_int(
            owner_read=True,
            owner_write=True,
            group_write=True,
            world_execute=True
        )
    )

    new_mode = os.lstat("test1.txt").st_mode

    print(json.dumps(permissions_from_int(new_mode), indent=2))


if __name__ == "__main__":
    test_get_permission_int()
