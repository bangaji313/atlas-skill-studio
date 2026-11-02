from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('atlas',ROOT/'atlas.py')
atlas=importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)

class AssemblerTests(unittest.TestCase):
    def test_catalog_counts_and_unique_names(self):
        lock=json.loads((ROOT/'catalog/atlas.lock.json').read_text(encoding='utf-8'))
        self.assertEqual(len(lock['skills']),227)
        self.assertEqual(len({s['name'] for s in lock['skills']}),227)
        for name,_,count in atlas.STUDIOS.values():
            self.assertEqual(sum(s['studio']==name for s in lock['skills']),count)

    def test_paths_cannot_escape_or_target_git(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory)
            for value in ['../secret','/absolute','C:/secret','a\\b','.git/config','.GIT/config','a/../../secret','a\nb','']:
                with self.subTest(value=value),self.assertRaises(ValueError):atlas.contained(base,value)
            self.assertEqual(atlas.contained(base,'skills/example/SKILL.md'),base/'skills/example/SKILL.md')

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            try:(Path(a)/'escape').symlink_to(Path(b),target_is_directory=True)
            except OSError:self.skipTest('OS does not permit test symlink creation')
            with self.assertRaises(ValueError):atlas.contained(Path(a),'escape/secret')

    def test_patch_preserves_line_endings_and_multiple_edits(self):
        before=b'a\nb\nc\nd\n'
        edits=[dict(start=1,end=2,lines=['B\n']),dict(start=3,end=4,lines=['D\r\n','E\n'])]
        self.assertEqual(atlas.patched(before,edits),b'a\nB\nc\nD\r\nE\n')

    def test_patch_rejects_bad_ranges(self):
        for edits in [[dict(start=-1,end=1,lines=[])],[dict(start=0,end=8,lines=[])],
                      [dict(start=0,end=2,lines=[]),dict(start=1,end=2,lines=[])]]:
            with self.subTest(edits=edits),self.assertRaises(ValueError):atlas.patched(b'a\nb\n',edits)

    def test_catalog_local_inputs_are_exact_and_contained(self):
        lock=json.loads((ROOT/'catalog/atlas.lock.json').read_text(encoding='utf-8'))
        for entry in lock['files']:
            atlas.contained(ROOT,entry['path'])
            if 'local' in entry:
                self.assertEqual(atlas.digest(atlas.contained(ROOT,entry['local']).read_bytes()),entry['sha256'])
            if 'patch' in entry:
                edits=json.loads(atlas.contained(ROOT,entry['patch']).read_text(encoding='utf-8'))
                self.assertIsInstance(edits,list)
            if 'source' in entry:
                source=lock['sources'][entry['source']]
                self.assertRegex(source['commit'],r'^[0-9a-f]{40}$')
                atlas.contained(ROOT,entry['source_path'])

    def test_antigravity_long_guides_survive_without_mutating_other_hosts(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);plugin=base/'plugin';skill=plugin/'skills/long'
            skill.mkdir(parents=True)
            original='---\nname: long\ndescription: Test a long skill\n---\n\n'+('Full source instructions.\n'*1200)
            other=base/'other-host.md';other.write_text(original,encoding='utf-8')
            entry=skill/'SKILL.md'
            try:entry.hardlink_to(other)
            except OSError:entry.write_text(original,encoding='utf-8')
            self.assertEqual(atlas.antigravity_entrypoints(plugin),['long'])
            self.assertEqual((skill/'ATLAS-FULL-GUIDE.md').read_text(encoding='utf-8'),original)
            self.assertEqual(other.read_text(encoding='utf-8'),original)
            self.assertLess(len(entry.read_bytes()),24000)

if __name__=='__main__':unittest.main()
