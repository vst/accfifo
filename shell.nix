{ pkgs ? import <nixpkgs> { }
, python ? "python310"
, ...
}:

let
  python-with-packages = pkgs.${python}.withPackages (p: with p; [
    ## Development dependencies:
    black
    isort

    ## Packaging dependencies:
    build
    twine
  ]);
in
pkgs.mkShell {
  buildInputs = [
    python-with-packages
  ];
}
