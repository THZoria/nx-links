import re
from basemodule import BaseModule

class Firmwares(BaseModule):
    def __init__(self):
        self.config = [
            {
                "username": "THZoria",
                "reponame": "NX_Firmware",
                "assetPatterns": [r".*Firmware.*\.zip"]
            }
        ]
        BaseModule.__init__(self)

    def handle_module(self):
        for i in range(len(self.config)):
            releases = self.get_releases(i)
            
            if not releases or getattr(releases, "totalCount", 0) == 0:
                print(f'No available releases for: {self.config[i]["username"]} / {self.config[i]["reponame"]}')
                continue

            
            
            for j in range(releases.totalCount):
                rel = releases[j]
                assets = self.get_asset_links(rel, i)
                if not assets:
                    continue
                for asset in assets:
                    
                    self.out[rel.title] = asset.browser_download_url
