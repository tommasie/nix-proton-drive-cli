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

      proton-drive-binary = pkgs.fetchurl {
        url = "https://proton.me/download/drive/cli/${version}/linux-x64/proton-drive";
        hash = "sha512-z2HCaIxF4QVdit1iIdlHGlpbZL87zbhkYPXLGEFFlsxN8822YnyQl8lL7DKjyZFa2jIR7yrlvjPEbrvJlsyqKA==";
      };

      # Executable bit is applied here, in a build step, so it never
      # affects the fetcher's content hash.
      bin = pkgs.runCommand "proton-drive-bin" { } ''
        install -Dm755 ${proton-drive-binary} $out/bin/proton-drive
      '';
    in
    {
      packages.${system}.default = pkgs.buildFHSEnv {
        inherit version;
        name = "proton-drive";
        targetPkgs =
          pkgs: with pkgs; [
            libsecret
            glib
            dbus
          ];
        runScript = pkgs.writeShellScript "proton-drive-run" ''
          exec ${bin}/bin/proton-drive "$@"
        '';

        meta = {
          mainProgram = "proton-drive";
        };
      };
    };
}
