{ pkgs, ... }:

{
  packages = [
    (pkgs.python312.withPackages (ps: with ps; [
      build
      matplotlib
      numpy
      pandas
      pytest
      pytest-cov
      python-dotenv
      pyyaml
      ruff
      scipy
      seaborn
      setuptools
      wheel
    ]))
  ];
}
