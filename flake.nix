{
  description = "Proton Drive CLI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs, ... }@inputs:
    let
      inherit (nixpkgs) lib;

      version = "0.9.0";

      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      systemAttrs = {
        x86_64-linux = {
          proton-system = "linux-x64";
          hash = "sha512-NTMCW6aa4RK2Tj4B+8wa0GiBNqQEP2z2pyiGln2F/c2ewjVHnC4RMXFhS+UiW/upNCdQmgXKWqYHHZJPp+kcqA==";
        };
        "aarch64-linux" = {
          proton-system = "linux-arm64";
          hash = "sha512-yNWmsXTlfwbQXLVINAC5lj+vWOdDtrM3Brtz7P9xgEf/zmtDmZQlW5S1sia5DS6RvvdBjslsHD9di/ObbNATIQ==";
        };
      };

      forEachSupportedSystem =
        f:
        lib.genAttrs supportedSystems (
          system:
          f {
            inherit system;
            pkgs = import nixpkgs { inherit system; };
          }
        );
    in
    {
      packages = forEachSupportedSystem (
        { pkgs, system }:
        let
          proton-drive-binary = pkgs.fetchurl {
            url = "https://proton.me/download/drive/cli/${version}/${
              systemAttrs.${system}.proton-system
            }/proton-drive";
            hash = "${systemAttrs.${system}.hash}";
          };

          # Executable bit is applied here, in a build step, so it never
          # affects the fetcher's content hash.
          bin = pkgs.runCommand "proton-drive-bin" { } ''
            install -Dm755 ${proton-drive-binary} $out/bin/proton-drive
          '';
        in
        {
          default = pkgs.buildFHSEnv {
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
        }
      );
    };
}
