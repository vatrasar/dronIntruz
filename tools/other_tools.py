import shutil


def create_folder(folder_path):
    save_directory = folder_path
    import os
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)
    for filename in os.listdir(save_directory):
        file_path = os.path.join(save_directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return save_directory
