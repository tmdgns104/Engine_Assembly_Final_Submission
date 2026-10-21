import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('assembly',Path(__file__).with_name('assemble_submission.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class AssemblyTests(unittest.TestCase):
    def test_current_urls_move_but_historical_commit_stays(self):
        current='https://github.com/tmdgns104/Engine_Assembly_Runtime_Review/blob/main/test.pdf'
        self.assertEqual(m.relocate_url(current,'project',m.SOURCES),'../docs/test.pdf')
        old='https://github.com/tmdgns104/Engine_Assembly_Defect_Inspector/blob/cfaa372eece0cd6a7dc659cc316c256fb4b6af76/a.py'
        self.assertEqual(m.relocate_url(old,'project',m.SOURCES),old)
        root='https://github.com/tmdgns104/Engine_Assembly_Defect_Inspector'
        self.assertEqual(m.relocate_url(root,'docs',m.SOURCES),'../project/')
    def test_raw_lfs_url_moves_to_target(self):
        old='https://github.com/tmdgns104/Engine_Assembly_Runtime_Review/raw/refs/heads/main/M1_M2_dataset_evidence_v002.zip'
        self.assertIn('/Engine_Assembly_Final_Submission/raw/refs/heads/main/docs/',m.relocate_url(old,'docs',m.SOURCES))
    def test_rewrite_reference_links(self):
        old='https://github.com/tmdgns104/Engine_Assembly_Runtime_Review/blob/main/test.pdf'
        data=m.rewrite_readme('[PDF]('+old+')\n[R01]: '+old+'\n','project')
        self.assertIn('[PDF](../docs/test.pdf)',data)
        self.assertIn('[R01]: ../docs/test.pdf',data)
    def test_links_percent_encoded_unicode_and_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'docs').mkdir();(root/'docs'/'한글.pdf').write_bytes(b'pdf')
            (root/'README.md').write_text('[x](docs/%ED%95%9C%EA%B8%80.pdf)\n[wrong](docs/missing.pdf)\n[R]: docs/%ED%95%9C%EA%B8%80.pdf\n[external](https://example.com/x)\n')
            result=m.check_links(root/'README.md',root)
            self.assertEqual(result['checked'],2);self.assertEqual(result['missing'],['docs/missing.pdf'])
    def test_lfs_pointer_and_empty_file(self):
        ptr=b'version https://git-lfs.github.com/spec/v1\noid sha256:'+b'a'*64+b'\nsize 373981270\n'
        self.assertEqual(int(m.LFS.fullmatch(ptr)[2]),373981270)
        self.assertEqual(m.blob_digest(b''),'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391')
    def test_tree_prefix_preserves_bytes_modes_and_symlinks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);source=root/'source';target=root/'target';source.mkdir();target.mkdir()
            def g(cwd,*args):return subprocess.check_output(['git',*args],cwd=cwd).decode().strip()
            for folder in (source,target):
                g(folder,'init','-q');g(folder,'config','user.name','Test');g(folder,'config','user.email','test@example.invalid')
            (source/'keep.bin').write_bytes(b'hello\r\n\x00\xff');(source/'run.sh').write_text('echo hello\n');os.chmod(source/'run.sh',0o755)
            (source/'link').symlink_to('keep.bin');(source/'empty.txt').touch()
            g(source,'add','.');g(source,'commit','-qm','source');sha=g(source,'rev-parse','HEAD')
            (target/'README.md').write_text('original\n');g(target,'add','.');g(target,'commit','-qm','target')
            g(target,'fetch','-q',str(source),sha);g(target,'read-tree','--prefix=project/','-u',sha)
            self.assertEqual((target/'project/keep.bin').read_bytes(),(source/'keep.bin').read_bytes())
            self.assertTrue((target/'project/run.sh').stat().st_mode & 0o111)
            self.assertEqual(os.readlink(target/'project/link'),'keep.bin')
            tree=g(target,'write-tree');self.assertEqual(g(target,'rev-parse',tree+':project'),g(source,'rev-parse','HEAD^{tree}'))

if __name__=='__main__':unittest.main(verbosity=2)
