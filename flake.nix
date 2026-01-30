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
          
          nativeBuildInputs = with pkgs; [
            gobject-introspection
            wrapGAppsHook3
          ];
          
          format = "other";
          
          dontBuild = true;
          
          installPhase = ''
            mkdir -p $out/bin
            mkdir -p $out/share/resume-builder
            mkdir -p $out/share/applications
            mkdir -p $out/share/doc/resume-builder
            
            cp resume_builder.py $out/share/resume-builder/
            chmod +x $out/share/resume-builder/resume_builder.py
            
            cat > $out/bin/resume-builder <<EOF
            #!${pkgs.bash}/bin/bash
            exec ${pkgs.python3}/bin/python3 $out/share/resume-builder/resume_builder.py "\$@"
            EOF
            chmod +x $out/bin/resume-builder
            
            cp resume-builder.desktop $out/share/applications/
            cp README.md LICENSE CHANGELOG.md CONTRIBUTING.md $out/share/doc/resume-builder/
          '';
          
          meta = with pkgs.lib; {
            description = "A GTK3-based resume builder that generates professional HTML resumes";
            homepage = "https://github.com/ALH477/resume-builder";
            license = licenses.asl20;
            maintainers = [ "ALH477@users.noreply.github.com" ];
            platforms = platforms.linux;
          };
        };
        
        dockerImage = pkgs.dockerTools.buildImage {
          name = "resume-builder";
          tag = "latest";
          
          copyToRoot = pkgs.buildEnv {
            name = "image-root";
            paths = [
              pkgs.bash
              pkgs.python3
              pkgs.python3Packages.pygobject3
              pkgs.gtk3
              pkgs.gobject-introspection
              pkgs.glib
              pkgs.cairo
              pkgs.pango
              pkgs.gdk-pixbuf
              pkgs.xorg.libX11
              pkgs.xorg.libXcomposite
              pkgs.xorg.libXcursor
              pkgs.xorg.libXdamage
              pkgs.xorg.libXext
              pkgs.xorg.libXfixes
              pkgs.xorg.libXi
              pkgs.xorg.libXrandr
              pkgs.xorg.libXrender
              pkgs.xorg.libXtst
              pkgs.atk
              pkgs.at-spi2-atk
              resume-builder
            ];
            pathsToLink = [ "/bin" "/lib" "/share" ];
          };
          
          config = {
            Cmd = [ "/bin/resume-builder" ];
            Env = [
              "DISPLAY=:99"
              "PYTHONPATH=/share/resume-builder"
            ];
            Labels = {
              "org.opencontainers.image.source" = "https://github.com/ALH477/resume-builder";
              "org.opencontainers.image.description" = "A GTK3-based desktop application for building professional HTML resumes";
              "org.opencontainers.image.version" = "1.0.0";
              "maintainer" = "ALH477";
            };
          };
        };
        
      in
      {
        packages = {
          default = resume-builder;
          resume-builder = resume-builder;
          docker = dockerImage;
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
