from distutils.command.build_py import build_py
import os
from setuptools import setup


class GenerateBindings(build_py):
    os.system('echo generating bindings')
    # os.system('mkdir -p src-generated/main/python')
    os.system('protoc -I=proto_schema --python_out=proto_output proto_schema/user.proto')
    os.system('echo generated bindings')


setup(name='serializer-demo-proto_schema',
      version='0.0.1',
      description='Demo Protobuf schema for dow jones free data set',
      author='Yves',
      cmdclass={'build_py': GenerateBindings}
      )
