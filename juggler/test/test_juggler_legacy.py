'''
Created on 22.03.2015

@author: Konfuzzyus
'''

from juggler.test.base_testcase import JugglerTestCase
import os

PRJ_EMPTY_LEGACY_XML = '''
    <Project>
        <Name>Empty</Name>
        <Version>v1.0</Version>
        <Requires/>
        <Content/>
    </Project>'''

class TestJuggler(JugglerTestCase):

    def test_help(self):
        with self.assertRaises(SystemExit):
            self._run_juggler(['-h'])

    def test_publish(self):
        args = ['--user_config', self.user_config,
                'publish',
                self.src_dir,
                self.bin_dir]
        self._with_project_config(PRJ_EMPTY_LEGACY_XML)
        exit_code = self._run_juggler(args)
        self.assertEqual(exit_code, 0)
        self.assertIn('Empty_vanilla-1.0.0-local.tar.gz',
                      os.listdir(self.local_repo_dir))
