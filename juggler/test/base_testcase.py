'''
Created on 22.03.2015

@author: Konfuzzyus
'''

import unittest
import tempfile
import shutil
import os

class JugglerTestCase(unittest.TestCase):
    def _get_test_user_config(self):
        cfg_name = 'global.xml'
        format_dict = {'local': self.local_repo_dir,
                       'remote': self.remote_repo_dir}
        test_config = '''
        <Repositories>
            <Local>
               %(local)s
            </Local>
            <Remote>
                file://%(remote)s
            </Remote>
        </Repositories>''' % format_dict

        filename = os.path.join(self.cnf_dir, cfg_name)
        with open(filename, 'w') as config_file:
            config_file.write(test_config)
        return filename
    
    def _with_project_config(self, config):
        cfg_name = 'juggle.xml'
        filename = os.path.join(self.src_dir, cfg_name)
        with open(filename, 'w') as config_file:
            config_file.write(config)

    def _run_juggler(self, args):
        from juggler.__main__ import main
        return main(args)

    def setUp(self):
        self.cnf_dir = tempfile.mkdtemp()
        self.src_dir = tempfile.mkdtemp()
        self.bin_dir = tempfile.mkdtemp()
        self.local_repo_dir = tempfile.mkdtemp()
        self.remote_repo_dir = tempfile.mkdtemp()
        self.user_config = self._get_test_user_config()

    def tearDown(self):
        shutil.rmtree(self.cnf_dir)
        shutil.rmtree(self.src_dir)
        shutil.rmtree(self.bin_dir)
        shutil.rmtree(self.local_repo_dir)
        shutil.rmtree(self.remote_repo_dir)