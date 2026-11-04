"""Local staging safety checks; these are not remote deployment evidence."""
import hashlib,json,tempfile,unittest
from pathlib import Path
from stage_bundle import prepare
from verify_staging import cache_error
class Staging(unittest.TestCase):
    def fixture(self,root):
        site=root/'native-site';site.mkdir();(site/'index.html').write_text('checked fixture')
        (root/'native-provenance.json').write_text(json.dumps({'schema':1,'website_sha':'a'*40,'website_dirty':False,'compiler_sha':json.loads((Path(__file__).parent/'compiler.json').read_text())['sha'],'files':{'index.html':hashlib.sha256(b'checked fixture').hexdigest()}}));return site
    def test_verified_bundle_reproducible_and_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);site=self.fixture(root)
            first=prepare(root,'a'*40,root/'one');second=prepare(root,'a'*40,root/'two');self.assertEqual(first,second)
            (site/'index.html').write_text('substitution')
            with self.assertRaises(ValueError):prepare(root,'a'*40,root/'bad')
    def test_dirty_or_different_commit_cannot_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root)
            with self.assertRaises(ValueError):prepare(root,'c'*40,root/'bad')
            receipt=json.loads((root/'native-provenance.json').read_text());receipt['website_dirty']=True;(root/'native-provenance.json').write_text(json.dumps(receipt))
            with self.assertRaises(ValueError):prepare(root,'a'*40,root/'bad')
    def test_wrong_compiler_and_symlink_root_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);site=self.fixture(root);receipt=json.loads((root/'native-provenance.json').read_text());receipt['compiler_sha']='c'*40;(root/'native-provenance.json').write_text(json.dumps(receipt))
            with self.assertRaises(ValueError):prepare(root,'a'*40,root/'bad')
            receipt['compiler_sha']=json.loads((Path(__file__).parent/'compiler.json').read_text())['sha'];(root/'native-provenance.json').write_text(json.dumps(receipt))
            site.rename(root/'real');site.symlink_to(root/'real',target_is_directory=True)
            with self.assertRaises(ValueError):prepare(root,'a'*40,root/'bad')
    def test_mutable_http_resources_must_revalidate(self):
        for file in ('index.html','app.js','docs.css','docs-index.json'):
            self.assertIsNotNone(cache_error(file,{}));self.assertIsNotNone(cache_error(file,{'Cache-Control':'max-age=86400'}))
            self.assertIsNone(cache_error(file,{'Cache-Control':'no-cache'}));self.assertIsNone(cache_error(file,{'Cache-Control':'public, max-age=300'}))
        self.assertIsNone(cache_error('assets/'+'a'*64+'.woff2',{'Cache-Control':'public, max-age=31536000, immutable'}))
if __name__=='__main__':unittest.main()
