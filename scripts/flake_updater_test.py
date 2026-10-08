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
               { self, nixpkgs, ... }@inputs:
                let
                    inherit (nixpkgs) lib;

                    version = "0.8.0";

                    supportedSystems = [
                        "x86_64-linux"
                    ];

                    systemAttrs = {
                        x86_64-linux = {
                        proton-system = "linux-x64";
                        hash =
                            "sha512-1234";
                        };
                    };
                in
                    {
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
            self.assertIn(new_hash, content)
        except SystemExit:
            self.fail("Unexpected exception raised")
        