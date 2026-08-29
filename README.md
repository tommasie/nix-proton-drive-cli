# Nix flake for proton-drive

Packages the third-party [Proton Drive CLI](https://proton.me/drive/download#desktop) binary
as a Nix flake.

## Usage

```bash
nix run .                  # run proton-drive directly
nix build .                # build; binary at ./result/bin/proton-drive
```

## Updating the version / hash

You can find the latest released version in [this page](https://proton.me/download/drive/cli/index.html).

To update the hash in the fetcher:
1. Copy the sha512 sum and run `nix hash convert --from-algo sha512 $hash`;
2. Set the `hash` attribute with this value.

## NixOS integration

Add as a flake input:

```nix
inputs.proton-drive.url = "github:tommasie/nix-proton-drive-cli";
```

Then in your system flake, thread it through and add the package:

```nix
specialArgs = { inherit proton-drive; };
```

```nix
# configuration.nix
{ pkgs, proton-drive, ... }: {
  environment.systemPackages = [ proton-drive.packages.x86_64-linux.default ];
}
```

## Secrets / keyring requirement

`proton-drive` stores session credentials via `libsecret`, which requires a
running Secret Service provider (e.g. GNOME Keyring) on the session D-Bus —
not just the library being present. Enable it in your NixOS config:

```nix
services.gnome.gnome-keyring.enable = true;
security.pam.services.login.enableGnomeKeyring = true;
# Adjust the PAM service name to match your login/display manager
# (e.g. gdm-password, sddm) if you don't log in via plain console login.
```

## Platform

`x86_64-linux` only