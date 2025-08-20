# scripts/basemodule.py
from github import Github, GithubException
import re
import argparse
import json

parser = argparse.ArgumentParser(description="Get links for AtmoPackUpdater")
requiredNamed = parser.add_argument_group('Require arguments')
requiredNamed.add_argument('-gt', '--githubToken', help='Github Token', required=True)
args, _unknown = parser.parse_known_args()


class BaseModule:
    def __init__(self, config: dict | list = {}):
        
        print("Init module: ", self.__module__)
        self.path = self.__module__ + ".json"
        self.out = {}
        
        self.handle_module()

    

    def _get_repo(self, index: int):
        gh = Github(args.githubToken)
        try:
            return gh.get_repo(self.config[index]["username"] + "/" + self.config[index]["reponame"])
        except GithubException:
            print("Unable to get: ",
                  self.config[index]["username"], "/", self.config[index]["reponame"])
            return None

    def get_latest_release(self, index: int):
        """
        Retourne la release la plus récente (ou None si aucune).
        Sûr même si la liste est vide.
        """
        repo = self._get_repo(index)
        if repo is None:
            return None
        try:
            releases = repo.get_releases()  # PaginatedList[Release]
            for rel in releases:            # évite releases[0] si vide
                return rel
            print("No available releases for: ",
                  self.config[index]["username"], "/", self.config[index]["reponame"])
            return None
        except GithubException:
            print("No available releases for: ",
                  self.config[index]["username"], "/", self.config[index]["reponame"])
            return None

    def get_latest_pre_release(self, index: int):
        """
        Retourne la première prerelease (beta) trouvée (ou None).
        """
        repo = self._get_repo(index)
        if repo is None:
            return None
        try:
            releases = repo.get_releases()
            for rel in releases:
                if getattr(rel, "prerelease", False):
                    return rel
            print("No available prerelease for: ",
                  self.config[index]["username"], "/", self.config[index]["reponame"])
            return None
        except GithubException:
            print("No available releases for: ",
                  self.config[index]["username"], "/", self.config[index]["reponame"])
            return None

    def get_releases(self, index: int):
        """
        Retourne un itérable de releases (PaginatedList) ou [] si erreur.
        """
        repo = self._get_repo(index)
        if repo is None:
            return []
        try:
            return repo.get_releases()
        except GithubException:
            print("No available releases for: ",
                  self.config[index]["username"], "/", self.config[index]["reponame"])
            return []

    

    def get_asset_link(self, release, pattern: str):
        """
        Retourne une liste d'assets de la release qui matchent regex `pattern`.
        release peut être None -> retourne [].
        """
        if release is None:
            return []
        assets = []
        try:
            for asset in release.get_assets():
                if re.search(pattern, asset.name):
                    assets.append(asset)
        except GithubException:
            
            pass
        return assets

    def get_asset_links(self, release, index: int):
        """
        Applique tous les patterns de self.config[index]["assetPatterns"] à la release.
        """
        assetPaths = []
        if release is not None:
            for pattern in self.config[index]["assetPatterns"]:
                assetPaths += self.get_asset_link(release, pattern)
        return assetPaths


    def handle_module(self):
        """
        Implémentation générique : parcourt la config et ajoute {asset.name: asset.url}.
        Les sous-classes redéfinissent généralement cette méthode.
        """
        if not hasattr(self, "config"):
            return
        for i in range(len(self.config)):
            release = self.get_latest_release(i)
            assets = self.get_asset_links(release, i)
            for a in assets:
                self.out[a.name] = a.browser_download_url

    def write_json(self):
        with open(self.path, 'w') as write_file:
            json.dump(self.out, write_file, indent=4)
