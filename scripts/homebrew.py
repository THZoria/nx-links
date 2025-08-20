from basemodule import BaseModule

class Homebrew(BaseModule):
    def __init__(self):
        
        self.config = [
            {
                "username": "XorTroll",
                "reponame": "Goldleaf",
                "assetPatterns": [r".*Goldleaf.*\.nro"]
            }
        ]
        BaseModule.__init__(self)

    def handle_module(self):
        a = []
        
        a.append([{"username": "rashevskyv",  "reponame": "dbi",                "homebrew": True,  "assetPatterns": [r".*DBI.*\.nro"]}])
        a.append([{"username": "WerWolv",     "reponame": "EdiZon",             "homebrew": True,  "assetPatterns": [r".*EdiZon.*\.nro"]}])
        a.append([{"username": "mtheall",     "reponame": "ftpd",               "homebrew": True,  "assetPatterns": [r".*ftpd-classic.*\.nro"]}])
        a.append([{"username": "XorTroll",    "reponame": "Goldleaf",           "homebrew": True,  "assetPatterns": [r".*Goldleaf.*\.nro"]}])
        a.append([{"username": "WerWolv",     "reponame": "Hekate-Toolbox",     "homebrew": True,  "assetPatterns": [r".*HekateToolbox.*\.nro"]}])
        a.append([{"username": "J-D-K",       "reponame": "JKSV",               "homebrew": True,  "assetPatterns": [r".*JKSV.*\.nro"]}])
        a.append([{"username": "tallbl0nde",  "reponame": "NX-Activity-Log",    "homebrew": True,  "assetPatterns": [r".*NX-Activity-Log.*\.nro"]}])
        a.append([{"username": "PoloNX",      "reponame": "Ls-News",            "homebrew": True,  "assetPatterns": [r".*Ls-News.*\.nro"]}])
        a.append([{"username": "PoloNX",      "reponame": "SimpleModDownloader","homebrew": True,  "assetPatterns": [r".*SimpleModDownloader.*\.nro"]}])
        a.append([{"username": "nadrino",     "reponame": "SimpleModManager",   "homebrew": True,  "assetPatterns": [r".*SimpleModManager.*\.nro"]}])

        a.append([{"username": "ndeadly",     "reponame": "MissionControl",     "homebrew": False, "assetPatterns": [r".*MissionControl.*\.zip"]}])
        a.append([{"username": "exelix11",    "reponame": "SysDVR",             "homebrew": False, "assetPatterns": [r"SysDVR\.zip"]}])
        a.append([{"username": "WerWolv",     "reponame": "nx-ovlloader",       "homebrew": False, "assetPatterns": [r".*nx-ovlloader.*\.zip"]}])
        # overlays
        a.append([{"username": "WerWolv",     "reponame": "Tesla-Menu",         "homebrew": False, "assetPatterns": [r".*ovlmenu.*\.zip"]}])
        a.append([{"username": "Hartie95",    "reponame": "fastCFWswitch",      "homebrew": False, "assetPatterns": [r".*fastCFWswitch.*\.zip"]}])
        a.append([{"username": "HookedBehemoth","reponame":"sys-tune",          "homebrew": False, "assetPatterns": [r".*sys-tune.*\.zip"]}])

        for i in a:
            self.config = i

            
            if self.config[0]["reponame"] in ("Goldleaf", "emuiibo"):
                release = self.get_latest_pre_release(0)
            else:
                release = self.get_latest_release(0)

            
            if release is None:
                print(f'No available releases for: {self.config[0]["username"]} / {self.config[0]["reponame"]}')
                continue

            
            assets = self.get_asset_link(release, self.config[0]["assetPatterns"][0])

            
            if not assets:
                print(f'No matching assets for: {self.config[0]["username"]} / {self.config[0]["reponame"]}')
                continue

            asset = assets[0]
            self.out[self.config[0]["reponame"]] = {
                "name": self.config[0]["reponame"],
                "link": asset.browser_download_url,
                "version": release.tag_name,
                "homebrew": self.config[0]["homebrew"]
            }
