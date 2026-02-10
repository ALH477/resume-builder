{
  description = "GTK Resume Builder - A professional HTML resume generator with web interface";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

   outputs = { self, nixpkgs, flake-utils }:
     flake-utils.lib.eachDefaultSystem (system:
       let
         pkgs = nixpkgs.legacyPackages.${system};
         
         pythonWithPackages = pkgs.python3.withPackages (ps: with ps; [
           pygobject3
           flask
         ]);
         
          resume-builder = pkgs.python3Packages.buildPythonApplication {
           pname = "resume-builder";
           version = "1.1.0";
           
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
             mkdir -p $out/share/resume-builder
             mkdir -p $out/share/applications
             mkdir -p $out/share/doc/resume-builder
             
             cp resume_builder.py $out/share/resume-builder/
             cp html_generator.py $out/share/resume-builder/
             if [ -f web_app.py ]; then cp web_app.py $out/share/resume-builder/; fi
             chmod +x $out/share/resume-builder/resume_builder.py
             chmod +x $out/share/resume-builder/html_generator.py
             if [ -f $out/share/resume-builder/web_app.py ]; then chmod +x $out/share/resume-builder/web_app.py; fi
             
             cp resume-builder.desktop $out/share/applications/
             cp README.md LICENSE CHANGELOG.md CONTRIBUTING.md $out/share/doc/resume-builder/
           '';
           
           # Custom postFixup to wrap the Python script with proper environment
           preFixup = ''
             makeWrapper ${pythonWithPackages}/bin/python $out/bin/resume-builder \
               --add-flags $out/share/resume-builder/resume_builder.py \
               --prefix GI_TYPELIB_PATH : "$GI_TYPELIB_PATH" \
               --prefix GDK_PIXBUF_MODULE_FILE : "$GDK_PIXBUF_MODULE_FILE" \
               --prefix XDG_DATA_DIRS : "$out/share" \
               --prefix PYTHONPATH : "$out/share/resume-builder"
           '';
          
          meta = with pkgs.lib; {
            description = "A GTK3 and web-based resume builder that generates professional HTML resumes";
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
               pythonWithPackages
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
              "org.opencontainers.image.description" = "GTK3 and web-based resume builder - use --web for Docker";
              "org.opencontainers.image.version" = "1.1.0";
              "maintainer" = "ALH477";
            };
          };
        };
        
        webDockerImage = pkgs.dockerTools.buildImage {
          name = "resume-builder-web";
          tag = "latest";
          
          copyToRoot = pkgs.buildEnv {
            name = "web-image-root";
             paths = [
               pkgs.bash
               pythonWithPackages
              resume-builder
            ];
            pathsToLink = [ "/bin" "/lib" "/share" ];
          };
          
          config = {
            Cmd = [ "/bin/resume-builder" "--web" "--host" "0.0.0.0" "--port" "5000" ];
            ExposedPorts = {
              "5000/tcp" = {};
            };
            Labels = {
              "org.opencontainers.image.source" = "https://github.com/ALH477/resume-builder";
              "org.opencontainers.image.description" = "Web-based resume builder - Flask interface for Docker";
              "org.opencontainers.image.version" = "1.1.0";
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
          docker-web = webDockerImage;
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
             pythonWithPackages
            gtk3
            gobject-introspection
          ];
          
          shellHook = ''
            echo "Resume Builder development environment"
            echo "Desktop mode: python3 resume_builder.py"
            echo "Web mode: python3 web_app.py"
          '';
        };
      }
    );
}
