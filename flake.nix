{
  description = "GTK Resume Builder - A professional HTML resume generator";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        resume-builder = pkgs.python3Packages.buildPythonApplication {
          pname = "resume-builder";
          version = "1.0.0";
          
          src = ./.;
          
          propagatedBuildInputs = with pkgs; [
            python3Packages.pygobject3
            gtk3
            gobject-introspection
          ];
          
          buildInputs = with pkgs; [
            wrapGAppsHook
          ];
          
          nativeBuildInputs = with pkgs; [
            gobject-introspection
            wrapGAppsHook
          ];
          
          format = "other";
          
          dontBuild = true;
          
          installPhase = ''
            mkdir -p $out/bin
            mkdir -p $out/share/resume-builder
            mkdir -p $out/share/applications
            mkdir -p $out/share/doc/resume-builder
            
            # Install the main script
            cp resume_builder.py $out/share/resume-builder/
            chmod +x $out/share/resume-builder/resume_builder.py
            
            # Create wrapper script
            cat > $out/bin/resume-builder <<EOF
            #!${pkgs.bash}/bin/bash
            exec ${pkgs.python3}/bin/python3 $out/share/resume-builder/resume_builder.py "\$@"
            EOF
            chmod +x $out/bin/resume-builder
            
            # Install desktop entry
            cp resume-builder.desktop $out/share/applications/
            
            # Install documentation
            cp README.md LICENSE CHANGELOG.md CONTRIBUTING.md $out/share/doc/resume-builder/
          '';
          
          meta = with pkgs.lib; {
            description = "A GTK3-based resume builder that generates professional HTML resumes";
            homepage = "https://github.com/yourusername/resume-builder";
            license = licenses.asl20;
            maintainers = [ ];
            platforms = platforms.linux;
          };
        };
        
      in
      {
        packages = {
          default = resume-builder;
          resume-builder = resume-builder;
        };
        
        apps = {
          default = {
            type = "app";
            program = "${resume-builder}/bin/resume-builder";
          };
          resume-builder = {
            type = "app";
            program = "${resume-builder}/bin/resume-builder";
          };
        };
        
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            python3Packages.pygobject3
            gtk3
            gobject-introspection
          ];
          
          shellHook = ''
            echo "Resume Builder development environment"
            echo "Run: python3 resume_builder.py"
          '';
        };
      }
    );
}
