import os

class WorkDir():
    '''
    用于设置工作路径的类
    使用方式 with WorkDir(user_name):
    '''
    def __init__(self,user_name):
        self.user_name=user_name
    def __enter__(self):
        if not os.path.exists("work"):
            os.mkdir("work")
        if not os.path.exists(f"work\\{self.user_name}"):
            os.mkdir(f"work\\{self.user_name}")
        os.chdir(f"work\\{self.user_name}")
    def __exit__(self, type, value, trace):
        os.chdir("..\\..")
