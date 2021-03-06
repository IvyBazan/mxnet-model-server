# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#     http://www.apache.org/licenses/LICENSE-2.0
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from collections import namedtuple

import pytest

from model_archiver.manifest_components.engine import EngineType
from model_archiver.manifest_components.manifest import RuntimeType
from model_archiver.model_packaging import generate_model_archive, package_model
from model_archiver.model_packaging_utils import ModelExportUtils


# noinspection PyClassHasNoInit
class TestModelPackaging:

    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    author = 'ABC'
    email = 'ABC@XYZ.com'
    engine = EngineType.MXNET.value
    model_name = 'my-model'
    model_path = 'my-model/'
    handler = 'a.py::my-awesome-func'
    export_path = '/Users/ghaipiyu/'

    args = Namespace(author=author, email=email, engine=engine, model_name=model_name, handler=handler,
                     runtime=RuntimeType.PYTHON.value, model_path=model_path, export_path=export_path, force=False)

    @pytest.fixture()
    def patches(self, mocker):
        Patches = namedtuple('Patches', ['arg_parse', 'export_utils', 'export_method'])
        patches = Patches(mocker.patch('model_archiver.model_packaging.ArgParser'),
                          mocker.patch('model_archiver.model_packaging.ModelExportUtils'),
                          mocker.patch('model_archiver.model_packaging.package_model'))

        return patches

    def test_gen_model_archive(self, patches):
        patches.arg_parse.export_model_args_parser.parse_args.return_value = self.args
        generate_model_archive()
        patches.export_method.assert_called()

    def test_export_model_method(self, patches):

        patches.export_utils.check_mar_already_exists.return_value = '/Users/ghaipiyu/'
        patches.export_utils.check_custom_model_types.return_value = '/Users/ghaipiyu', ['a.txt', 'b.txt']
        patches.export_utils.zip.return_value = None

        package_model(self.args, ModelExportUtils.generate_manifest_json(self.args))
        patches.export_utils.validate_inputs.assert_called()
        patches.export_utils.zip.assert_called()
        patches.export_utils.clean_temp_files.assert_called()
