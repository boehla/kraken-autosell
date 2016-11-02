with import <nixpkgs> {}; {
 pyEnv = stdenv.mkDerivation {
   name = "py";
   buildInputs = [
    stdenv
    openssl
    python35Packages.virtualenv
  ];
  shellHook = ''
    if [ ! -d venv ]
    then
      virtualenv venv
    fi
    source venv/bin/activate
  '';
 };
}
