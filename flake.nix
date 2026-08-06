{
  description = "Paper Trading Codex 1.1.2 - reproducible offline test environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
        pythonEnv = python.withPackages (ps: with ps; [
          build
          matplotlib
          numpy
          pandas
          pip
          pytest
          pytest-cov
          python-dotenv
          pyyaml
          ruff
          scipy
          seaborn
          setuptools
          wheel
        ]);
      in {
        packages.default = pythonEnv;
        packages.python = pythonEnv;

        devShells.default = pkgs.mkShell {
          packages = [ pythonEnv pkgs.git pkgs.just ];
          shellHook = ''
            export PYTHONPATH="$PWD''${PYTHONPATH:+:$PYTHONPATH}"
            echo "Paper Trading Codex 1.1.2"
            echo "Environment ready. No files or dependencies were modified."
          '';
        };
      });
}
