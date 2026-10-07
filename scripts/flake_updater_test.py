import unittest
import copy
import flake_updater

class FlakeUpdaterTest(unittest.TestCase):
    sample_flake = '''
        {
        description = "";

        inputs = {
            nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
        };

        outputs =
            { self, nixpkgs }:
                let
                    version = "0.8.0";
                    system = "x86_64-linux";
                    pkgs = import nixpkgs { inherit system; };

                    proton-drive-binary = pkgs.fetchurl {
                        url = "url";
                        hash = "sha512-1234";
                    };
                in
                    {
                        packages.${system}.default = pkgs.buildFHSEnv {
                        # content
                        };
                    }
    '''

    def test_change_version(self):
        flake_copy = copy.deepcopy(self.sample_flake)
        new_version = "0.9.0"
        try:
            content = flake_updater.update_version(flake_copy, new_version)
            self.assertTrue(f'version = "{new_version}";' in content)
        except SystemExit:
            self.fail("Unexpected exception raised")


    def test_change_hash(self):
        flake_copy = copy.deepcopy(self.sample_flake)
        new_hash = "sha512-5678"
        try:
            content = flake_updater.update_hash(flake_copy, new_hash)
            print(content)
            self.assertTrue(f'hash = "{new_hash}";' in content)
        except SystemExit:
            self.fail("Unexpected exception raised")
        