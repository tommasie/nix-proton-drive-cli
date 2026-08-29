{
  description = "Proton Drive CLI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      version = "0.8.0";
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      proton-drive-bin = pkgs.fetchurl {
        url = "https://proton.me/download/drive/cli/${version}/linux-x64/proton-drive";
        sha256 = "sha256-hXb7eT449Gb5CygoWg4Q6T6mtSmWadOweGNLUVioVBM=";
        executable = true;
      };
    in
    {
      packages.${system}.default = pkgs.buildFHSEnv {
        name = "proton-drive";
        version = ${version};
        targetPkgs =
          pkgs: with pkgs; [
            libsecret
            glib
            dbus
          ];
        runScript = pkgs.writeShellScript "proton-drive-run" ''
          exec ${proton-drive-bin} "$@"
        '';

        meta = {
          mainProgram = "proton-drive";
        };
      };
    };
}
